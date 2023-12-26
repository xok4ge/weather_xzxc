import requests


API_KEY_W='930e11b7-bae8-4f45-a7f4-7eca6fa464f4'

API_KEY_G='6c440d10-829c-47b5-8622-839601e9f8e3'

# c = input()
# payload = {'geocode': c,
#            'apikey': API_KEY_G,
#            'format': 'json'}
# res_g = requests.get('https://geocode-maps.yandex.ru/1.x', params=payload)
# print(res_g.url)
# print(res_g.json()['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['boundedBy']['Envelope']['lowerCorner'].split())

# cords=['37.038186', '55.312148']
#
# payload={
#         'lat': cords[1],
#         'lon': cords[0]
# }
#
# res_w = requests.get('https://api.weather.yandex.ru/v2/forecast?', params=payload,
#                      headers={'X-Yandex-API-Key': API_KEY_W})
# print(res_w.json())