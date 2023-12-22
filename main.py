import dearpygui.dearpygui as dpg
import ctypes
from db import *

conn = db_session()
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
smw_width, smw_height = 400, 500  # start_menu_window

dpg.create_context()


def main_window():
    if dpg.get_active_window():
        dpg.configure_item(dpg.get_active_window(), show=False)
    dpg.configure_item('main', show=True)
    if dpg.get_value('username_input'):
        dpg.set_value('username_input', '')
    if dpg.get_value('password_input'):
        dpg.set_value('password_input', '')
    dpg.set_primary_window(window=main_menu_window, value=True)


def reg_user(sender, app_data):
    dpg.set_value('error_reg', '')
    db_username = dpg.get_value('username_input')
    db_password = dpg.get_value('password_input')
    back = add_user(db_username, db_password, conn)
    if back:
        dpg.set_value('error_reg', f'user {back} already exists')


def reg_user_window():
    dpg.configure_item(dpg.get_active_window(), show=False)
    dpg.configure_item('auth', show=True)
    dpg.set_primary_window(window=auth_window, value=True)
    dpg.set_value('error_reg', '')


def login_user_window():
    pass


with dpg.font_registry():
    default_font = dpg.add_font(file='assets/fonts/dante.ttf', size=20)

with dpg.window(tag='auth', label='ffgm', no_resize=True, no_move=True, no_title_bar=False, show=False) as auth_window:
    with dpg.group(pos=[smw_width // 2 - 130, smw_height // 2 - 100]):
        dpg.add_text(default_value='username')
        dpg.add_input_text(no_spaces=True, tag='username_input')
        dpg.add_text(default_value='password')
        dpg.add_input_text(password=True, no_spaces=True, tag='password_input')
        dpg.add_spacer(height=5, width=10)
        dpg.add_button(label='apply', width=100, callback=reg_user)
        dpg.add_text(default_value='', color=(243, 201, 255), tag='error_reg')

    with dpg.menu_bar(tag='back_bar'):
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


dpg.create_viewport(title='Weather', width=smw_width, height=smw_height, small_icon='assets/img/qwerty.ico', resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_viewport_pos([screensize[0]//2-70, screensize[1]//2-270])
main_window()
dpg.start_dearpygui()
dpg.destroy_context()
