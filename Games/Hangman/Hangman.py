import random
import string
from words import words
from hangman_visual import lives_visual_dict

def get_valid_word(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()

def hangman():
    word = get_valid_word(words)
    word_letters=set(word)                  #creates a set of letters from the selected word 
    alphabet= set(string.ascii_uppercase)
    used_letters=set()                    #set of letters the player has already gussed 
    lives=13
    while len(word_letters)>0 and lives>0:              #loop to exhaust the set of word letters
        
        print ('You have used: ', ' '.join(used_letters), 'Lives left: ', lives) #to show the used letters in terminal
        word_list =[letter if letter in used_letters else '-' for letter in word]
        print(lives_visual_dict[lives])
        print ('Current word: ', ' '.join(word_list))

        user_letter= input('Guess a letter: ').upper() #gets user input
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                 lives -=1
                 print('Letter not in word')
        
        elif user_letter in used_letters:
            print ("\nYou've already used that letter. Try again.")
            
        else:
            print ("\nInvalid character")
    if lives==0:
        print(lives_visual_dict[lives])
        print ('You DIED. The word was: ', word)
    else:
        print('You guessed the word: ', word, '!!')


hangman()