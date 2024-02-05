import dearpygui.dearpygui as dpg
import ctypes
import sys
import math
from api import *
from receive import *
from datetime import datetime
from get_data import *
from pathlib import Path as pth
from date_picker import DatePicker
from db import *
from config import *
from file_import import *
from predict import make_day_prediction


conn = db_session()
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
view_pos = [screensize[0] // 2 - 70, screensize[1] // 2 - 270]
dpg.create_context()



def upload_file(sender, app_data):
    dpg.configure_item('file_ext_pop', show=True)
    upload_file_fi(app_data['file_path_name'], app_data['file_name'].split('.'))
    dpg.configure_item('file_ext_pop', show=False)
    stations = [', '.join(list(map(str, i))) for i in get_stations()]

    dpg.configure_item(combo_station, items=stations)



def monitor_place(sender, app_data):
    try:
        plc = dpg.get_value('mtr_cnf')
        data = get_place(plc)
        cldate, fjson, curjson = read_json(data)
        monitor_clear()
        period = [int(i['hour'])  for i in fjson]
        temp, wind_s, pressure, prec, hum, wind_m = [[float(i['temp']) for i in fjson], [float(i['wind_speed']) for i in fjson],
                                                     [float(i['pressure_mm']) for i in fjson], [float(i['prec_mm']) for i in fjson],
                                                     [float(i['humidity']) for i in fjson], max([float(i['wind_gust']) for i in fjson])]

        dpg.set_value('mnt_date', dpg.get_value('mnt_date') + cldate)
        dpg.set_value('mnt_avtemp', dpg.get_value('mnt_avtemp') + str(round(sum(temp)/len(fjson), 1)) + ' °C')
        dpg.set_value('mnt_avwind', dpg.get_value('mnt_avwind') + str(round(sum(wind_s)/len(fjson), 1)) + ' m/s')
        dpg.set_value('mnt_avpr', dpg.get_value('mnt_avpr') + str(round(sum(pressure)/len(fjson), 1)) + ' mmHg')
        dpg.set_value('mnt_rfal', dpg.get_value('mnt_rfal') + str(round(sum(prec), 1)) + ' mm')
        dpg.set_value('mnt_hum', dpg.get_value('mnt_hum') + str(round(sum(hum)/len(fjson), 1)) + ' %')
        dpg.set_value('mnt_mint', dpg.get_value('mnt_mint') + str(min([float(i['temp']) for i in fjson])) + ' °C')
        dpg.set_value('mnt_maxt', dpg.get_value('mnt_maxt') + str(max([float(i['temp']) for i in fjson])) + ' °C')
        dpg.set_value('mnt_maxw', dpg.get_value('mnt_maxw') + str(wind_m) + ' m/s')
        dpg.set_value('mntc_temp', dpg.get_value('mntc_temp') + str(curjson['temp']) + ' °C')
        dpg.set_value('mntc_wind', dpg.get_value('mntc_wind') + str(curjson['wind_speed']) + ' m/s')
        dpg.set_value('mntc_hum', dpg.get_value('mntc_hum') + str(curjson['humidity']) + ' %')
        dpg.set_value('mntc_pr', dpg.get_value('mntc_pr') + str(curjson['pressure_mm']) + ' mmHg')
        dpg.set_value('mntc_cnd', dpg.get_value('mntc_cnd') + str(curjson['condition']))

        mn_axis_fit()

        dpg.set_value('lsmn_temp', [period, temp])
        dpg.set_value('sctmn_temp', [period, temp])

        dpg.set_value('lsmn_rfal', [period, prec])
        dpg.set_value('sctmn_rfal', [period, prec])

        dpg.set_value('lsmn_hum', [period, hum])
        dpg.set_value('sctmn_hum', [period, hum])

        dpg.set_value('lsmn_pres', [period, pressure])
        dpg.set_value('sctmn_pres', [period, pressure])

        dpg.set_value('bmn_wind', [period, wind_s])
        dpg.set_value('bmn_windmx', [period, [wind_m]*len(fjson)])

        dpg.set_value('drag_temp', curjson['temp'])
        dpg.configure_item('drag_temp', show=True)
    except Exception as e:
        dpg.configure_item('er_city', show=True)
def save_file_an(sender, app_data):
    an_flnms = ['an_ind', 'an_date', 'an_avtemp', 'an_avwind', 'an_avpr', 'an_rfal', 'an_hum', 'an_cc', 'an_mint',
          'an_maxt', 'an_maxw']
    with open(app_data['file_path_name'], mode='w', encoding='utf-8') as file:
        for el in an_flnms:
            file.write(dpg.get_value(el)+'\n')


def fr_axis_fit():
    dpg.set_axis_limits_auto('fr_xtemp')
    dpg.fit_axis_data('fr_xtemp')
    dpg.set_axis_limits_auto('fr_ytemp')
    dpg.fit_axis_data('fr_ytemp')

    dpg.set_axis_limits_auto('fr_xrfal')
    dpg.fit_axis_data('fr_xrfal')
    dpg.set_axis_limits_auto('fr_yrfal')
    dpg.fit_axis_data('fr_yrfal')

    dpg.set_axis_limits_auto('fr_xhum')
    dpg.fit_axis_data('fr_xhum')
    dpg.set_axis_limits_auto('fr_yhum')
    dpg.fit_axis_data('fr_yhum')

    dpg.set_axis_limits_auto('fr_xpres')
    dpg.fit_axis_data('fr_xpres')
    dpg.set_axis_limits_auto('fr_ypres')
    dpg.fit_axis_data('fr_ypres')

    dpg.set_axis_limits_auto('fr_xwind')
    dpg.fit_axis_data('fr_xwind')
    dpg.set_axis_limits_auto('fr_ywind')
    dpg.fit_axis_data('fr_ywind')
def mn_axis_fit():
    dpg.set_axis_limits_auto('mn_xtemp')
    dpg.fit_axis_data('mn_xtemp')
    dpg.set_axis_limits_auto('mn_ytemp')
    dpg.fit_axis_data('mn_ytemp')

    dpg.set_axis_limits_auto('mn_xrfal')
    dpg.fit_axis_data('mn_xrfal')
    dpg.set_axis_limits_auto('mn_yrfal')
    dpg.fit_axis_data('mn_yrfal')

    dpg.set_axis_limits_auto('mn_xhum')
    dpg.fit_axis_data('mn_xhum')
    dpg.set_axis_limits_auto('mn_yhum')
    dpg.fit_axis_data('mn_yhum')

    dpg.set_axis_limits_auto('mn_xpres')
    dpg.fit_axis_data('mn_xpres')
    dpg.set_axis_limits_auto('mn_ypres')
    dpg.fit_axis_data('mn_ypres')

    dpg.set_axis_limits_auto('mn_xwind')
    dpg.fit_axis_data('mn_xwind')
    dpg.set_axis_limits_auto('mn_ywind')
    dpg.fit_axis_data('mn_ywind')
def graph_axis_fit():
    dpg.set_axis_limits_auto('x_axis_temp')
    dpg.fit_axis_data('x_axis_temp')
    dpg.set_axis_limits_auto('y_axis_temp')
    dpg.fit_axis_data('y_axis_temp')

    dpg.set_axis_limits_auto('x_axis_wind')
    dpg.fit_axis_data('x_axis_wind')
    dpg.set_axis_limits_auto('y_axis_wind')
    dpg.fit_axis_data('y_axis_wind')

    dpg.set_axis_limits_auto('x_axis_rainfall')
    dpg.fit_axis_data('x_axis_rainfall')
    dpg.set_axis_limits_auto('y_axis_rainfall')
    dpg.fit_axis_data('y_axis_rainfall')

    dpg.set_axis_limits_auto('x_axis_mstr')
    dpg.fit_axis_data('x_axis_mstr')
    dpg.set_axis_limits_auto('y_axis_mstr')
    dpg.fit_axis_data('y_axis_mstr')

    dpg.set_axis_limits_auto('x_axis_prsr')
    dpg.fit_axis_data('x_axis_prsr')
    dpg.set_axis_limits_auto('y_axis_prsr')
    dpg.fit_axis_data('y_axis_prsr')

    dpg.set_axis_limits_auto('x_pie')
    dpg.fit_axis_data('x_pie')
    dpg.set_axis_limits_auto('y_pie')
    dpg.fit_axis_data('y_pie')
def monitor_clear():
    dpg.set_value('mnt_date', value='Date: ')
    dpg.set_value('mnt_avtemp', value='Average temperature: ')
    dpg.set_value('mnt_avwind', value='Average wind velocity: ')
    dpg.set_value('mnt_avpr', value='Average atm pressure: ')
    dpg.set_value('mnt_rfal', value='Amount of rainfall: ')
    dpg.set_value('mnt_hum', value='Average humidity value: ')
    dpg.set_value('mnt_mint', value='Minimum temperature: ')
    dpg.set_value('mnt_maxt', value='Maximum temperature: ')
    dpg.set_value('mnt_maxw', value='Maximum wind velocity: ')
    #####
    dpg.set_value('mntc_temp', value='Current temperature: ')
    dpg.set_value('mntc_wind', value='Current wind velocity: ')
    dpg.set_value('mntc_hum', value='Current humidity: ')
    dpg.set_value('mntc_pr', value='Current pressure: ')
    dpg.set_value('mntc_cnd', value='Current condition: ')


def forecast_clear():
    dpg.set_value('lsfr_temp', [[], []])
    dpg.set_value('predfr_temp', [[], []])

    dpg.set_value('lsfr_wind', [[], []])
    dpg.set_value('predfr_wind', [[], []])

    dpg.set_value('lsfr_rfal', [[], []])
    dpg.set_value('predfr_rfal', [[], []])

    dpg.set_value('lsfr_hum', [[], []])
    dpg.set_value('predfr_hum', [[], []])

    dpg.set_value('lsfr_pres', [[], []])
    dpg.set_value('predfr_pres', [[], []])

def analyze_clear():
    dpg.set_value('an_ind', value='Synoptic index: ')
    dpg.set_value('an_date', value='Date: ')
    dpg.set_value('an_avtemp', value='Average temperature: ')
    dpg.set_value('an_avwind', value='Average wind velocity: ')
    dpg.set_value('an_avpr', value='Average atm pressure: ')
    dpg.set_value('an_rfal', value='Amount of rainfall: ')
    dpg.set_value('an_hum', value='Average humidity value: ')
    dpg.set_value('an_cc', value='Cloud cover: ')
    dpg.set_value('an_mint', value='Minimum temperature: ')
    dpg.set_value('an_maxt', value='Maximum temperature: ')
    dpg.set_value('an_maxw', value='Maximum wind velocity: ')


def change_disp(sender, app_data):
    diagram_y = ['bar_temp', 'bar_wind', 'bar_wind_avg', 'bar_rainfall', 'bar_mstr', 'bar_prsr']
    graph_y = ['line_series_temp', 'line_series_wind', 'line_series_rainfall', 'line_series_mstr', 'line_series_prsr',
               'scatter_temp', 'scatter_wind', 'scatter_rainfall', 'scatter_mstr', 'scatter_prsr']
    if app_data == 'diagram':
        for el in graph_y:
            dpg.configure_item(el, show=False)
        for el in diagram_y:
            dpg.configure_item(el, show=True)
    elif app_data == 'graph':
        for el in diagram_y:
            dpg.configure_item(el, show=False)
        for el in graph_y:
            dpg.configure_item(el, show=True)
    graph_axis_fit()

def render_vis_chart(df, period_type, date):

    try:
        render_data = get_render(df, [date.year, date.month, date.day], period_type)
    # main_params
        period, temp, wind, rnfl, moist, press, maxw = [list(map(float, render_data['Срок по Гринвичу'])),
                                                  list(map(float, render_data['Температура воздуха по сухому термометру'])),
                                                  list(map(float, render_data['Средняя скорость ветра'])),
                                                  list(map(float, render_data['Сумма осадков за период между сроками'])),
                                                  list(map(float, render_data['Относительная влажность воздуха'])),
                                                  list(map(lambda x: x*0.75, map(float, render_data['Атмосферное давление на уровне станции']))),
                                                  list(map(float, render_data['Максимальная скорость ветра']))]
        if math.isnan(temp[0]) and math.isnan(wind[0]) and math.isnan(press[0]):
            raise Exception
        # sup_params
        syn_ind = str(int(render_data.iloc[0]['Синоптический индекс станции']))
        labels = {0: ['clear', 0],
                  1: ['light clouds', 0],
                  2: ['cloudy', 0],
                  3: ['snowstorm/sandstorm', 0],
                  4: ['fog', 0],
                  5: ['drizzle', 0],
                  6: ['rain', 0],
                  7: ['snow', 0],
                  8: ['rainfall', 0],
                  9: ['thunder', 0]}
        weath = list(map(float, render_data['Погода между сроками']))
        piev, piel = [], []
        for el in weath:
            try:
                labels[int(el)][1]+=1
            except ValueError:
                continue
        for x in labels.values():
            if x[1]!=0:
                piev += [x[1]]
                piel += [x[0]]
        cl_cvr, cl_cvr_w = list(map(float, render_data['Общее количество облачности'])), ''
        if len(list(filter(lambda x: 5 <= x <= 13, cl_cvr))) > len(list(filter(lambda x: 0 <= x < 5, cl_cvr))):
            cl_cvr_w = 'cloudy'
        else:
            cl_cvr_w = 'clear'


        dpg.set_value('line_series_temp', [period, temp])
        dpg.set_value('scatter_temp', [period, temp])

        dpg.set_value('line_series_wind', [period, wind])
        dpg.set_value('scatter_wind', [period, wind])

        dpg.set_value('line_series_rainfall', [period, rnfl])
        dpg.set_value('scatter_rainfall', [period, rnfl])

        dpg.set_value('line_series_mstr', [period, moist])
        dpg.set_value('scatter_mstr', [period, moist])

        dpg.set_value('line_series_prsr', [period, press])
        dpg.set_value('scatter_prsr', [period, press])

        dpg.set_value('bar_temp', [period, temp])
        dpg.set_value('bar_wind', [period, wind])
        dpg.set_value('bar_wind_avg', [period, maxw])
        dpg.set_value('bar_rainfall', [period, rnfl])
        dpg.set_value('bar_mstr', [period, moist])
        dpg.set_value('bar_prsr', [period, press])

        graph_axis_fit()
        analyze_clear()
        forecast_clear()

        dpg.set_value('an_ind', dpg.get_value('an_ind') + syn_ind)
        dpg.set_value('an_date', dpg.get_value('an_date') + str(date.date()) + f"{' start of the week' if period_type=='week' else ''}")
        dpg.set_value('an_rfal', dpg.get_value('an_rfal') + str(round(sum(rnfl), 1)) + ' mm')
        dpg.set_value('an_cc', dpg.get_value('an_cc') + cl_cvr_w)
        dpg.set_value('an_maxw', dpg.get_value('an_maxw') + str(max(maxw)) + ' m/s')
        dpg.set_value('an_avtemp', dpg.get_value('an_avtemp') + str(round(sum(temp)/len(temp), 1)) + ' °C')
        dpg.set_value('an_mint', dpg.get_value('an_mint') + str(min(temp)) + ' °C')
        dpg.set_value('an_maxt', dpg.get_value('an_maxt') + str(max(temp)) + ' °C')
        dpg.set_value('an_avwind', dpg.get_value('an_avwind') + str(round(sum(wind)/len(wind), 1)) + ' m/s')
        dpg.set_value('an_avpr', dpg.get_value('an_avpr') + str(round(sum(press)/len(press), 1)) + ' mmHg')
        dpg.set_value('an_hum', dpg.get_value('an_hum') + str(round(sum(moist)/len(moist), 1)) + ' %')

        dpg.configure_item('an_pie', values=piev, labels=piel)

        if period_type == 'day':
            extra = list(map(float, get_station_predict(syn_ind, conn)))
            data = [date.year, date.month, date.day, extra[0], extra[1], extra[2]]
            predict = make_day_prediction(data)

            temp_pr, wind_pr, prec_pr, hum_pr, press_pr = [
                [i[0] for i in predict], [i[2] for i in predict], [i[1] for i in predict], [i[3] for i in predict],
                [i[4]*0.75 for i in predict]]
            print(temp_pr, wind_pr, prec_pr, hum_pr, press_pr)
            # Y; m; d; hour; latitude; longitude; altitude above sea level


            dpg.set_value('lsfr_temp', [period, temp])
            dpg.set_value('predfr_temp', [period, temp_pr])

            dpg.set_value('lsfr_wind', [period, wind])
            dpg.set_value('predfr_wind', [period, wind_pr])

            dpg.set_value('lsfr_rfal', [period, rnfl])
            dpg.set_value('predfr_rfal', [period, prec_pr])

            dpg.set_value('lsfr_hum', [period, moist])
            dpg.set_value('predfr_hum', [period, hum_pr])

            dpg.set_value('lsfr_pres', [period, press])
            dpg.set_value('predfr_pres', [period, press_pr])

            fr_axis_fit()
        else:
            pass
    except Exception as e:
        print(e)
        dpg.configure_item('kokodrile', show=True)



def get_stations():
    stations = []
    p = pth('data')
    for dt in [x for x in p.iterdir() if x.is_dir()]:
        new = pth(dt)
        stations += [get_station_db(i.name[:-4], conn) for i in new.iterdir()]
    stations = list(filter(lambda x: x is not None, stations))
    stations = sorted(stations, key=lambda x: int(x[2]))
    return stations


def set_station_datepick(sender, app_data):
    minv, maxv = get_data_clbk(str(app_data.split(', ')[-1]), date=True)
    date_picker.set_min_value(datetime(minv[0], minv[1], minv[2]))
    date_picker.set_max_value(datetime(maxv[0], maxv[1], maxv[2]))
    date_picker.set_value(datetime(maxv[0], maxv[1], maxv[2]))


def confirm_pref_btn():
    period = dpg.get_value('period')
    place = dpg.get_value('place_list')
    if place != 'list of stations':
        date = date_picker.get_value()
        df = get_data_clbk(str(place.split(', ')[-1]))
        render_vis_chart(df, period, date)


# reg/log window block
def main_window():
    dpg.set_viewport_width(smw_width)
    dpg.set_viewport_height(smw_height)
    if dpg.get_active_window():
        print(dpg.get_active_window())
        dpg.configure_item(dpg.get_active_window(), show=False)
    dpg.configure_item('main', show=True)
    if dpg.get_value('username_input'):
        dpg.set_value('username_input', '')
    if dpg.get_value('password_input'):
        dpg.set_value('password_input', '')
    if dpg.get_value('password_log_input'):
        dpg.set_value('password_log_input', '')
    if dpg.get_value('username_log_input'):
        dpg.set_value('username_log_input', '')
    dpg.set_primary_window(window=main_menu_window, value=True)


def reg_user(sender, app_data):
    dpg.set_value('error_reg', '')
    db_username = dpg.get_value('username_input')
    db_password = dpg.get_value('password_input')
    back = add_db_user(db_username, db_password, conn)
    if back:
        dpg.set_value('error_reg', f'user {back} already exists')


def reg_user_window():
    dpg.configure_item(dpg.get_active_window(), show=False)
    dpg.configure_item('auth', show=True)
    dpg.set_primary_window(window=auth_window, value=True)
    dpg.set_value('error_reg', '')


def login_user_window():
    dpg.configure_item(dpg.get_active_window(), show=False)
    dpg.configure_item('login', show=True)
    dpg.set_primary_window(window=login_window, value=True)
    dpg.set_value('error_log', '')


def log_user():
    dpg.set_value('error_reg', '')
    db_username = dpg.get_value('username_log_input')
    db_password = dpg.get_value('password_log_input')
    back = login_db_user(db_username, db_password, conn)  # True/False, username
    if not back[0]:
        dpg.set_value('error_log', f'incorrect login or password')
    else:
        dpg.set_value('error_log', 'success')
        work_window_start()

# def move_mouse(sender, app_data):
#     print(app_data)
#
#
# with dpg.handler_registry():
#     dpg.add_mouse_move_handler(callback=move_mouse)


with dpg.font_registry():
    default_font = dpg.add_font(file='assets/fonts/dante.ttf', size=20)
    with dpg.font('assets/fonts/russian.otf', size=14, pixel_snapH=True) as russian_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

with dpg.window(tag='auth', label='ffgm', no_resize=True, no_move=True, no_title_bar=False, show=False) as auth_window:
    with dpg.group(pos=[smw_width // 2 - 130, smw_height // 2 - 100]):
        dpg.add_text(default_value='username')
        dpg.add_input_text(no_spaces=True, tag='username_input')
        dpg.add_text(default_value='password')
        dpg.add_input_text(password=True, no_spaces=True, tag='password_input')
        dpg.add_spacer(height=5, width=10)
        dpg.add_button(label='apply', width=100, callback=reg_user)
        dpg.add_text(default_value='', color=(243, 201, 255), tag='error_reg')

    with dpg.menu_bar(tag='back_bar_r'):
        dpg.add_button(label='<-', width=50, pos=[0,0], callback=main_window)

# help(dpg.window)
with dpg.window(tag='main', label='ffgm', no_resize=True, no_move=True, no_title_bar=False) as main_menu_window:
    with dpg.group(horizontal=True):
        title = dpg.add_text(default_value='ffgm.immo', pos=[smw_width // 2 - 100, smw_height // 2 - 100])
        dpg.bind_item_font(title, default_font)

    text = dpg.add_text(default_value='alpha vers', pos=[smw_width // 2 - 40, smw_height // 2 - 70])
    with dpg.group(horizontal=True, pos=[smw_width // 2 - 110, smw_height // 2 - 40]):
        register = dpg.add_button(label='register', callback=reg_user_window, width=100, height=30)
        login = dpg.add_button(label='login', callback=login_user_window, width=100, height=30)

with dpg.window(tag='login', label='ffgm', no_resize=True, no_move=True, show=False) as login_window:
    with dpg.group(pos=[smw_width // 2 - 130, smw_height // 2 - 100]):
        dpg.add_text(default_value='username')
        dpg.add_input_text(no_spaces=True, tag='username_log_input')
        dpg.add_text(default_value='password')
        dpg.add_input_text(password=True, no_spaces=True, tag='password_log_input')
        dpg.add_spacer(height=5, width=10)
        dpg.add_button(label='apply', width=100, callback=log_user)
        dpg.add_text(default_value='', color=(243, 201, 255), tag='error_log')

    with dpg.menu_bar(tag='back_bar_l'):
        dpg.add_button(label='<-', width=50, pos=[0,0], callback=main_window)

# end of the block

# work window block
with dpg.window(tag='work_window', no_scrollbar=True, label='ffgm', no_resize=True, no_move=True, show=False, no_scroll_with_mouse=True) as work_window:
        with dpg.menu_bar(tag='back_bar_work'):
            with dpg.group(pos=[0,0]):
                with dpg.menu(label=' File'):  # not a mstk, space is needed
                    with dpg.file_dialog(show=False, callback=upload_file, tag="upload_file_dia", width=700, height=400):
                        dpg.add_file_extension('(*.csv *.xlsx){.csv,.xlsx}')
                        dpg.add_file_extension('.csv', color=(121, 237, 158), custom_text='[CSV]')
                        dpg.add_file_extension('.xlsx', color=(121, 237, 158), custom_text='[EXCEL]')

                    dpg.add_menu_item(label='Import file', callback=lambda: dpg.show_item("upload_file_dia"))
                with dpg.menu(label='Extra'):
                    dpg.add_menu_item(label='Exit', callback=dpg.destroy_context)

        with dpg.tab_bar(tag='Navigation'):
            with dpg.tab(label='Visualisation'):
                with dpg.child_window(autosize_x=True, autosize_y=True, no_scrollbar=True, no_scroll_with_mouse=True, border=False):
                    with dpg.group(horizontal=True) as grp:
                        with dpg.child_window(width=320, height=310, no_scroll_with_mouse=True, no_scrollbar=True):
                            with dpg.group(horizontal=True):
                                with dpg.popup(parent=dpg.last_item(), modal=True, max_size=[300, 30],
                                               tag='file_ext_pop'):
                                    dpg.configure_item(dpg.last_item(), pos=[400, 200])
                                    dpg.add_text('the file is in the process of processing')
                                dpg.add_text('Choose place: ')
                                stations = [', '.join(list(map(str, i))) for i in get_stations()]
                                combo_station = dpg.add_combo(stations, width=350, no_arrow_button=True,
                                                              default_value='list of stations', callback=set_station_datepick, tag='place_list')
                            dpg.bind_item_font(combo_station, russian_font)
                            dpg.add_spacer(height=10)
                            with dpg.group(horizontal=True):
                                dpg.add_text('Choose period:')
                                dpg.add_radio_button(items=['day', 'week'], horizontal=True, tag='period', default_value='day')
                            dpg.add_spacer(height=10)
                            dpg.add_text('Choose date:')
                            date_picker = DatePicker()
                            confirm_pref_vis = dpg.add_button(label='confirm', pos=[215, 280], width=100, callback=confirm_pref_btn)
                            with dpg.popup(parent=dpg.last_item(), modal=True, max_size=[250, 30], tag='kokodrile'):
                                dpg.configure_item(dpg.last_item(), pos=[400, 200])
                                dpg.add_text('not enough data for processing')
                        with dpg.tab_bar(tag='visualisation_nav'):
                            #  graphs
                            with dpg.tab(label='Temperature'):
                                with dpg.plot(width=640, height=500):
                                    dpg.add_plot_legend(label='temperature')

                                    # REQUIRED: create x and y axes
                                    dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='x_axis_temp')
                                    dpg.add_plot_axis(dpg.mvYAxis, label="temperature, °C", tag="y_axis_temp")
                                    dpg.add_line_series([], [], tag='line_series_temp', parent='y_axis_temp')
                                    dpg.add_scatter_series([], [], tag='scatter_temp', parent='y_axis_temp')

                                    dpg.add_bar_series([], [], tag='bar_temp', parent='y_axis_temp', show=False)

                            with dpg.tab(label='Wind'):
                                with dpg.plot(width=640, height=500):
                                    dpg.add_plot_legend(label='wind')
                                    # REQUIRED: create x and y axes
                                    dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='x_axis_wind')
                                    dpg.add_plot_axis(dpg.mvYAxis, label="wind velocity, m/s", tag="y_axis_wind")
                                    dpg.add_line_series([], [], tag='line_series_wind', parent='y_axis_wind')
                                    dpg.add_scatter_series([], [], tag='scatter_wind', parent='y_axis_wind')
                                    dpg.add_bar_series([], [], label='avg_velocity', tag='bar_wind',
                                                       parent='y_axis_wind', weight=1, show=False)
                                    dpg.add_bar_series([], [], label='max_velocity', tag='bar_wind_avg',
                                                       parent='y_axis_wind', weight=0.5, show=False)

                            with dpg.tab(label='Rainfall'):
                                with dpg.plot(width=640, height=500):
                                    dpg.add_plot_legend(label='rainfall')
                                    # REQUIRED: create x and y axes
                                    dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='x_axis_rainfall')
                                    dpg.add_plot_axis(dpg.mvYAxis, label="precipitation total, mm", tag="y_axis_rainfall")
                                    dpg.add_line_series([], [], tag='line_series_rainfall', parent='y_axis_rainfall')
                                    dpg.add_scatter_series([], [], tag='scatter_rainfall', parent='y_axis_rainfall')
                                    dpg.add_bar_series([], [], tag='bar_rainfall', parent='y_axis_rainfall', show=False)

                            with dpg.tab(label='Humidity'):
                                with dpg.plot(width=640, height=500):
                                    dpg.add_plot_legend(label='moisture')
                                    # REQUIRED: create x and y axes
                                    dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='x_axis_mstr')
                                    dpg.add_plot_axis(dpg.mvYAxis, label="relative humidity, %", tag="y_axis_mstr")
                                    dpg.add_line_series([], [], tag='line_series_mstr', parent='y_axis_mstr')
                                    dpg.add_scatter_series([], [], tag='scatter_mstr', parent='y_axis_mstr')
                                    dpg.add_bar_series([], [], tag='bar_mstr', parent='y_axis_mstr', show=False)

                            with dpg.tab(label='Pressure'):
                                with dpg.plot(width=640, height=500):
                                    dpg.add_plot_legend(label='presssure')
                                    # REQUIRED: create x and y axes
                                    dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='x_axis_prsr')
                                    dpg.add_plot_axis(dpg.mvYAxis, label="atmosphere pressure, mmHg", tag="y_axis_prsr")
                                    dpg.add_line_series([], [], tag='line_series_prsr', parent='y_axis_prsr')
                                    dpg.add_scatter_series([], [], tag='scatter_prsr', parent='y_axis_prsr')
                                    dpg.add_bar_series([], [], tag='bar_prsr', parent='y_axis_prsr', show=False)

                        with dpg.child_window(width=320, height=203, pos=[0, 320], no_scroll_with_mouse=True):
                            with dpg.group(horizontal=True):
                                dpg.add_text(default_value='Display type:')
                                dpg.add_radio_button(items=['graph', 'diagram'], horizontal=True, callback=change_disp)

            with dpg.tab(label='Analyze'):
                with dpg.file_dialog(directory_selector=False, show=False, callback=save_file_an, tag="file_dialog_tag", width=700,
                                height=400):
                    dpg.add_file_extension(".txt", color=(121, 237, 158))
                with dpg.child_window(autosize_x=True, autosize_y=True, no_scrollbar=True, no_scroll_with_mouse=True,
                                      border=False):
                    with dpg.group(horizontal=True):
                        with dpg.child_window(width=320, height=523, no_scroll_with_mouse=True, no_scrollbar=True):
                            dpg.add_text(default_value='Info', pos=[320//2-20, 0])
                            dpg.add_spacer(height=20)
                            with dpg.group() as an_info:
                                dpg.add_text(default_value='Synoptic index: ', tag='an_ind')
                                dpg.add_text(default_value='Date: ', tag='an_date')
                                dpg.add_text(default_value='Average temperature: ', tag='an_avtemp')
                                dpg.add_text(default_value='Average wind velocity: ', tag='an_avwind')
                                dpg.add_text(default_value='Average atm pressure: ', tag='an_avpr')
                                dpg.add_text(default_value='Amount of rainfall: ', tag='an_rfal')
                                dpg.add_text(default_value='Average humidity value: ', tag='an_hum')
                                dpg.add_text(default_value='Cloud cover: ', tag='an_cc')
                                dpg.add_text(default_value='Minimum temperature: ', tag='an_mint')
                                dpg.add_text(default_value='Maximum temperature: ', tag='an_maxt')
                                dpg.add_text(default_value='Maximum wind velocity: ', tag='an_maxw')
                                dpg.add_button(label='save to file', pos=[100, 290], callback=lambda: dpg.show_item("file_dialog_tag"))

                        with dpg.plot(width=640, height=525):
                            dpg.add_plot_legend(label='presssure')
                            dpg.add_plot_axis(dpg.mvXAxis, tag='x_pie')
                            dpg.add_plot_axis(dpg.mvYAxis, tag="y_pie")
                            dpg.add_pie_series(0., 0., 10., values=[], labels=[], parent='y_pie',
                                               normalize=True, tag='an_pie')

            with dpg.tab(label='Forecasting'):
                with dpg.child_window(autosize_x=True, autosize_y=True, no_scrollbar=True, no_scroll_with_mouse=True,
                                      border=False):
                    with dpg.tab_bar(tag='forecast_tab'):
                        with dpg.tab(label='Temperature'):
                            with dpg.plot(width=970, height=500):
                                dpg.add_plot_legend(label='fr_temp')
                                dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='fr_xtemp')
                                dpg.add_plot_axis(dpg.mvYAxis, tag="fr_ytemp", label="temperature, °C")
                                dpg.add_line_series([], [], tag='lsfr_temp', parent='fr_ytemp', label='current')

                                dpg.add_line_series([], [], tag='predfr_temp', parent='fr_ytemp', label='predict')

                        with dpg.tab(label='Wind'):
                            with dpg.plot(width=640, height=500):
                                dpg.add_plot_legend(label='mn_wind')
                                dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='fr_xwind')
                                dpg.add_plot_axis(dpg.mvYAxis, label="wind velocity, m/s", tag="fr_ywind")
                                dpg.add_line_series([], [], label='current', tag='lsfr_wind',
                                                   parent='fr_ywind')

                                dpg.add_line_series([], [], tag='predfr_wind', parent='fr_ywind', label='predict')

                        with dpg.tab(label='Rainfall'):
                            with dpg.plot(width=640, height=500):
                                dpg.add_plot_legend(label='fr_rfal')
                                dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='fr_xrfal')
                                dpg.add_plot_axis(dpg.mvYAxis, tag="fr_yrfal", label='precipitation total, mm')
                                dpg.add_line_series([], [], tag='lsfr_rfal', parent='fr_yrfal', label='current')

                                dpg.add_line_series([], [], tag='predfr_rfal', parent='fr_yrfal', label='predict')

                        with dpg.tab(label='Humidity'):
                            with dpg.plot(width=640, height=500):
                                dpg.add_plot_legend(label='fr_hum')
                                dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='fr_xhum')
                                dpg.add_plot_axis(dpg.mvYAxis, tag="fr_yhum", label='relative humidity, %')
                                dpg.add_line_series([], [], tag='lsfr_hum', parent='fr_yhum', label='current')

                                dpg.add_line_series([], [], tag='predfr_hum', parent='fr_yhum', label='predict')


                        with dpg.tab(label='Pressure'):
                            with dpg.plot(width=640, height=500):
                                dpg.add_plot_legend(label='mn_pres')
                                dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='fr_xpres')
                                dpg.add_plot_axis(dpg.mvYAxis, tag="fr_ypres", label='atmosphere pressure, mmHg')
                                dpg.add_line_series([], [], tag='lsfr_pres', parent='fr_ypres', label='current')
                                dpg.add_line_series([], [], tag='predfr_pres', parent='fr_ypres', label='predict')

            with dpg.tab(label='Monitoring'):
                with dpg.child_window(autosize_x=True, autosize_y=True, no_scrollbar=True, no_scroll_with_mouse=True,
                                      border=False):
                    with dpg.group(horizontal=True):
                        with dpg.child_window(no_scrollbar=True, no_scroll_with_mouse=True,
                                              border=True, width=320, height=80):
                            with dpg.group(horizontal=True):
                                dpg.add_text('Input place: ')
                                dpg.add_input_text(width=200, height=50, tag='mtr_cnf')
                            dpg.add_spacer(height=10)
                            dpg.add_button(label='confirm', width=100, pos=[207, 50], callback=monitor_place)
                            with dpg.popup(parent=dpg.last_item(), modal=True, tag='er_city', max_size=[250, 20]):
                                dpg.configure_item(dpg.last_item(), pos=[400, 200])
                                dpg.add_text('the incorrect name of the city')
                        with dpg.tab_bar(tag='monitoring_tab'):
                            with dpg.tab(label='Temperature'):
                                with dpg.plot(width=640, height=500):
                                    dpg.add_plot_legend(label='mn_temp')
                                    dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='mn_xtemp')
                                    dpg.add_plot_axis(dpg.mvYAxis, tag="mn_ytemp", label="temperature, °C")
                                    dpg.add_line_series([], [], tag='lsmn_temp', parent='mn_ytemp')
                                    dpg.add_scatter_series([], [], tag='sctmn_temp', parent='mn_ytemp')
                                    dpg.add_drag_line(label='cur_temp', tag='drag_temp', parent='mn_temp',
                                                      color=(235, 153, 255), vertical=False, default_value=0, show=False)

                            with dpg.tab(label='Wind'):
                                with dpg.plot(width=640, height=500):
                                    dpg.add_plot_legend(label='mn_wind')
                                    dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='mn_xwind')
                                    dpg.add_plot_axis(dpg.mvYAxis, label="wind velocity, m/s", tag="mn_ywind")
                                    dpg.add_bar_series([], [], label='avg_velocity', tag='bmn_wind',
                                                       parent='mn_ywind', weight=1)
                                    dpg.add_bar_series([], [], label='max_velocity', tag='bmn_windmx',
                                                       parent='mn_ywind', weight=0.5)

                            with dpg.tab(label='Rainfall'):
                                with dpg.plot(width=640, height=500):
                                    dpg.add_plot_legend(label='mn_rfal')
                                    dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='mn_xrfal')
                                    dpg.add_plot_axis(dpg.mvYAxis, tag="mn_yrfal", label='precipitation total, mm')
                                    dpg.add_line_series([], [], tag='lsmn_rfal', parent='mn_yrfal')
                                    dpg.add_scatter_series([], [], tag='sctmn_rfal', parent='mn_yrfal')

                            with dpg.tab(label='Humidity'):
                                with dpg.plot(width=640, height=500):
                                    dpg.add_plot_legend(label='mn_hum')
                                    dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='mn_xhum')
                                    dpg.add_plot_axis(dpg.mvYAxis, tag="mn_yhum", label='relative humidity, %')
                                    dpg.add_line_series([], [], tag='lsmn_hum', parent='mn_yhum')
                                    dpg.add_scatter_series([], [], tag='sctmn_hum', parent='mn_yhum')

                            with dpg.tab(label='Pressure'):
                                with dpg.plot(width=640, height=500):
                                    dpg.add_plot_legend(label='mn_pres')
                                    dpg.add_plot_axis(dpg.mvXAxis, label="period, 3hr", tag='mn_xpres')
                                    dpg.add_plot_axis(dpg.mvYAxis, tag="mn_ypres", label='atmosphere pressure, mmHg')
                                    dpg.add_line_series([], [], tag='lsmn_pres', parent='mn_ypres')
                                    dpg.add_scatter_series([], [], tag='sctmn_pres', parent='mn_ypres')

                    with dpg.group(horizontal=True, pos=[0, 90]):
                        with dpg.child_window(width=320, height=432, no_scroll_with_mouse=True, no_scrollbar=True):
                            dpg.add_text(default_value='Info', pos=[320 // 2 - 20, 0])
                            dpg.add_spacer(height=20)
                            with dpg.group():
                                dpg.add_text(default_value='Date: ', tag='mnt_date')
                                dpg.add_text(default_value='Average temperature: ', tag='mnt_avtemp')
                                dpg.add_text(default_value='Average wind velocity: ', tag='mnt_avwind')
                                dpg.add_text(default_value='Average atm pressure: ', tag='mnt_avpr')
                                dpg.add_text(default_value='Amount of rainfall: ', tag='mnt_rfal')
                                dpg.add_text(default_value='Average humidity value: ', tag='mnt_hum')
                                dpg.add_text(default_value='Minimum temperature: ', tag='mnt_mint')
                                dpg.add_text(default_value='Maximum temperature: ', tag='mnt_maxt')
                                dpg.add_text(default_value='Maximum wind velocity: ', tag='mnt_maxw')
                                dpg.add_text(default_value='---------------------------------------------')
                                dpg.add_text(default_value='Current temperature: ', tag='mntc_temp')
                                dpg.add_text(default_value='Current wind velocity: ', tag='mntc_wind')
                                dpg.add_text(default_value='Current humidity: ', tag='mntc_hum')
                                dpg.add_text(default_value='Current pressure: ', tag='mntc_pr')
                                dpg.add_text(default_value='Current condition: ', tag='mntc_cnd')

def work_window_start():
    dpg.set_viewport_height(ww_height)
    dpg.set_viewport_width(ww_width)
    dpg.set_viewport_pos([view_pos[0]-70, view_pos[1]-100])
    dpg.configure_item(dpg.get_active_window(), show=False)
    dpg.configure_item(work_window, show=True)
    dpg.set_primary_window(window=work_window, value=True)



dpg.create_viewport(title='ktchk', small_icon='assets/img/qwerty.ico', resizable=False)
main_window()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_viewport_pos(view_pos)
dpg.start_dearpygui()
dpg.destroy_context()
