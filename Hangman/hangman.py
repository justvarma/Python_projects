import random
from words import words
import string

def get_valid_word(words):
    word = random.choice(words).upper()
    while '-' in word or ' ' in word:
        word = random.choice(words).upper()
    return word

def hangman():
    word = get_valid_word(words)
    word_letters = set(word)  
    alphabet = set(string.ascii_uppercase)
    used_letters = set()
    lives = 6

    while len(word_letters) > 0 and lives > 0:
        print(f"\nYou have {lives} lives left. Used letters: {', '.join(used_letters) if used_letters else 'None'}")
        word_list = [letter if letter in used_letters else '_' for letter in word]
        print(f"Current word: {' '.join(word_list)}")

        user_letter = input('Guess a letter: ').upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives -= 1
                print('Letter is not in the word.')    
        elif user_letter in used_letters:
            print("You have already used that character. Please try again.")
        else:
            print("Invalid character. Please try again.")

    if lives == 0:
        print(f"\nYou lost! The word was: {word}\n")
    else:
        print(f"\n🎉 Congratulations! You guessed the word: {word} 🎉\n")

hangman()