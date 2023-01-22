import time
from playwright.sync_api import sync_playwright
import pandas as pd
from website_handling import *
from game_logic import *
from data_processing import *
import random
import openpyxl

random.seed(0)
KEYBOARD_ROW1 = 'QWERTYUIOP'
KEYBOARD_ROW2 = 'ASDFGHJKL'
KEYBOARD_ROW3 = '0ZXCVBNM0'
KEYBOARD_ROWS = [KEYBOARD_ROW1,KEYBOARD_ROW2,KEYBOARD_ROW3]


# Can configure these settings in the "Config" sheet of wordle_doc.xlsx.

settings = pd.read_excel('wordle_doc.xlsx', sheet_name='Config')
display_graphics = settings['Selection'][0]
has_been_run = settings['Selection'][1]
starting_word = settings['Selection'][2]
display_num_left = settings['Selection'][3]
display_words_left = settings['Selection'][4]
display_guesses = settings['Selection'][5]
display_wotd = settings['Selection'][6]
display_victory = settings['Selection'][7]


guessable = initial_processing(has_been_run)

with sync_playwright() as p:
    page = start_game(p, display_graphics)
    guess_num = 0
    word = starting_word
    guesses = [word]
    guess = take_a_guess(word, KEYBOARD_ROWS, page, guess_num)
    guessable = handle_hints(guess, guessable)
    guess_num+=1

    won = you_win(guess)

    while (not won) and guess_num < 6:
        if display_guesses:
            print('guess: ', word)
        if display_num_left:
            print('number of words left: ', str(len(guessable)))
        if display_words_left:
            print('remaining words:\n', guessable.to_string(index=False))

        word = random.choice(guessable.tolist())
        guesses.append(word)
        guess = take_a_guess(word, KEYBOARD_ROWS, page, guess_num)
        guessable = handle_hints(guess, guessable)
        guess_num+=1
        won = you_win(guess)
    if display_wotd:
        print('The word of the day is: ', word)
    if display_victory:
        print("You won in ", str(guess_num), ' guesses!')

    if not has_been_run:
        update_records(word,guesses)

    page.close()




    # it doesn't appear that there's a way to get the word of the day if you get all the words wrong.
    # keep running list of word of the day and don't guess those words
    # could start w/ raise or from a list of words like 'raise' and 'crane' and randomly pick one

    # idea: import a corpus from famous book(s) and get word counts. rank words in order of highest word counts to find most common words
    # then search the remaining list for the top word, if it's there, guess that word, if not, go to the next word

    # maybe build in some logic so that it's less likely to guess a word if it has 2 of the same letters right next to each other.