import math
import random


class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + "'s turn. Input move (0-8): ")
            try:
                val = int(square)
                if val not in game.avaliable_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid square. Try again.")
        return val


class ComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.avaliable_moves()) == 9:
            square = random.choice(game.avaliable_moves())
        else:
            square = self.minmax(game, self.letter)["position"]
        return square

    def minmax(self, state, player):
        max_player = self.letter  # human
        other_player = "O" if player == "X" else "X"
        if state.current_winner == other_player:
            return {
                "position": None,
                "score": 1 * (state.num_empty_squares() + 1)
                if other_player == max_player
                else -1 * (state.num_empty_squares() + 1),
            }
        elif not state.empty_squares():  # no empty square
            return {"positon": None, "score": 0}

        if player == max_player:
            # maximize human. Player has to score abv -infinity
            best = {"position": None, "score": -math.inf}
        else:
            # minimize computer player. Min number of steps to win
            best = {"position": None, "score": math.inf}
        for possible_move in state.avaliable_moves():
            # Step 1: Make move
            state.make_move(possible_move, player)
            # Step 2: Recurse minmax to simulate game after making move
            sim_score = self.minmax(state, other_player)
            # Step 3: Undo the move
            state.board[possible_move] = " "
            state.current_winner = None
            sim_score["position"] = possible_move
            # Step 4: update  dicts if necessary
            if player == max_player:
                if sim_score["score"] > best["score"]:
                    best = sim_score  # replace best
            else:
                if sim_score["score"] < best["score"]:
                    best = sim_score  # replce best with min number of moves
        return best
