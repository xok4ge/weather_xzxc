import dearpygui.dearpygui as dpg
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
mw_width, mw_height = 400, 500

dpg.create_context()



def main_window():
    pass


def reg_user():
    pass


def reg_user_window():
    dpg.configure_item('main', show=False)
    dpg.configure_item('auth', show=True)
    dpg.set_primary_window(window=auth_window, value=True)


def login_user_window():
    pass


with dpg.font_registry():
    default_font = dpg.add_font(file='assets/fonts/dante.ttf', size=20)

with dpg.window(tag='auth', label='ffgm', no_resize=False, no_move=False, no_title_bar=False, show=False) as auth_window:
    with dpg.group(pos=[mw_width // 2-130, mw_height // 2-100]):
        dpg.add_text(default_value='username')
        username = dpg.add_input_text(no_spaces=True)
        dpg.add_text(default_value='password')
        password = dpg.add_input_text(password=True, no_spaces=True)
        dpg.add_spacer(height=5)
        apply = dpg.add_button(label='apply', width=100, callback=reg_user)

# help(dpg.window)
with dpg.window(tag='main', label='ffgm', no_resize=False, no_move=False, no_title_bar=False) as main_menu_window:
    with dpg.group(horizontal=True):
        title = dpg.add_text(default_value='ffgm.immo', pos=[mw_width // 2 - 100, mw_height // 2 - 100])
        dpg.bind_item_font(title, default_font)

    text = dpg.add_text(default_value='alpha vers', pos=[mw_width // 2 - 40, mw_height // 2 - 70])
    with dpg.group(horizontal=True, pos=[mw_width // 2-110, mw_height // 2-40]):
        register = dpg.add_button(label='register', callback=reg_user_window, width=100, height=30)
        login = dpg.add_button(label='login', callback=login_user_window, width=100, height=30)


dpg.create_viewport(title='Weather', width=mw_width, height=mw_height, small_icon='assets/img/qwerty.ico')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_viewport_pos([screensize[0]//2-70, screensize[1]//2-270])
dpg.set_primary_window(window=main_menu_window, value=True)
dpg.start_dearpygui()
dpg.destroy_context()
