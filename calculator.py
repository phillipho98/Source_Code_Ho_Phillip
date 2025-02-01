#Author: Phillip Ho
#CWU ID: 49763643


#############################CS480 Advanced Software Engineering Lab 2 Requirements#############################

#Create a software that can do basic arithmetic/trigonometric/logarithmic operations (“+”,”-“,”*”,”/”, ”^”, sin, cos, tan, cot, ln, log10) 
#with real numbers involving parenthesis (“()”) and curly brackets (“{}”).

#Evaluation should  properly the mathematic formula based on the precedence of the operators, 
#the parenthesis and the aforementioned mathematical functions.

#No external software library; except the math library.

#The “-“ should be considered as unary and binary operator as well based on the syntax. 
#Ex. “---3” (is three unary operators), “2-3” the “-“ is a binary operator. 

#The mathematic expression evaluation (see PN, RPN and shunting-yard algorithms if this is the
#choice you select) should be implemented in the software code. Do not use eval() or similar type
#of internal evaluation functions! [Note: External source code can be used, but is to be explicitly
#mentioned in your source code!]

#Note from professor:'You can use all kind of external libraries as far it is not about the expressions evaluation. Qt can be used.'

###########################################Lab 2 Grading Criteria###############################################

#1.The calculator should be able to correctly evaluate all kind of syntactically correct mathematic
#expressions. I.e. “-5.78+-(4-2.23)+sin(0)*cos(1)/(1+tan(2*ln(-3+2*(1.23+99.111)))=” (5p.) 

#2. The software should check for correct inputs. I.e. “((2+3/)(4/- = “ (4p.) 

#3. Usage of a version control system and proper description. (1p.) 

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLineEdit, QToolButton,
                             QWidget, QSizePolicy, QLayout)
from PyQt5.QtGui import QFont

