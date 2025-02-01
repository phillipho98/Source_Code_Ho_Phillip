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

################################################################################################################




#imports for Qt python library that is used to create the calculator GUI
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLineEdit, QToolButton,
                             QWidget, QSizePolicy, QLayout)

from PyQt5.QtGui import QFont
#imports for math library that is used to evaluate the mathematical expressions
import math

class Button(QToolButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        #set size policy to make buttons expand horizontally but maintain vertical size at same time
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #sets the displayed text on the button
        self.setText(text)
    
    #used to set the size of the button
    def sizeHint(self):
        size = super().sizeHint()
        #for better visibility
        size.setHeight(size.height() + 20)
        #square-ish aspect ratio)
        size.setWidth(max(size.width(), size.height()))
        return size

class Calculator(QWidget):
    NumDigitButtons = 10
    
    #initialization of the calculator GUI
    def __init__(self, parent=None):
        super().__init__(parent)
        
        #display is the text box that shows the current input and result (i.e the calculator window)
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(100)
        
        #display font settings
        font = self.display.font()
        font.setPointSize(font.pointSize() + 4)
        self.display.setFont(font)
        
        #creates digit buttons 0-9 based off of NumDigitButtons being 10
        self.digitButtons = []
        for i in range(self.NumDigitButtons):
            self.digitButtons.append(self.createButton(str(i), self.digitClicked))
        
        #decimal point button
        self.pointButton = self.createButton(".", self.pointClicked)
        
        #backspace button
        self.backspaceButton = self.createButton("Backspace", self.backspaceClicked)

        #clear button
        self.clearButton = self.createButton("Clear", self.clear)
        
        #operator buttons
        self.divisionButton = self.createButton("/", self.operatorClicked)
        self.timesButton = self.createButton("×", self.operatorClicked)
        self.minusButton = self.createButton("-", self.operatorClicked)
        self.plusButton = self.createButton("+", self.operatorClicked)
        

        self.sinButton = self.createButton("sin", self.functionClicked)
        self.cosButton = self.createButton("cos", self.functionClicked)
        self.tanButton = self.createButton("tan", self.functionClicked)
        self.cotButton = self.createButton("cot", self.functionClicked)
        self.lnButton = self.createButton("ln", self.functionClicked)
        self.log10Button = self.createButton("log10", self.functionClicked)
        self.powerButton = self.createButton("^", self.operatorClicked)
        self.equalButton = self.createButton("=", self.equalClicked)
        
        #parentheses/bracket buttons
        self.openParenButton = self.createButton("(", self.parenthesisClicked)
        self.closeParenButton = self.createButton(")", self.parenthesisClicked)
        self.openCurlyButton = self.createButton("{", self.parenthesisClicked)
        self.closeCurlyButton = self.createButton("}", self.parenthesisClicked)
        
        #negative sign button
        self.negativeButton = self.createButton("(-)", self.negativeClicked)
        
        #main layout of the calculator GUI
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        #adds all buttons to the main layout
        mainLayout.addWidget(self.display, 0, 0, 1, 7)

        mainLayout.addWidget(self.backspaceButton, 1, 0, 1, 2)
        mainLayout.addWidget(self.clearButton, 1, 2, 1, 2)
        
        for i in range(1, self.NumDigitButtons):
            row = ((9 - i) // 3) + 2
            column = ((i - 1) % 3) + 1
            mainLayout.addWidget(self.digitButtons[i], row, column)
        
        mainLayout.addWidget(self.negativeButton, 5, 0)
        mainLayout.addWidget(self.digitButtons[0], 5, 1)
        mainLayout.addWidget(self.pointButton, 5, 2)
        
        mainLayout.addWidget(self.divisionButton, 2, 4)
        mainLayout.addWidget(self.timesButton, 3, 4)
        mainLayout.addWidget(self.minusButton, 4, 4)
        mainLayout.addWidget(self.plusButton, 5, 4)
        
        mainLayout.addWidget(self.sinButton, 2, 5)
        mainLayout.addWidget(self.cosButton, 3, 5)
        mainLayout.addWidget(self.tanButton, 4, 5)
        mainLayout.addWidget(self.cotButton, 5, 5)
        
        mainLayout.addWidget(self.lnButton, 2, 6)
        mainLayout.addWidget(self.log10Button, 3, 6)
        mainLayout.addWidget(self.powerButton, 4, 6)
        mainLayout.addWidget(self.equalButton, 5, 6)
        
        mainLayout.addWidget(self.openParenButton, 6, 0)
        mainLayout.addWidget(self.closeParenButton, 6, 1)
        mainLayout.addWidget(self.openCurlyButton, 6, 2)
        mainLayout.addWidget(self.closeCurlyButton, 6, 3)
        
        self.setLayout(mainLayout)
        self.setWindowTitle("Calculator")

    def createButton(self, text, member):
        button = Button(text)
        button.clicked.connect(member)
        return button


    #######################################ALL FUNCTIONS THAT ARE CALLED WHEN A BUTTON IS PRESSED#################

    def digitClicked(self):
        digit = self.sender().text()
        current_text = self.display.text()
        if current_text == '0' and digit != '0':  # Handle all digits including 0
            self.display.setText(digit)
        else:
            self.display.setText(current_text + digit)

    def functionClicked(self):
        function = self.sender().text() + '('
        current_text = self.display.text()
        if current_text == '0':
            self.display.setText(function)
        else:
            self.display.setText(current_text + function)

    def operatorClicked(self):
        operator = self.sender().text()
        current_text = self.display.text()
        if current_text == '0':
            self.display.setText(operator)
        else:
            self.display.setText(current_text + operator)

    def pointClicked(self):
        current_text = self.display.text()
        # Find the start of the current number being entered
        i = len(current_text) - 1
        while i >= 0 and (current_text[i].isdigit() or current_text[i] == '.'):
            i -= 1
        current_number = current_text[i+1:]
        if '.' not in current_number:
            self.display.setText(current_text + '.')

    def backspaceClicked(self):
        current_text = self.display.text()
        self.display.setText(current_text[:-1] if len(current_text) > 0 else '0')

    def parenthesisClicked(self):
        paren = self.sender().text()
        current_text = self.display.text()
        if current_text == '0':
            self.display.setText(paren)
        else:
            self.display.setText(current_text + paren)

    def negativeClicked(self):
        current_text = self.display.text()
        if current_text == '0':
            self.display.setText('-')
        else:
            # Insert negative sign at valid positions
            last_char = current_text[-1] if current_text else ''
            if last_char in ('+', '-', '×', '÷', '('):
                self.display.setText(current_text + '-')

    def clear(self):
        """Hard clear that resets completely"""
        self.display.setText('0')
        # Add any additional reset logic here if needed later

    def abortOperation(self):
        self.display.setText("####")

    def equalClicked(self):
        expression = (self.display.text()
                      .replace('{', '(')
                      .replace('}', ')')
                      .replace('÷', '/')
                      .replace('×', '*'))
        
        ##################################DEBUGGING IN TERMINAL####################################################
        try:
            print("Raw expression:", expression)  
            tokens = self.tokenize(expression)
            print("Tokens:", tokens)  
            rpn = self.parse_expression(tokens)
            print("RPN:", rpn)  
            result = self.evaluate_rpn(rpn)
            print("Result:", result) 
            self.display.setText(f"{result:.6f}".rstrip('0').rstrip('.') if '.' in f"{result}" else str(int(result)))
        except Exception as e:
            print(f"Error: {repr(e)} at:")  
            import traceback
            traceback.print_exc()
            self.abortOperation()

    #unary minus handling
    @staticmethod
    def tokenize(expression):
        tokens = []
        i = 0
        n = len(expression)
        while i < n:
            char = expression[i]
            if char.isspace():
                i += 1
                continue
            if char.isdigit() or char == '.':
                j = i
                while j < n and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                num = expression[i:j]
                tokens.append(num)
                i = j
            elif char.isalpha():
                j = i
                while j < n and expression[j].isalpha():
                    j += 1
                func = expression[i:j]
                tokens.append(func)
                i = j
            elif char in '+-*/^':
                if char == '-' and (i == 0 or tokens[-1] in '+-*/^(' or (tokens and tokens[-1] in ['(', 'sin', 'cos', 'tan', 'cot', 'ln', 'log10'])):
                    tokens.append('u-')
                else:
                    tokens.append(char)
                i += 1
            elif char in '()':
                tokens.append(char)
                i += 1
            else:
                raise ValueError("Invalid character")
        return tokens

    @staticmethod
    def parse_expression(tokens):
        output = []
        stack = []
        precedence = {'u-': 7, '^': 6, '*': 5, '/': 5, '+': 4, '-': 4,
                      'sin': 8, 'cos': 8, 'tan': 8, 'cot': 8, 'ln': 8, 'log10': 8}
        for token in tokens:
            if token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):
                output.append(float(token))
            elif token in precedence:
                while stack and stack[-1] != '(' and precedence.get(token, 0) <= precedence.get(stack[-1], 0):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
                if stack and stack[-1] in precedence:
                    output.append(stack.pop())
            else:
                raise ValueError("Unknown token")
        while stack:
            token = stack.pop()
            if token == '(':
                raise ValueError("Mismatched parentheses")
            output.append(token)
        return output

    #function evaluation in RPN processor
    @staticmethod
    def evaluate_rpn(rpn):
        stack = []
        #processes each token in the RPN expression
        for token in rpn:
            #numbers are directly pushed to the stack
            if isinstance(token, float):
                stack.append(token)
            
            #handles unary negation (e.g., -3)
            elif token == 'u-':
                stack.append(-stack.pop())
            
            #binary arithmetic operations
            elif token in {'+', '-', '*', '/', '^'}:
                #pop operands in reverse order (RPN is operand1 operand2 operator)
                b = stack.pop()
                a = stack.pop() if token != '^' else stack.pop()  #handling for exponent order
                
                #performs the operation and pushes result
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)  #handles exponents: a^b
                    
            #trigonometric functions (require single operand)
            elif token in {'sin', 'cos', 'tan', 'cot'}:
                a = stack.pop()
                if token == 'sin':
                    stack.append(math.sin(a))
                elif token == 'cos':
                    stack.append(math.cos(a))
                elif token == 'tan':
                    stack.append(math.tan(a))
                elif token == 'cot':
                    stack.append(1 / math.tan(a))
                    
            #logarithmic functions
            elif token in {'ln', 'log10'}:
                a = stack.pop()
                if a <= 0:
                    raise ValueError("Log of non-positive number")
                if token == 'ln':
                    stack.append(math.log(a))  #natural logarithm
                elif token == 'log10':
                    stack.append(math.log10(a))  #base-10 logarithm
                    
            #error handling for unknown operators
            else:
                raise ValueError("Unknown operator")
        
        #final result should be the only element left in stack
        if len(stack) != 1:
            raise ValueError("Invalid expression format")
            
        return stack[0]

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())