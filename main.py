import time
from playwright.sync_api import sync_playwright
import pandas as pd
from website_handling import *
from game_logic import *
from data_processing import *
import random
import openpyxl

random.seed(0)

KEYBOARD_ROW1 = 'qwertyuiop'
KEYBOARD_ROW2 = 'asdfghjkl'
KEYBOARD_ROW3 = '0zxcvbnm0'
KEYBOARD_ROWS = [KEYBOARD_ROW1,KEYBOARD_ROW2,KEYBOARD_ROW3]

guessable = initial_processing()

with sync_playwright() as p:
    page = start_game(p)
    guess_num = 0
    word = 'RAISE'
    guesses = [word]
    guess = take_a_guess(word, KEYBOARD_ROWS, page, guess_num)
    guessable = handle_hints(guess, guessable)
    guess_num+=1

    won = you_win(guess)

    while (not won) and guess_num < 6:
        print('guess: ', word)
        print('number of words left: ', str(len(guessable)))
        print('remaining words: ', guessable)

        word = random.choice(guessable.tolist())
        guesses.append(word)
        guess = take_a_guess(word, KEYBOARD_ROWS, page, guess_num)
        guessable = handle_hints(guess, guessable)
        guess_num+=1
        won = you_win(guess)
    print("You won in ", str(guess_num), ' guesses!')
    store_latest(word)
    add_word_path(guesses)
    page.close()




    # it doesn't appear that there's a way to get the word of the day if you get all the words wrong.
    # keep running list of word of the day and don't guess those words
    # could start w/ raise or from a list of words like 'raise' and 'crane' and randomly pick one
    # keep a count of guesses and start it at 1 (because i start w/ raise)
    # row number will be equal to guess number

    # Check if when you lose, it reveals the word for that day and how you grab that element

    # idea: import a corpus from famous book(s) and get word counts. rank words in order of highest word counts to find most common words
    # then search the remaining list for the top word, if it's there, guess that word, if not, go to the next word

    # maybe build in some logic so that it's less likely to guess a word if it has 2 of the same letters right next to each other.