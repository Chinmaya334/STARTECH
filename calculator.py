import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Simple Calculator")
        self.window.geometry("300x400")
        self.window.configure(bg='#f0f0f0')
        
        # Variables to store numbers and operation
        self.current_number = ""
        self.previous_number = ""
        self.operation = ""
        
        # Create the display
        self.create_display()
        
        # Create buttons
        self.create_buttons()
    
    def create_display(self):
        """Create the display screen for the calculator"""
        # Display frame
        display_frame = tk.Frame(self.window, bg='#f0f0f0')
        display_frame.pack(pady=10, padx=10, fill='x')
        
        # Display entry widget
        self.display = tk.Entry(
            display_frame,
            font=('Arial', 20),
            justify='right',
            state='readonly',
            bg='white',
            fg='black',
            bd=2,
            relief='solid'
        )
        self.display.pack(fill='x', ipady=10)
        
        # Set initial display
        self.update_display("0")
    
    def create_buttons(self):
        """Create all calculator buttons"""
        # Button frame
        button_frame = tk.Frame(self.window, bg='#f0f0f0')
        button_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Button layout: [row][column]
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0 ', '00','.', '=']
        ]
        
        # Create buttons row by row
        for row_index, row in enumerate(buttons):
            for col_index, button_text in enumerate(row):
                if button_text == '0':
                    # Make 0 button span 2 columns
                    btn = tk.Button(
                        button_frame,
                        text=button_text,
                        font=('Arial', 18),
                        command=lambda text=button_text: self.button_click(text),
                        bg='#e0e0e0',
                        fg='black',
                        relief='raised',
                        bd=2
                    )
                    btn.grid(row=row_index, column=col_index, columnspan=2, 
                            sticky='ew', padx=2, pady=2, ipady=10)
                else:
                    # Regular button
                    btn = tk.Button(
                        button_frame,
                        text=button_text,
                        font=('Arial', 18),
                        command=lambda text=button_text: self.button_click(text),
                        bg=self.get_button_color(button_text),
                        fg='black' if button_text.isdigit() or button_text == '.' else 'white',
                        relief='raised',
                        bd=2
                    )
                    btn.grid(row=row_index, column=col_index, 
                            sticky='ew', padx=2, pady=2, ipady=10)
        
        # Configure grid weights for responsive design
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
    
    def get_button_color(self, button_text):
        """Return appropriate color for each button type"""
        if button_text.isdigit() or button_text == '.':
            return '#e0e0e0'  # Light gray for numbers
        elif button_text in ['+', '-', '×', '÷', '=']:
            return '#ff9500'  # Orange for operations
        else:
            return '#a6a6a6'  # Gray for special functions
    
    def button_click(self, button_text):
        """Handle button clicks"""
        try:
            if button_text.isdigit():
                self.number_click(button_text)
            elif button_text == '.':
                self.decimal_click()
            elif button_text in ['+', '-', '×', '÷']:
                self.operation_click(button_text)
            elif button_text == '=':
                self.equals_click()
            elif button_text == 'C':
                self.clear_click()
            elif button_text == '±':
                self.plus_minus_click()
            elif button_text == '%':
                self.percent_click()
        except Exception as e:
            self.show_error("Error occurred")
            self.clear_all()
    
    def number_click(self, number):
        """Handle number button clicks"""
        if self.current_number == "0":
            self.current_number = number
        else:
            self.current_number += number
        self.update_display(self.current_number)
    
    def decimal_click(self):
        """Handle decimal point button click"""
        if '.' not in self.current_number:
            if self.current_number == "":
                self.current_number = "0."
            else:
                self.current_number += "."
            self.update_display(self.current_number)
    
    def operation_click(self, op):
        """Handle operation button clicks (+, -, ×, ÷)"""
        if self.current_number == "":
            return
        
        if self.previous_number != "" and self.operation != "":
            self.equals_click()
        
        self.previous_number = self.current_number
        self.current_number = ""
        self.operation = op
        
        # Show the operation on display
        display_text = self.previous_number + " " + op
        self.update_display(display_text)
    
    def equals_click(self):
        """Handle equals button click"""
        if self.previous_number == "" or self.current_number == "" or self.operation == "":
            return
        
        try:
            # Convert to float for calculation
            num1 = float(self.previous_number)
            num2 = float(self.current_number)
            
            # Perform calculation based on operation
            if self.operation == '+':
                result = num1 + num2
            elif self.operation == '-':
                result = num1 - num2
            elif self.operation == '×':
                result = num1 * num2
            elif self.operation == '÷':
                if num2 == 0:
                    self.show_error("Cannot divide by zero!")
                    self.clear_all()
                    return
                result = num1 / num2
            
            # Format result (remove unnecessary decimals)
            if result == int(result):
                result = int(result)
            else:
                result = round(result, 8)  # Round to 8 decimal places
            
            # Update display and reset variables
            self.update_display(str(result))
            self.current_number = str(result)
            self.previous_number = ""
            self.operation = ""
            
        except Exception as e:
            self.show_error("Invalid calculation")
            self.clear_all()
    
    def clear_click(self):
        """Handle clear button click"""
        self.clear_all()
    
    def clear_all(self):
        """Clear all data and reset calculator"""
        self.current_number = ""
        self.previous_number = ""
        self.operation = ""
        self.update_display("0")
    
    def plus_minus_click(self):
        """Handle plus/minus button click (change sign)"""
        if self.current_number != "" and self.current_number != "0":
            if self.current_number.startswith('-'):
                self.current_number = self.current_number[1:]
            else:
                self.current_number = '-' + self.current_number
            self.update_display(self.current_number)
    
    def percent_click(self):
        """Handle percent button click"""
        if self.current_number != "":
            try:
                result = float(self.current_number) / 100
                if result == int(result):
                    result = int(result)
                self.current_number = str(result)
                self.update_display(self.current_number)
            except:
                self.show_error("Invalid percentage")
    
    def update_display(self, value):
        """Update the calculator display"""
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, str(value))
        self.display.config(state='readonly')
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
    
    def run(self):
        """Start the calculator application"""
        # Add keyboard support
        self.window.bind('<Key>', self.key_press)
        self.window.focus_set()
        
        # Start the main loop
        self.window.mainloop()
    
    def key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        
        if key.isdigit():
            self.button_click(key)
        elif key == '.':
            self.button_click('.')
        elif key == '+':
            self.button_click('+')
        elif key == '-':
            self.button_click('-')
        elif key == '*':
            self.button_click('×')
        elif key == '/':
            self.button_click('÷')
        elif key == '\r' or key == '=':  # Enter or equals
            self.button_click('=')
        elif key == '\x08':  # Backspace
            self.backspace()
        elif key.lower() == 'c':
            self.button_click('C')
    
    def backspace(self):
        """Handle backspace (delete last digit)"""
        if self.current_number != "":
            self.current_number = self.current_number[:-1]
            if self.current_number == "":
                self.current_number = "0"
            self.update_display(self.current_number)

# Create and run the calculator
if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()