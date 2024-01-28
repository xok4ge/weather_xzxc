import requests


API_KEY_W='1e168a48-80cc-4e78-93ac-0f949443fe03'

API_KEY_G='6c440d10-829c-47b5-8622-839601e9f8e3'

# может возвращать всякую херню надо эт дело допиливать но ща времени нет
# ладно допилил, осталось выводить ошибку когда город error
def get_place(place):
    payload = {'geocode': place,
               'apikey': API_KEY_G,
               'lang': 'en_Ru',
               'format': 'json',
               'kind': 'locality',
               'results': 1}
    res_g = requests.get('https://geocode-maps.yandex.ru/1.x', params=payload)
    geo_json = res_g.json()
    try:
        kind = geo_json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind']
        if kind in ['locality', 'province']:
            coords = geo_json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
            payload = {
                    'lat': coords[1],
                    'lon': coords[0]
            }

            res_w = requests.get('https://api.weather.yandex.ru/v2/forecast?', params=payload,
                                 headers={'X-Yandex-API-Key': API_KEY_W})
            rdata = res_w.json()
            return rdata
        else:
            raise Exception
    except Exception as e:
        return e



