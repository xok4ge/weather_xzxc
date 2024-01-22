import sys
import pandas as pd
from pathlib import Path as pth
from timeit import default_timer as timer
from db import *


head = ['Синоптический индекс станции', 'Год по Гринвичу', 'Месяц по Гринвичу',
        'День по Гринвичу', 'Срок по Гринвичу', 'Общее количество облачности', 'Погода между сроками',
        'Направление ветра', 'Средняя скорость ветра', 'Максимальная скорость ветра',
        'Сумма осадков за период между сроками', 'Относительная влажность воздуха',
        'Температура воздуха по сухому термометру', 'Атмосферное давление на уровне станции']

pd.set_option('display.max_columns', None)


def get_data_clbk(filename, date=False):
    start = timer()
    path = pth.cwd().joinpath('data')
    for dir in path.iterdir():
        if dir.is_dir():
            if f'{filename}.csv' in [x.name for x in dir.iterdir()]:
                df = pd.read_csv(dir.joinpath(f'{filename}.csv'), engine='pyarrow')
                if date:
                    min_val = df.iloc[0][['Год по Гринвичу', 'Месяц по Гринвичу', 'День по Гринвичу']]
                    max_val = df.iloc[-1][['Год по Гринвичу', 'Месяц по Гринвичу', 'День по Гринвичу']]
                    return [list(map(int, min_val)), list(map(int, max_val))]
                return df

def get_render(df, date):
    rendata = df[(df['Год по Гринвичу'] == date[0]) & (df['Месяц по Гринвичу'] == date[1])
             & (df['День по Гринвичу'] == date[2])]
    return rendata


    # df = pd.read_csv('data1/30469.csv')
    # pd.set_option('display.max_columns', None)
    # start = timer()

# мои красные ожоги так идут тебе к лицу
# и я знаю все загоны, и я знаю наизусть тебя всю
# прочитал как книгу с головы до ног
# через несколько мгновений начинаем наш полет
