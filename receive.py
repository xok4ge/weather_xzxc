import json

# head = ['Синоптический индекс станции', 'Год по Гринвичу', 'Месяц по Гринвичу',
#         'День по Гринвичу', 'Срок по Гринвичу', 'Общее количество облачности', 'Погода между сроками',
#         'Направление ветра', 'Средняя скорость ветра', 'Максимальная скорость ветра',
#         'Сумма осадков за период между сроками', 'Относительная влажность воздуха',
#         'Температура воздуха по сухому термометру', 'Атмосферное давление на уровне станции']

f = open("json_demo.json")
data = json.load(f)
result_final = []

date = data["forecasts"][0]["date"].split("-")
hours = []
for i in range(0, 24, 3):
    src = data["forecasts"][0]["hours"]
    src[i]["prec_mm"] += src[i - 1]["prec_mm"] + src[i - 2]["prec_mm"]
    hours.append(src[i])
for i in hours:
    result = dict()
    result["year"] = date[0]
    result["month"] = date[1]
    result["day"] = date[2]
    result["hour"] = i["hour"]
    result["cloudness"] = i["cloudness"]
    result["condition"] = i["condition"]
    result["wind_dir"] = i["wind_dir"]
    result["wind_speed"] = i["wind_speed"]
    result["wind_gust"] = i["wind_gust"]
    result["prec_mm"] = i["prec_mm"]
    result["humidity"] = i["humidity"]
    result["temp"] = i["temp"]
    result["pressure_mm"] = i["pressure_mm"]
    result_final.append(result)

# for i in result_final:
#     print(i)