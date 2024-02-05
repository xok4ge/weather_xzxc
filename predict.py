import pandas as pd
import numpy as np
import os
import time
from sklearn.linear_model import RANSACRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import joblib
import csv
from timeit import default_timer as timer

def migrated_pand():
    head = ['Синоптический индекс станции', 'Год по Гринвичу', 'Месяц по Гринвичу', 'День по Гринвичу',
            'Срок по Гринвичу', 'Год источника (местный)', 'Месяц источника (местный)', 'День источника (местный)',
            'Срок источника', 'Номер срока в сутках по поясному декретному зимнему времени (ПДЗВ)', 'Время местное',
            'Номер часового пояса', 'Начало метеорологических суток по ПДЗВ', 'Горизонтальная видимость',
            'Признак качества', 'Признак наличия знака «>»', 'Общее количество облачности', 'Признак качества0',
            'Количество облачности нижнего яруса', 'Признак качества1', 'Форма облаков верхнего яруса',
            'Признак качества2', 'Форма облаков среднего яруса', 'Признак качества3',
            'Форма облаков вертикального развития', 'Признак качества4', 'Слоистые и слоисто-кучевые облака',
            'Признак качества5', 'Слоисто-дождевые, разорвано-дождевые облака', 'Признак качества6',
            'Высота нижней границы облачности', 'Признак качества7',
            'Признак способа определения высоты нижней границы облачности',
            'Признак наличия облачности ниже уровня станции', 'Признак качества8', 'Погода между сроками',
            'Признак качества9', 'Погода в срок наблюдения', 'Признак качества10', 'Направление ветра',
            'Признак качества11', 'Средняя скорость ветра', 'Признак качества12', 'Признак наличия знака «>»13',
            'Максимальная скорость ветра', 'Признак качества14', 'Признак наличия знака «>»15',
            'Сумма осадков за период между сроками', 'Признак качества16', 'Температура поверхности почвы',
            'Признак качества17', 'Минимальная температура поверхности почвы', 'Признак качества18',
            'Минимальная температура поверхности почвы между сроками', 'Признак качества19',
            'Максимальная температура поверхности почвы между сроками', 'Признак качества20',
            'Температура поверхности почвы по максимальному термометру после встряхивания', 'Признак качества21',
            'Температура воздуха по сухому термометру', 'Признак качества22',
            'Температура воздуха по смоченному термометру', 'Признак качества23', 'Признак наличия льда на батисте',
            'Температура воздуха по спирту минимального термометра', 'Признак качества24',
            'Минимальная температура воздуха между сроками', 'Признак качества25',
            'Максимальная температура воздуха между сроками', 'Признак качества26',
            'Температура воздуха по максимальному термометру после встряхивания', 'Признак качества27',
            'Парциальное давление водяного пара', 'Признак качества28', 'Указатель точности измерения элемента',
            'Относительная влажность воздуха', 'Признак качества29', 'Дефицит насыщения водяного пара',
            'Признак качества30', 'Указатель точности измерения элемента31', 'Температура точки росы',
            'Признак качества32', 'Атмосферное давление на уровне станции', 'Признак качества33',
            'Атмосферное давление на уровне моря', 'Признак качества34', 'Характеристика барической тенденции',
            'Признак качества35', 'Величина барической тенденции', 'Признак качества36']
    k = [5, 4, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 4, 1, 1, 2, 1, 2, 1,
         2, 1, 3, 1, 2, 1, 1, 2, 1, 1, 6, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1,
         1, 3, 1, 7, 1, 1, 5, 1, 6, 1, 6, 1, 2, 1, 4, 1]

    path = 'C:\\python\\GitHub\\predprof\\data\\Srok8c'  # путь к папке со скачанными датафреймами
    files = [f for f in os.listdir(path)]
    pd.set_option('display.max_colwidth', None)
    for f in files:
        df = path + f'\\{f}'
        table = pd.read_csv(df, header=None)
        start = timer()
        with open(f'{f[:-4]}.dat', mode='a', encoding='utf-8') as cs:
            writer = csv.writer(cs)
            writer.writerow(head)
            for y in range(table.shape[0]):
                zxc = str(table.iloc[y])[5:]
                new = []
                st = 0
                for el in k:
                    new.append(zxc[st:st + el].strip())
                    st += el + 1
                writer.writerow(new)
        print(timer() - start)

# d = Info.upload_info(file_path='data/srock8/20069.dat', save_path='20069.csv', extension='csv')
# l = Data()
# print(l.set_location(20069, time=['1980/12/12', '2022/12/12']))
# print(l.choose_time())

