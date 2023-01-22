import pandas as pd
from openpyxl import load_workbook
from datetime import datetime



def initial_processing():
    candidates = pd.read_excel('wordle_doc.xlsx',sheet_name='All Guess Candidates')
    used = pd.read_excel('wordle_doc.xlsx',sheet_name='Past Words')
    # c = candidates["Guess Candidates"]
    # print('c: ', str(c))
    c = candidates["Guess Candidates"].apply(lambda x: x.lower()) # when i get rid of the x.lower(), my code stops working
    p = used["Past Words"].apply(lambda x: x.lower())
    working_list = pd.concat([c,p]).drop_duplicates(keep=False)
    return working_list

# Adds today's word to list of used words
def store_latest(word):
    wb = load_workbook('wordle_doc2.xlsx')
    ws = wb['Past Words']
    mr = ws.max_row
    last_word_of_day = ws.cell(row=mr, column=1).value
    if last_word_of_day.lower() != word.lower():
        ws.cell(row=mr+1, column=1).value = word.upper()
        wb.save('wordle_doc2.xlsx')

def add_word_path(guesses):
    wb = load_workbook('wordle_doc2.xlsx')
    ws = wb['Guessing Path']
    mr = ws.max_row
    last_date = str(ws.cell(row=mr, column=1).value)[:10]
    print('last date: ',last_date)
    print('Guesses:')
    row_index = mr
    col_index = 1
    today = datetime.today().strftime('%Y-%m-%d')
    if today != last_date:
        row_index += 1
        ws.cell(row=row_index, column=col_index).value = today
        col_index +=1
        for g in guesses:
            ws.cell(row=row_index, column=col_index).value = g
            col_index+=1
    # for g in guesses:
    #     print(g)

    # print('last date: ',last_date)
    # print('today: ', today)
    # print('last date: ',str(len(last_date))[:-1])
    # print('today date: ',str(len(today))[:-1])
    print('last date == today: ', last_date==today)

    # if last_word_of_day.lower() != word.lower():
    #     print('entered if')
    #     ws.cell(row=mr+1, column=1).value = word.upper()
    wb.save('wordle_doc2.xlsx')

# should probably keep running list of words guessed
    pass
