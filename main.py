import dearpygui.dearpygui as dpg
import ctypes
from db import *
from config import *

conn = db_session()
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
view_pos = [screensize[0] // 2 - 70, screensize[1] // 2 - 270]


dpg.create_context()


# reg/log window block
def main_window():
    dpg.set_viewport_width(smw_width)
    dpg.set_viewport_height(smw_height)
    if dpg.get_active_window():
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
        dpg.set_value('error_log', f'user {back[1]} is not exist')
    else:
        dpg.set_value('error_log', 'success')
        work_window_start()


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
with dpg.window(tag='work_window', label='ffgm', no_resize=True, no_move=True, show=False) as work_window:
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
                with dpg.child_window():
                    with dpg.child_window(width=300, height=100):
                        pass

            with dpg.tab(label='Analyze'):
                pass


def work_window_start():
    dpg.set_viewport_height(ww_height)
    dpg.set_viewport_width(ww_width)
    dpg.set_viewport_pos([view_pos[0]+50, view_pos[1]-100])
    dpg.configure_item(dpg.get_active_window(), show=False)
    dpg.configure_item('work_window', show=True)
    dpg.set_primary_window(window=work_window, value=True)



dpg.create_viewport(title='ktchk', small_icon='assets/img/qwerty.ico', resizable=False)
main_window()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_viewport_pos(view_pos)
dpg.start_dearpygui()
dpg.destroy_context()
