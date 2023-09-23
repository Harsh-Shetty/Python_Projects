import math
import time
from TTT_player import HumanPlayer, ComputerPlayer

class TicTacToe():
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i*3:(i+1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_numbers():
        # gives indices for each row eg: 0| 1| 2
        number_board=[[str(i) for i in range(j*3, (j+1)*3)]for j in range (3)]
        for row in number_board:
            print('| ' + ' | '.join(row)+' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def avaliable_moves(self):
        moves=[]
        # below line gives a Tuple ['x','x','0']-> [(Indice=0, 'x'),(1, 'x'),(2, '0')]
        for (i,spot) in enumerate(self.board):
            if spot == ' ':
                moves.append(i)
        return moves
    
    def empty_squares(self):
        return ' ' in self.board
    
    def num_empty_squares(self):
        return len(self.avaliable_moves())
    
    def winner(self, square, letter):
        row_ind = math.floor(square / 3)
        row = self.board[row_ind*3 : (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True 
        
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range (3)]
        if all([spot == letter for spot in column]):
            return True

        if square % 2 == 0:
            diagonal_1 = [self.board[i] for i in [0, 4, 8]] #Top left, middle,  bottom right
            if all([spot == letter for spot in diagonal_1]):
                return True
            diagonal_2 = [self.board[i] for i in [2, 4, 6]] #Top right, middle,  bottom left
            if  all([spot == letter for spot in diagonal_2]):
                return True
        return False

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_numbers()
    
    letter= 'X'

    while game.empty_squares():
        if letter =='O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        
        #function to make move
        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('') #empty line
        
            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter #retrns the winning letter

            letter='O' if letter == 'X' else 'X'  #after move is made. Alterate letters
        
        time.sleep(1)                   #time delay for computer move

    if print_game:
        print('It\'s a tie!!!')

if __name__== '__main__':
    x_player = HumanPlayer('X')
    o_player = ComputerPlayer('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)