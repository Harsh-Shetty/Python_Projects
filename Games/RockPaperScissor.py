from random import choice

print(
    "Let's play ROCK, PAPER & SCISSORS. The one who scores 3 points/victories will win the game."
)
print("")

player_wins = 0
computer_wins = 0

computer = choice(["r", "s", "p"])

player = False

while computer_wins < 4 or player_wins < 4:

    player = input("'r' for ROCK, 'p' for PAPER, 's' for SCISSOR: ")

    if player == computer:
        print("I picked " + computer)
        print("That's a tie! again!")
    elif player == "r":
        if computer == "p":
            print("I picked " + computer)
            print("You lose! Computer gets the point")
            computer_wins += 1
        else:
            print("I picked " + computer)
            print("You win!")
            player_wins += 1
    elif player == "p":
        if computer == "s":
            print("I picked " + computer)
            print("You lose. Computer gets the point!")
            computer_wins += 1
        else:
            print("I picked " + computer)
            print("You win")
            player_wins += 1
    elif player == "s":
        if computer == "r":
            print("I picked " + computer)
            print("You lose! Computer gets the point")
            computer_wins += 1
        else:
            print("I picked " + computer)
            print("You win!")
            player_wins += 1
    else:
        print("Thats not a valid input! Check your spelling!")

    player = False
    computer = choice(["r", "s", "p"])

    print("")
    print("Player points: ", player_wins)
    print("Computer points: ", computer_wins)
    print("")

    if player_wins == 3:
        print("Well done, you WIN the game!")
        break
    if computer_wins == 3:
        print("I got 3 points. You LOSE the game. Better luck next time!")
        break
