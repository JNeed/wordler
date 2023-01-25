import pandas as pd
def get_hints(page,row):
    ls = []
    for i in range(1,6):
        ls.append(page.locator('//*[@id="wordle-app-game"]/div[1]/div/div[' + str(row) + ']/div[' + str(i) + ']/div').get_attribute('data-state'))
    return ls

def handle_green(letter, letter_index, ser):
    green = ser.apply(lambda x: letter == str(x)[letter_index])
    return ser[green]
def handle_yellow(letter, letter_index, ser):
    yellow1 = ser.apply(lambda x: letter in str(x))
    ser = ser[yellow1]
    yellow2 = ser.apply(lambda x: letter != str(x)[letter_index])
    return ser[yellow2]

def handle_black(letter, letter_index, word, zipped, ser):
    black = ser.apply(lambda x: letter not in str(x))
    if len(set(word)) == len(word): # if there are no dup letters in guess
        return ser[black]
    hints = pd.Series()
    for i,z in enumerate(zipped):
        if z[0] == letter:
            hints.at[i]=z[1]
    if any(hints=='present') or any(hints =='correct'):
        neq = ser.apply(lambda x: letter != str(x)[letter_index])
        return ser[neq]
    elif all(hints == 'absent'): # if there are dup letters in guess but both are black
        ser[black]
    else:
        print('Something went wrong in game_logic.py handle_black.')
    return ser

def handle_hints(word,zipped, ser):
    letter_index = 0
    new_ser = ser
    for letter, hint in zipped:
        if hint == 'correct':
            new_ser = handle_green(letter,letter_index, new_ser)
        elif hint == 'present':
            new_ser = handle_yellow(letter, letter_index, new_ser)
        elif hint == 'absent':
            new_ser = handle_black(letter, letter_index, word, zipped, new_ser)
        else:
            print('something went wrong in elliminate candidates')
        letter_index += 1
    return new_ser

def you_win(zipped):
    for k, v in zipped:
        if v != 'correct':
            return False
    return True