from datetime import datetime, date
import pandas as pd
import sys


def f(sequence):
    value = 2
    for i in sequence:
        yield i + 1


g = f(range(3))

pdf = pd.DataFrame([1, 2, 3])
pdf.to_csv('./aaaaa.csv', index=False)

CONST = "./bbbbb/"
ymd = "20221111"

pdf.to_csv(CONST + 'aaaaa.csv')

pdf.to_csv(CONST + 'aaaaa' + ymd + '.csv')

pdf.to_csv(f'aaaaa{ymd}.csv')


path = CONST + 'aaaaa.csv'
pdf.to_csv(path)

path = CONST + f'aaaaa{ymd}.csv'
pdf.to_csv(path)

path = CONST + 'aaaaa{ymd}.csv'.format(ymd=ymd)
pdf.to_csv(path)

pdf.to_csv('aaaaa{ymd}.csv'.format(ymd=ymdymd))

pdf.to_csv('aaaaa.csv' + date(2022, 10, 1).strftime('%Y%m%d'))

'a/a/a'.split('/')
