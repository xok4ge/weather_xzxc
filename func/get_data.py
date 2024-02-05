import datetime as dt
import pandas as pd
from pathlib import Path as pth
from timeit import default_timer as timer

head = ['Синоптический индекс станции', 'Год по Гринвичу', 'Месяц по Гринвичу',
        'День по Гринвичу', 'Срок по Гринвичу', 'Общее количество облачности', 'Погода между сроками',
        'Направление ветра', 'Средняя скорость ветра', 'Максимальная скорость ветра',
        'Сумма осадков за период между сроками', 'Относительная влажность воздуха',
        'Температура воздуха по сухому термометру', 'Атмосферное давление на уровне станции']


pd.set_option('display.max_columns', None)


def get_data_clbk(filename, date=False):
    start = timer()
    path = pth.cwd().joinpath('../data')
    for dir in path.iterdir():
        if dir.is_dir():
            if f'{filename}.csv' in [x.name for x in dir.iterdir()]:
                df = pd.read_csv(dir.joinpath(f'{filename}.csv'), engine='pyarrow')
                if date:
                    min_val = df.iloc[0][['Год по Гринвичу', 'Месяц по Гринвичу', 'День по Гринвичу']]
                    max_val = df.iloc[-1][['Год по Гринвичу', 'Месяц по Гринвичу', 'День по Гринвичу']]
                    return [list(map(int, min_val)), list(map(int, max_val))]
                return df


def get_render(df, date, pt):
    if pt == 'day':
        rendata = df[(df['Год по Гринвичу'] == date[0]) & (df['Месяц по Гринвичу'] == date[1])
                 & (df['День по Гринвичу'] == date[2])]
        return rendata
    else:
        # try:
        cloud, wth, avw, maxw, prec, hum, temp, atm = [], [], [], [], [], [], [], []
        syn = ''
        for x in range(7):
            datex = list(map(int, str(dt.datetime(*date).date()+dt.timedelta(days=x)).split('-')))
            dxfrm = df.loc[(df['Год по Гринвичу'] == datex[0]) & (df['Месяц по Гринвичу'] == datex[1])
                 & (df['День по Гринвичу'] == datex[2])]
            #---------------------------------------------------
            syn = int(list(dxfrm['Синоптический индекс станции'])[0])
            cloud.append(sorted(list(dxfrm['Общее количество облачности']),
                                key=lambda x: list(dxfrm['Общее количество облачности']).count(x))[-1])
            wth.append(sorted(list(dxfrm['Погода между сроками']),
                                key=lambda x: list(dxfrm['Погода между сроками']).count(x))[-1])
            avw.append(round(sum(list(dxfrm['Средняя скорость ветра']))/len(dxfrm['Средняя скорость ветра']), 1))
            prec.append(round(sum(list(dxfrm['Сумма осадков за период между сроками'])), 1))
            hum.append(round(sum(list(dxfrm['Относительная влажность воздуха']))/len(dxfrm['Относительная влажность воздуха'])))
            temp.append(round(sum(list(dxfrm['Температура воздуха по сухому термометру']))
                             / len(dxfrm['Температура воздуха по сухому термометру']), 1))
            atm.append((round(sum(list(dxfrm['Атмосферное давление на уровне станции']))
                             / len(dxfrm['Атмосферное давление на уровне станции']))))
            maxw.append(max(list(dxfrm['Максимальная скорость ветра'])))
        df_data = {'Синоптический индекс станции': syn,
                   'Срок по Гринвичу': [1, 2, 3, 4, 5, 6, 7],
                   'Общее количество облачности': cloud,
                   'Погода между сроками': wth,
                   'Средняя скорость ветра': avw,
                   'Максимальная скорость ветра': maxw,
                   'Сумма осадков за период между сроками': prec,
                   'Относительная влажность воздуха': hum,
                   'Температура воздуха по сухому термометру': temp,
                   'Атмосферное давление на уровне станции': atm}
        rendata=pd.DataFrame(df_data)
        return rendata
        # excepr Exception as e:

# мои красные ожоги так идут тебе к лицу
# и я знаю все загоны, и я знаю наизусть тебя всю
# прочитал как книгу с головы до ног
# через несколько мгновений начинаем наш полет
