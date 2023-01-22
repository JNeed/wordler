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

    # test = ser.apply(lambda x: 'a' in x) failed; i wonder if the problem was that the words False and True were in there
    yellow1 = ser.apply(lambda x: letter in str(x))
    ser = ser[yellow1]
    yellow2 = ser.apply(lambda x: letter != str(x)[letter_index])
    return ser[yellow2]

def handle_black(letter, ser):
    black = ser.apply(lambda x: letter not in str(x))
    return ser[black]

def handle_hints(zipped, ser):
    # need to figure out a way to make this work
    # each subsequent widdling depends on the last
    letter_index = 0
    new_ser = ser
    for letter, hint in zipped:
        if hint == 'correct':
            new_ser = handle_green(letter,letter_index, new_ser)
        elif hint == 'present':
            new_ser = handle_yellow(letter, letter_index, new_ser)
        elif hint == 'absent':
            new_ser = handle_black(letter, new_ser)
        else:
            print('something went wrong in elliminate candidates')
        letter_index += 1
    return new_ser

def you_win(zipped):
    for k, v in zipped:
        if v != 'correct':
            return False
    return True