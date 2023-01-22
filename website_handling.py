import time
from playwright.sync_api import sync_playwright
from game_logic import *


def zipem(word,hints):
    return list(zip(word,hints))

# Return tuple with row num and key position of a letter
def get_key_pos(letter,keyboard_rows):
    if letter in keyboard_rows[0]:
        return (1, keyboard_rows[0].index(letter) + 1)
    elif letter in keyboard_rows[1]:
        return (2, keyboard_rows[1].index(letter) + 1)
    elif letter in keyboard_rows[2]:
        return (3, keyboard_rows[2].index(letter) + 1)
    elif letter == '1': # we'll just let 1 indicate the enter key
        return(3,1)
    else:
        print("something went wrong")
    
def generate_locator(row_num,key_num):
    return '//*[@id="wordle-app-game"]/div[2]/div[' + str(row_num) + ']/button[' + str(key_num) + ']'

def type_key(letter,keyboard_rows,page):
    row, pos = get_key_pos(letter,keyboard_rows)
    loc = generate_locator(row,pos)
    page.locator(loc).click()

def take_a_guess(word,keyboard_rows,page,guess_num):
    word = word.upper()
    for letter in word:
        type_key(letter,keyboard_rows,page)
    type_key('1',keyboard_rows,page)
    time.sleep(2.3)
    hints = get_hints(page,guess_num + 1)
    return zipem(word,hints)

def start_game(p,display_graphics):
    browser = ''
    if display_graphics:
        browser = p.chromium.launch(headless=False)
    elif not display_graphics:
        browser = p.chromium.launch()
    else:
        print('malfunction in website_handling.py: start_game()')
    # browser = p.chromium.launch(headless=False)
    page = browser.new_context().new_page()
    page.goto("https://www.nytimes.com/games/wordle/index.html")
    page.click('body > div > div > dialog > div > button > svg')
    return page
