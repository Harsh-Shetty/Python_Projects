import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size= dim_size
        self.num_bombs = num_bombs #numbr of bombs
        self.board = self.make_new_board()
        self.assign_val_board() #assigns vals to empty spaces to help us
        #identify how many bombs r present in the neighbourhood
        self.dug = set()
    
    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # abv line creates a array like this:
        #[[None, None, ...., None],
        # [None, None, ...., None],
        # [...., ...., ...., ....],
        # [...., ...., ...., ....],
        # [None, None, ...., None]]
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc= random.randint(0, self.dim_size**2 - 1) #selects random location for the bomb
            # getting the indices of the randomly selected location (row, column)
            row = loc // self.dim_size
            col = loc % self.dim_size
            # * = bomb in printed board
            if board[row][col] == '*':
                continue #bomb already planted so we continue ahead

            board[row][col] = '*' #BOMB HAS BEEN PLANTED
            bombs_planted += 1

        return board
    
    def assign_val_board (self):
        for r in range (self.dim_size):
            for c in range (self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r, c)
    
    def get_num_neighbouring_bombs(self, row, col):
        num_neighbouring_bombs = 0
        # OG code: "for c in range (col-1, (col+1) +1)" checks left $ right
        # cols. +1 in the end is convention.
        # Same for row which checks abv and below.
        # MIN & MAX addedd to  give bounds. So that outside the board is
        # not checked. 
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    continue # OG loctio. Don't check
                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1
        return num_neighbouring_bombs
    
    def dig(self, row, col):
        #return True for successful dig. False if bomb dug.
        self.dug.add((row, col)) #keep track of locations dug 
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0: #more than 0 neighbouring bombs
            return True 
        # for self.board [row] [col] == 0 i.e NO neighbouring bombs 
        # Same row & col check as in get_num_neighbouring_bombs
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue  #already dug
                self.dig(r,c) #continue digging
        return True
    
    def __str__(self):
        # prints a string that shows the board
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # gives array. Same as line 13
        for row in range (self.dim_size):
            for col in range (self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col]= ' '
        # printing the board
        str_rep = ''
        #get max col widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key = len)))
        # print the csv strings
        indices = [i for i in range (self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        for i in range(len(visible_board)):
            row = visible_board[i]
            str_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            str_rep += ' |'.join(cells)
            str_rep += ' |\n'
        
        str_len = int(len(str_rep) / self.dim_size)
        str_rep = indices_row + '-'*str_len + '\n' + str_rep + '-'*str_len
        
        return str_rep


def play(dim_size=10, num_bombs=10):
    # Create board and plant bombs
    board = Board (dim_size, num_bombs) #goes through Class Board
    # and  creates the board
    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        # example of usr input: 0(Row), 3 (Col)
        # After split the ,--> Detect comma
        #(\\s))--> Detect whitespace
        # * indicates 0 or more of those abv (comma or whitespace)
        # Thus 0 or more , & whitespace will be splitted. Thus inputs
        # like 0,0 or 0,,3 or 0 0 or 1, 5 or 5,   ,  8 will be accepted.
        row, col = int(user_input[0]), int(user_input[-1])
        # Out of bounds condition
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print ("Invalid Location. Try Again.")
            continue
        # if it's valid then Dig.
        safe = board.dig(row, col)
        if not safe:
            # we've dug a bomb. Game Over. Loop(game) ends
            break
    if safe:
        print ("Congrats!! You have WON!") # no empty space left
    else:
        print ("Sorry Game Over")  # Bomb Dug
        # revealing Board
        board.dug=[(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print (board)

if __name__ == '__main__':
    play()