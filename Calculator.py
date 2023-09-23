import tkinter as tk

#  fonts
Small_font = ("Arial", 16)
large_font = ("Arial", 40, "bold")
Digit_font = ("Arial", 24, "bold")
Symbol_font = ("Arial", 20)

# Colours
Light_gray = "#F5F5F5"
Blue = "#25265E"
White = "#FFFFFF"
off_white = "#F8FAFF"
Light_Blue = "#CCEDFF"


class Calculator:
    def __init__(self):
        # window specifications
        self.window = tk.Tk()
        self.window.geometry("450x600")
        self.window.title("Calculator")

        self.total_expression = ""  # Result
        # Display input abvove total_expression (Result)
        # in a muted (dim) manner
        self.current_expression = ""

        self.display_frame = self.create_display_frame()

        self.total_label, self.current_label = self.create_display_labels()

        # Buttons in grid system
        self.digits = {
            7:(1,1), 8:(1,2), 9:(1,3),
            4:(2,1), 5:(2,2), 6:(2,3),
            1:(3,1), 2:(3,2), 3:(3,3),
            '.':(4,1), 0: (4,2) 
        }
        # Adding operators
        # \u00F7 & \u00D7 unicode values for division & multiplication
        # symbols respectively
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        

        # Adding buttons
        self.buttons_frame = self.create_buttons_frame()
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_square_root_button()
        self.bind_keys()

    # Allow keyboard input
    def bind_keys(self):
        # Enter Button = Equals button (evaluate)
        self.window.bind("<Return>", lambda  event: self.evaluate())
        # BackSpace = AC (clear)
        self.window.bind("<BackSpace>", lambda  event: self.clear())
        # Refer lines 132 and 168
        for key in self.digits:
            self.window.bind(str(key), lambda event,digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(str(key), lambda event,operator=key: self.append_operator(operator))

        """
        The Buttons aren't filling the box so we configure it with a non-zero
        weight for all rows & columns.
        """
        self.buttons_frame.rowconfigure(0,weight=1)
        for x in range (1,5):
            self.buttons_frame.rowconfigure(x,weight=1)
            self.buttons_frame.columnconfigure(x,weight=1)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    """
    The positioning in the box madde by tkinter co-relates
    to a compass. E means right side & centre along the Y-axis. 
    User input & result will be displayed here. Originally both will be 0.
    """
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=Light_gray)
        frame.pack(expand=True, fill="both")
        return frame

    def create_display_labels(self):
        total_label = tk.Label(
            self.display_frame,
            text=self.total_expression,
            anchor=tk.E,
            bg=Light_gray,
            fg=Blue,
            padx=24,
            font=Small_font,
        )
        total_label.pack(expand=True, fill="both")

        current_label = tk.Label(
            self.display_frame,
            text=self.current_expression,
            anchor=tk.E,
            bg=Light_gray,
            fg=Blue,
            padx=24,
            font=large_font,
        )
        current_label.pack(expand=True, fill="both")

        return total_label, current_label

    """
    Makes the digit_buttons accept input. The current value is NULL. Clicking the digit_button
    fills the NULL field
    """
    # Replace default pythonic operators with unicode symbols (Refer line 40)
    def update_total_label(self):
        expression = self.total_expression
        for operator,symbol in self.operations.items():
            expression = expression.replace(operator, f"{symbol}")
        self.total_label.config(text=expression)

    def update_current_label(self):
        # [:11] Slicing operator added to limit the result to 11 characters (decimal included)
        self.current_label.config(text=self.current_expression[:11]) 

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_current_label()

    """
    Creating Buttons
    """
    def create_digit_buttons(self):
        for digit,grid_value in self.digits.items():
            button = tk.Button(
                self.buttons_frame,
                text=str(digit),
                bg = White,
                fg = Blue,
                font=Digit_font,
                borderwidth=0, # removes button border
                command=lambda x=digit: self.add_to_expression(x) # lambda bcoz the value
                # of command must be a function. So we make it a lamba function. Digit was bound
                # to x because digit variable is in loop. So only . (decimal) was being displayed
                # in the current_expression when any digit_button was pressed, as the loop started
                # again when digit_button was pressed & ended in . (decimal).
            )

            button.grid(
                row=grid_value[0],
                column=grid_value[1],
                sticky=tk.NSEW
                # button fills the entire cell. NSEW - Compass directions
            )


    """
    Adds the operator to the total_expression. Eg: If we press 9 it will be shown in
    current_expression. After that, pressing any OPERATOR (let's say -) will result in
    9- in the total_expression and empty string (NULL value) in the current_expression
    """
    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_current_label()

    """
    Creating Operators
    """
    def create_operator_buttons(self):
        i = 0
        for operator,symbol in self.operations.items():
            button = tk.Button(
                self.buttons_frame,
                text=symbol,
                bg=off_white,
                fg=Blue,
                font=Symbol_font,
                borderwidth=0,
                command=lambda x=operator: self.append_operator(x)
            )
            """
            These buttons should be at the last column & start 1 row above the
            DIGIT BUTTONS.
            """
            button.grid(
                row=i,
                column=4, # 3 columns for DIGIT BUTTONS
                sticky=tk.NSEW
            )
            i += 1

    """
    Finctionality to CLEAR the EXPRESSIONS fields.
    """
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_current_label()
        self.update_total_label()

    """
    eval function evalutes and returns the value of valid Python expression. In short,
    it calculates and gives answer. This builds on append_operator func in line 141.
    Eg: Pressing 8 & then X (Multiply) results in 8* in total_expression due to the 
    append_operator function. After that when we press 9 it results to 8* in total_expression
    & 9 in current_expression. Then when we press = (Equals) 8*9 will be in in total_expression
    & the result 72 will be in current_expression.
    Line 221 & 222 puts 8*9 in total_expression
    Line 224 calculates the expression in total_expression and prints it in current_expression
    """
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = "" #reset total_expresion in the logic
        except Exception as e:
            self.current_expression = "Error"
        # self.update_total_label() Add this if total_expression feild is wished
        # to be cleared visually too.
        # try block added to get Error message for 1/0 input
        finally:
            self.update_current_label()

    """
    Creating Equals & All Clear (AC) button
    """
    def create_clear_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="AC",
            bg=off_white,
            fg=Blue,
            font=Symbol_font,
            borderwidth=0,
            command=self.clear
        )

        button.grid(
            row=0,
            column=1,
            sticky=tk.NSEW
        )

    def create_equals_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="=",
            bg=Light_Blue,
            fg=Blue,
            font=Symbol_font,
            borderwidth=0,
            command=self.evaluate
        )

        button.grid(
            row=4, # Last row
            column=3,
            columnspan=2,  #buttons as big as or spans for 2 columns
            sticky=tk.NSEW
        )

    """
    Similarly creating Square & SQUARE ROOT buttons and their functionality
    """
    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_current_label()

    def create_square_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="x\u00b2", # Unicode for square
            bg=off_white,
            fg=Blue,
            font=Symbol_font,
            borderwidth=0,
            command=self.square
        )

        button.grid(
            row=0,
            column=2,
            sticky=tk.NSEW
        )

    def square_root(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_current_label()

    def create_square_root_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="\u221ax", # Unicode for square root
            bg=off_white,
            fg=Blue,
            font=Symbol_font,
            borderwidth=0,
            command=self.square_root
        )

        button.grid(
            row=0,
            column=3,
            sticky=tk.NSEW
        )
    

    # Executes the code
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
