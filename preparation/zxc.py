# from bs4 import BeautifulSoup
# from db import *
#
# conn = db_session()
# cur = conn.cursor()
# with open('meteo.html', mode='r', encoding='UTF-8') as file:
#     text = file.read()
#
#
# zxc = BeautifulSoup(text, 'html.parser')
# for tb in zxc.find_all('tr')[1:]:
#     resp = list(filter(lambda x: x !='\n', tb))
#     for x in range(len(resp)):
#         resp[x]=resp[x].contents
#     resp = resp[:4]+resp[5:]
#     si, name, lat, long, country = list(map(lambda x: x[0], resp))
#     lat = str(lat).replace(',', '.')
#     long = str(long).replace(',', '.')
#     cur.execute('''insert into stations(synoptic_index, name, latitude, longitude, country)
#                     values (%s, %s, %s, %s, %s)''', (int(si), name, float(lat), float(long), country))
# print('done')