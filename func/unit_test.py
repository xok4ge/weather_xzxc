import requests

API_KEY_G = '6c440d10-829c-47b5-8622-839601e9f8e3'

def validate_city(name, key):
    payload = {'geocode': name,
               'apikey': key,
               'lang': 'en_Ru',
               'format': 'json',
               'kind': 'locality',
               'results': 1}
    res_g = requests.get('https://geocode-maps.yandex.ru/1.x', params=payload)
    geo_json = res_g.json()
    if geo_json['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']["found"] == "0":
        return "Город не найден. Возможно, Вы допустили ошибку или опечатку."
    else:
        return geo_json

print(validate_city("Москва", API_KEY_G))
print(validate_city("fkdrgkdgjhdkh", API_KEY_G))

