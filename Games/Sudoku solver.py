# puzzle is a List of Lists
# eg: [ [3,9,-1  -1,5,-1  -1,-1,1],
#       [-1,5,-1  2,-1,-1 -1,-1,5],
#       
#       [-1,5,-1 -1,6,8   -1,-1,4],
#       [2,-1,6  -1,-1,3  -1,-1,-1] ]
# Abv is a 9x4 square. -1 represents blank space. We will make a
# similar 9x9 square.
import time
from pprint import pprint

def find_next_empty(puzzle):
    #finds & returns empty cell(-1)
    # indices range from 0-8
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c
    return None, None # if all filled

def is_valid(puzzle, guess, row, col):
    #checks the num is not repeated horizontally & vertically i.e row & col
    #returns True if valid move (i.e num not alredy present in row & col)
    # othrwise False
    row_vals = puzzle[row]
    if guess in row_vals:
        return False
    # we are not aware of indices of col as it is only given to row when
    # it is created. There4, we associated the index [i] to col.
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False
    # for the 3x3 squres in the puzzle. Iterate 3 times (as the sq is 9x9).
    # Up to down for rows. Left to right for cols
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
           if puzzle[r][c] == guess:
               return False
    return True

start= time.time()

def solve_sudoku(puzzle):
    #returns whether a soln exists
    #Step 1: choose empty cell on the puzzle to make a guess
    row, col = find_next_empty(puzzle)
    #Step 1.1: If all filled we r done
    if row is None:
        return True #if all row filled (None) then that means all cols r also filled
    #Step 2: If an empty cell exists, we give an input from 1-9
    for guess in range(1, 10): #1,2,3,....,8,9
        if is_valid(puzzle, guess, row, col):         #check if guess valid
            puzzle[row][col] = guess                 #assign valid VALUE
            if solve_sudoku(puzzle):
                return True
        # if not valid or if guess didn't solve the puzzle
        # New num must be tried
        puzzle[row][col] = -1 #reset the blank space as guess didn't work
    # If all gusses fail then the puzzle is unsolvable
    return False

if __name__ == '__main__':
    example_board = [
        [3, -1, -1,   -1, 5, 7,   -1, 9, -1],
        [-1, -1, 4,   -1, 6, 3,   7, -1, -1],
        [-1, -1, 1,   2, 8, 4,   -1, 3, -1],

        [-1, 2, -1,   -1, 9, 1,   -1, -1, 4],
        [-1, -1, 9,   -1, -1, -1,   1, -1, -1],
        [6, -1, -1,   3, 4, -1,   -1, 7, -1],

        [-1, 4, -1,   6, 2, 5,   8, -1, -1],
        [-1, -1, 8,   7, 1, -1,   2, -1, -1],
        [-1, 7, -1,   4, 3, -1,   -1, -1, 9]
    ]
    print(solve_sudoku(example_board))
    pprint(example_board)
    end= time.time()
    print("Solved in: ", end-start, "seconds")