class Button(QToolButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
    
    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

class Calculator(QWidget):
    NumDigitButtons = 10
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sumInMemory = 0.0
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.waitingForOperand = True
        self.pendingAdditiveOperator = ""
        self.pendingMultiplicativeOperator = ""
        
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)
        
        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)
        
        self.digitButtons = []
        for i in range(self.NumDigitButtons):
            self.digitButtons.append(self.createButton(str(i), self.digitClicked))
        
        self.pointButton = self.createButton(".", self.pointClicked)
        self.changeSignButton = self.createButton("±", self.changeSignClicked)
        
        self.backspaceButton = self.createButton("Backspace", self.backspaceClicked)
        self.clearButton = self.createButton("Clear", self.clear)
        self.clearAllButton = self.createButton("Clear All", self.clearAll)
        
        self.clearMemoryButton = self.createButton("MC", self.clearMemory)
        self.readMemoryButton = self.createButton("MR", self.readMemory)
        self.setMemoryButton = self.createButton("MS", self.setMemory)
        self.addToMemoryButton = self.createButton("M+", self.addToMemory)
        
        self.divisionButton = self.createButton("÷", self.multiplicativeOperatorClicked)
        self.timesButton = self.createButton("×", self.multiplicativeOperatorClicked)
        self.minusButton = self.createButton("-", self.additiveOperatorClicked)
        self.plusButton = self.createButton("+", self.additiveOperatorClicked)
        
        self.squareRootButton = self.createButton("Sqrt", self.unaryOperatorClicked)
        self.powerButton = self.createButton("x²", self.unaryOperatorClicked)
        self.reciprocalButton = self.createButton("1/x", self.unaryOperatorClicked)
        self.equalButton = self.createButton("=", self.equalClicked)
        
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addWidget(self.display, 0, 0, 1, 6)
        mainLayout.addWidget(self.backspaceButton, 1, 0, 1, 2)
        mainLayout.addWidget(self.clearButton, 1, 2, 1, 2)
        mainLayout.addWidget(self.clearAllButton, 1, 4, 1, 2)
        
        mainLayout.addWidget(self.clearMemoryButton, 2, 0)
        mainLayout.addWidget(self.readMemoryButton, 3, 0)
        mainLayout.addWidget(self.setMemoryButton, 4, 0)
        mainLayout.addWidget(self.addToMemoryButton, 5, 0)
        
        for i in range(1, self.NumDigitButtons):
            row = ((9 - i) // 3) + 2
            column = ((i - 1) % 3) + 1
            mainLayout.addWidget(self.digitButtons[i], row, column)
        
        mainLayout.addWidget(self.digitButtons[0], 5, 1)
        mainLayout.addWidget(self.pointButton, 5, 2)
        mainLayout.addWidget(self.changeSignButton, 5, 3)
        
        mainLayout.addWidget(self.divisionButton, 2, 4)
        mainLayout.addWidget(self.timesButton, 3, 4)
        mainLayout.addWidget(self.minusButton, 4, 4)
        mainLayout.addWidget(self.plusButton, 5, 4)
        
        mainLayout.addWidget(self.squareRootButton, 2, 5)
        mainLayout.addWidget(self.powerButton, 3, 5)
        mainLayout.addWidget(self.reciprocalButton, 4, 5)
        mainLayout.addWidget(self.equalButton, 5, 5)
        
        self.setLayout(mainLayout)
        self.setWindowTitle("Calculator")

    def createButton(self, text, member):
        button = Button(text)
        button.clicked.connect(member)
        return button

    def digitClicked(self):
        clickedButton = self.sender()
        digitValue = int(clickedButton.text())
        
        if self.display.text() == '0' and digitValue == 0:
            return
        
        if self.waitingForOperand:
            self.display.clear()
            self.waitingForOperand = False
            
        self.display.setText(self.display.text() + str(digitValue))

    def unaryOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
        result = 0.0
        
        if clickedOperator == "Sqrt":
            if operand < 0.0:
                self.abortOperation()
                return
            result = (operand) ** 0.5
        elif clickedOperator == "x²":
            result = operand ** 2
        elif clickedOperator == "1/x":
            if operand == 0.0:
                self.abortOperation()
                return
            result = 1.0 / operand
            
        self.display.setText(str(result))
        self.waitingForOperand = True

    def additiveOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
        
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.factorSoFar))
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ""
        
        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.sumSoFar))
        else:
            self.sumSoFar = operand
            
        self.pendingAdditiveOperator = clickedOperator
        self.waitingForOperand = True

    def multiplicativeOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
        
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.factorSoFar))
        else:
            self.factorSoFar = operand
            
        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True

    def equalClicked(self):
        operand = float(self.display.text())
        
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ""
            
        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self.pendingAdditiveOperator = ""
        else:
            self.sumSoFar = operand
            
        self.display.setText(str(self.sumSoFar))
        self.sumSoFar = 0.0
        self.waitingForOperand = True

    def pointClicked(self):
        if self.waitingForOperand:
            self.display.setText('0')
        if '.' not in self.display.text():
            self.display.setText(self.display.text() + '.')
        self.waitingForOperand = False

    def changeSignClicked(self):
        text = self.display.text()
        value = float(text)
        
        if value > 0:
            text = '-' + text
        elif value < 0:
            text = text[1:]
            
        self.display.setText(text)

    def backspaceClicked(self):
        if self.waitingForOperand:
            return
            
        text = self.display.text()[:-1]
        if not text:
            text = '0'
            self.waitingForOperand = True
        self.display.setText(text)

    def clear(self):
        if self.waitingForOperand:
            return
            
        self.display.setText('0')
        self.waitingForOperand = True

    def clearAll(self):
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.pendingAdditiveOperator = ""
        self.pendingMultiplicativeOperator = ""
        self.display.setText('0')
        self.waitingForOperand = True

    def clearMemory(self):
        self.sumInMemory = 0.0

    def readMemory(self):
        self.display.setText(str(self.sumInMemory))
        self.waitingForOperand = True

    def setMemory(self):
        self.equalClicked()
        self.sumInMemory = float(self.display.text())

    def addToMemory(self):
        self.equalClicked()
        self.sumInMemory += float(self.display.text())

    def abortOperation(self):
        self.clearAll()
        self.display.setText("####")

    def calculate(self, rightOperand, pendingOperator):
        if pendingOperator == "+":
            self.sumSoFar += rightOperand
        elif pendingOperator == "-":
            self.sumSoFar -= rightOperand
        elif pendingOperator == "×":
            self.factorSoFar *= rightOperand
        elif pendingOperator == "÷":
            if rightOperand == 0.0:
                return False
            self.factorSoFar /= rightOperand
        return True

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())