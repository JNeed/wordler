import pandas as pd


s = pd.Series(['alabama', 'ohio','connecticut'])

guess = 'ache'

for letter in guess:
    print(s.apply(lambda x: letter in x))