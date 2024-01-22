import dearpygui.dearpygui as dpg
import ctypes
from datetime import datetime
from get_data import *
from pathlib import Path as pth
from date_picker import DatePicker
from db import *
from config import *


conn = db_session()
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
view_pos = [screensize[0] // 2 - 70, screensize[1] // 2 - 270]
dpg.create_context()

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
    print(app_data)

def render_vis_chart(df, period, date):
    render_data = get_render(df, [date.year, date.month, date.day])
    # main_params
    period, temp, wind, rnfl, moist, press, maxw = [list(map(float, render_data['Срок по Гринвичу'])),
                                              list(map(float, render_data['Температура воздуха по сухому термометру'])),
                                              list(map(float, render_data['Средняя скорость ветра'])),
                                              list(map(float, render_data['Сумма осадков за период между сроками'])),
                                              list(map(float, render_data['Относительная влажность воздуха'])),
                                              list(map(lambda x: x*0.75, map(float, render_data['Атмосферное давление на уровне станции']))),
                                              list(map(float, render_data['Максимальная скорость ветра']))]
    # sup_params
    syn_ind = str(int(render_data.iloc[0]['Синоптический индекс станции']))
    cl_cvr, cl_cvr_w = list(map(int, render_data['Общее количество облачности'])), ''
    if len(list(filter(lambda x: 5 <= x <= 13, cl_cvr))) > len(list(filter(lambda x: 0 <= x < 5, cl_cvr))):
        cl_cvr_w = 'cloudy'
    else:
        cl_cvr_w = 'clear'
    print(cl_cvr)


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

    dpg.set_value('an_ind', dpg.get_value('an_ind') + syn_ind)
    dpg.set_value('an_date', dpg.get_value('an_date') + str(date.date()))
    dpg.set_value('an_rfal', dpg.get_value('an_rfal') + str(round(sum(rnfl), 1)) + ' mm')
    dpg.set_value('an_cc', dpg.get_value('an_cc') + cl_cvr_w)
    dpg.set_value('an_maxw', dpg.get_value('an_maxw') + str(max(maxw)) + ' m/s')
    dpg.set_value('an_avtemp', dpg.get_value('an_avtemp') + str(round(sum(temp)/len(temp), 1)) + ' °C')
    dpg.set_value('an_mint', dpg.get_value('an_mint') + str(min(temp)) + ' °C')
    dpg.set_value('an_maxt', dpg.get_value('an_maxt') + str(max(temp)) + ' °C')
    dpg.set_value('an_avwind', dpg.get_value('an_avwind') + str(sum(wind)/len(wind)) + ' m/s')
    dpg.set_value('an_avpr', dpg.get_value('an_avpr') + str(round(sum(press)/len(press))) + ' mmHg')
    dpg.set_value('an_hum', dpg.get_value('an_hum') + str(round(sum(moist)/len(moist))) + ' %')



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
                    pass
                with dpg.menu(label='Extra'):
                    dpg.add_menu_item(label='Help')
                    dpg.add_menu_item(label='Credits')
                    dpg.add_menu_item(label='Exit', callback=main_window)
        with dpg.tab_bar(tag='Navigation'):
            with dpg.tab(label='Visualisation'):
                with dpg.child_window(autosize_x=True, autosize_y=True, no_scrollbar=True, no_scroll_with_mouse=True, border=False):
                    with dpg.group(horizontal=True) as grp:
                        with dpg.child_window(width=320, height=310, no_scroll_with_mouse=True, no_scrollbar=True):
                            with dpg.group(horizontal=True):
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
                                dpg.add_button(label='save to file', pos=[100, 290])

            with dpg.tab(label='Forecasting'):
                pass

            with dpg.tab(label='Monitoring'):
                pass

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