# p = Predictions()
# print(p.make_prediction(data=[[1.966e+03, 1.000e+00, 2.000e+01, 6.020e+01, 3.050e+01, 1.150e+02],
#        [1.966e+03, 1.000e+00, 1.500e+01, 7.950e+01, 7.700e+01, 1.000e+01]],
#                   model='XGBoost'))

# p = Predictions()
# p.make_day_prediction()

class Info:

    def __init__(self) -> None:
        pass

    def upload_info(file_path, save_path='file.csv', extension='csv'):
        local_path = 'data/storage/'
        if extension == 'csv' or extension == 'dat':
            data = pd.read_csv(file_path).fillna(method='ffill')
            data = data.to_csv(local_path + save_path, index=False)  # сохраняем в локальную папку storage
        elif extension == 'xlsx':
            data = pd.read_excel(file_path).fillna(method='ffill')
            data = data.to_csv(local_path + save_path, index=False)

    def export_info(self):
        pass  # чее??? TODO: хз написать ченить


class Data:  # migrated Location
    def __init__(self) -> None:  # функция парсит .dat; .csv файлы и заполняет пропущенные значения
        self.data = None

    def set_location(self, station_index=int, time=list):
        # тут короче либо в бд хранить данные климатические и к ним обращаться
        # либо яндекс API юзать
        # написан варик где пока все на локал data/storage/___.dat
        for i in os.listdir('data/storage/'):
            sin_index = int(i.replace('.dat', '').replace('.csv', '').replace('.xlsx', ''))
            if sin_index == station_index:
                dataframe = pd.read_csv(f'data/storage/{i}', sep=',')
                break

        self.data = dataframe
        self.location = sin_index

        if time:
            start = time[0]
            end = time[1]
            start = start.split('/')
            end = end.split('/')
            print(start, end)
            choose = self.data.loc[
                (self.data['Год по Гринвичу'] >= int(start[0])) & (self.data['Год по Гринвичу'] <= int(end[0]))]
            choose = choose.loc[
                (choose['Месяц по Гринвичу'] >= int(start[1])) & (choose['Месяц по Гринвичу'] <= int(end[1]))]
            choose = choose.loc[
                (choose['День по Гринвичу'] >= int(start[2])) & (choose['День по Гринвичу'] <= int(end[2]))]

            return choose  # оставлю как есть в зависимости от того что понадобится тебе. Возвращается объект датафрейма там можно медиану найти

    def to_validation_type(self):

        X = np.array([self.data['Год по Гринвичу'].to_numpy(),
                      self.data['Месяц по Гринвичу'].to_numpy(),
                      self.data['День по Гринвичу'].to_numpy(),
                      self.data['Широта'].to_numpy(dtype=float),
                      self.data['Долгота'].to_numpy(dtype=float),
                      self.data['Высота над уровнем моря'].to_numpy(dtype=float)])

        X = np.transpose(X)
        return X


def make_prediction(data, model='XGBoost'):
    pred = []
    # data format: Y; m; d; hour; latitude; longitude; altitude above sea level
    # output: tempreture percipitation wind humidity pressure
    if model == 'XGBoost':
        Xg_reg_temp = joblib.load('sklearn_models/xg_regressor_temp.pkl')
        Xg_reg_per = joblib.load('sklearn_models/xg_regressor_per.pkl')
        Xg_reg_wind = joblib.load('sklearn_models/xg_regressor_wind.pkl')
        Xg_reg_hum = joblib.load('sklearn_models/xg_regressor_hum.pkl')
        Xg_reg_press = joblib.load('sklearn_models/xg_regressor_press.pkl')

        pred.append(Xg_reg_temp.predict(data))
        pred.append(Xg_reg_per.predict(data))
        pred.append(Xg_reg_wind.predict(data))
        pred.append(Xg_reg_hum.predict(data))
        pred.append(Xg_reg_press.predict(data))

        return np.transpose(np.array(pred))

    elif model == 'RFR':  # TODO: дописать
        rfr_reg = joblib.load('data//sklearn_models//rf_regressor.pkl')
        pred = rfr_reg.predict(data)
        return pred


def make_day_prediction(date, model='XGBoost'):
    pred = []
    date = [[[date[0], date[1], date[2], i, date[3], date[4], date[5]]] for i in range(0, 22, 3)]
    for data in date:
        pred.append(list(make_prediction(data)[0]))
    # return 9 np.ndarray
    return pred




