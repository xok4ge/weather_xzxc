from bs4 import BeautifulSoup
from db import *

conn = db_session()
cur = conn.cursor()
with open('meteo.html', mode='r', encoding='UTF-8') as file:
    text = file.read()


zxc = BeautifulSoup(text, 'html.parser')
for tb in zxc.find_all('tr')[1:]:
    resp = list(filter(lambda x: x !='\n', tb))
    for x in range(len(resp)):
        resp[x]=resp[x].contents
    si, name, lat, long, alt, country = list(map(lambda x: x[0], resp))
    lat = str(lat).replace(',', '.')
    long = str(long).replace(',', '.')
    alt = str(alt).replace(',', '.')
    cur.execute('''insert into stations(synoptic_index, name, latitude, longitude, altitude, country)
                    values (%s, %s, %s, %s, %s, %s)''', (int(si), name, float(lat), float(long), alt, country))
print('done')