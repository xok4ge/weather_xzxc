import pandas as pd
import csv
from timeit import default_timer as timer
import os

# headers=[]
# k=0
# with open('names.txt', mode='r', encoding='utf-8') as f:
#     for x in f.readlines():
#         new = x.strip()
#         if new in headers:
#             new+=str(k)
#             k+=1
#         headers.append(new)
# print(headers)

head = ['Синоптический индекс станции', 'Год по Гринвичу', 'Месяц по Гринвичу', 'День по Гринвичу', 'Срок по Гринвичу', 'Год источника (местный)', 'Месяц источника (местный)', 'День источника (местный)', 'Срок источника', 'Номер срока в сутках по поясному декретному зимнему времени (ПДЗВ)', 'Время местное', 'Номер часового пояса', 'Начало метеорологических суток по ПДЗВ', 'Горизонтальная видимость', 'Признак качества', 'Признак наличия знака «>»', 'Общее количество облачности', 'Признак качества0', 'Количество облачности нижнего яруса', 'Признак качества1', 'Форма облаков верхнего яруса', 'Признак качества2', 'Форма облаков среднего яруса', 'Признак качества3', 'Форма облаков вертикального развития', 'Признак качества4', 'Слоистые и слоисто-кучевые облака', 'Признак качества5', 'Слоисто-дождевые, разорвано-дождевые облака', 'Признак качества6', 'Высота нижней границы облачности', 'Признак качества7', 'Признак способа определения высоты нижней границы облачности', 'Признак наличия облачности ниже уровня станции', 'Признак качества8', 'Погода между сроками', 'Признак качества9', 'Погода в срок наблюдения', 'Признак качества10', 'Направление ветра', 'Признак качества11', 'Средняя скорость ветра', 'Признак качества12', 'Признак наличия знака «>»13', 'Максимальная скорость ветра', 'Признак качества14', 'Признак наличия знака «>»15', 'Сумма осадков за период между сроками', 'Признак качества16', 'Температура поверхности почвы', 'Признак качества17', 'Минимальная температура поверхности почвы', 'Признак качества18', 'Минимальная температура поверхности почвы между сроками', 'Признак качества19', 'Максимальная температура поверхности почвы между сроками', 'Признак качества20', 'Температура поверхности почвы по максимальному термометру после встряхивания', 'Признак качества21', 'Температура воздуха по сухому термометру', 'Признак качества22', 'Температура воздуха по смоченному термометру', 'Признак качества23', 'Признак наличия льда на батисте', 'Температура воздуха по спирту минимального термометра', 'Признак качества24', 'Минимальная температура воздуха между сроками', 'Признак качества25', 'Максимальная температура воздуха между сроками', 'Признак качества26', 'Температура воздуха по максимальному термометру после встряхивания', 'Признак качества27', 'Парциальное давление водяного пара', 'Признак качества28', 'Указатель точности измерения элемента', 'Относительная влажность воздуха', 'Признак качества29', 'Дефицит насыщения водяного пара', 'Признак качества30', 'Указатель точности измерения элемента31', 'Температура точки росы', 'Признак качества32', 'Атмосферное давление на уровне станции', 'Признак качества33', 'Атмосферное давление на уровне моря', 'Признак качества34', 'Характеристика барической тенденции', 'Признак качества35', 'Величина барической тенденции', 'Признак качества36']
k = [5, 4, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 4, 1, 1, 2, 1, 2, 1, 2, 1, 3, 1, 2, 1, 1, 2, 1, 1, 6, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 1, 3, 1, 7, 1, 1, 5, 1, 6, 1, 6, 1, 2, 1, 4, 1]

path = 'C:\\Users\\xok4ge\Documents\\dataset\\data1'  # путь к папке со скачанными датафреймами
files = [f for f in os.listdir(path)]
pd.set_option('display.max_colwidth', None)
for f in files:
    df = path+f'\\{f}'
    table = pd.read_csv(df, header=None)
    start = timer()
    with open(f'data1/{f[:-4]}.csv', mode='a', encoding='utf-8') as cs:
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