import tkinter as tk
import colours as c
import random


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")

        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=3, width=600, height=600)
        self.main_grid.grid(pady=(100, 0))
        self.make_GUI()  # GUI initialization
        self.start_game()  # initializing game

        # Initializing Keyboard binds
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        # makes the code run infinetely until user termination
        self.mainloop()

    # make grid
    def make_GUI(self):
        self.cells = []  # holds information of each CELL in the GRID
        for i in range(4):
            #  ROW by ROW APPENDING the CELLS (above)
            row = []
            for j in range(4):
                # FRAME for each CELL
                cell_frame = tk.Frame(
                    self.main_grid, bg=c.EMPTY_CELL_COLOR, width=150, height=150
                )
                # PADDING (spacing) to visualise grid lines between the CELLS
                cell_frame.grid(
                    row=i, column=j, padx=5, pady=5
                )  # apt placement of grids
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        # make SCOREBOARD
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tk.Label(score_frame, text="Score", font=c.SCORE_LABEL_FONT).grid(
            row=0
        )  # row=0 positions the LABEL at the top
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)  # places right belos score_label

    def start_game(self):
        # CReate matrix of zeros
        self.matrix = [[0] * 4 for _ in range(4)]

        # fill 2 random cells with 2s
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        # colour for 2 numbered cell.
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2",
        )
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        # colour for 2 numbered cell.
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2",
        )

        self.score = 0  #  score set to 0

    """
    Stack will compress all numbers in the matrix towards one side of
    the board eliminating all the gaps of empty cells between them. We'll write
    our stack function to compress to the left side.
    """

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0  # keeps track of filled cells
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    # adds horizontally adjacent tiles
    def combine(self):
        for i in range(4):
            for j in range(3):
                if (
                    self.matrix[i][j] != 0
                    and self.matrix[i][j] == self.matrix[i][j + 1]
                ):
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    """
    Flips the logic of matrix. So stack function which compresses to the left side
    can be used for RIGHT SWIPE as well.
    """

    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix

    """
    Flips the matrix over its diagonal. Used with stack for compressing up.
    When used with reverse it compresses down.
    """

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    # Add new tile
    def add_new_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])

    # Update GUI to match the matrix
    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.CELL_NUMBER_COLORS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value),
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    # Check if any moves possible
    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    # Check if Game over
    def game_over(self):
        if any(2048 in row for row in self.matrix):
            # New Frame for game over. Inheriting from main_grid
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            # Placing this FRAME over main_grid
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="You Win!!",
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT,
            ).pack()  # pack to display it on the game
        # Lose condition: No EMPTY CELL left
        elif (
            not any(0 in row for row in self.matrix)
            and not self.horizontal_move_exists()
            and not self.vertical_move_exists()
        ):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            # Placing this FRAME over main_grid
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="GAME OVER",
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                fon=c.GAME_OVER_FONT,
            ).pack()

    def left(self, event):
        self.stack()  # Compresses filled cells to the left side
        self.combine()  # Adds horizontally adjacent cell numbers
        self.stack()  # Eliminates newly created Empty CELLS

        self.add_new_tile()
        self.update_GUI()
        self.game_over()  # checks if GAME OVER conditions are being met

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()

        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()

        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()

        self.add_new_tile()
        self.update_GUI()
        self.game_over()


if __name__ == "__main__":
    Game()
