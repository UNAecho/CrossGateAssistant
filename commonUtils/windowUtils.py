import win32gui
import time
time.sleep(1)
hwnd_title = dict()


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)


def set_foreground_window(window_name):
    for handles_key, handles_value in hwnd_title.items():
        if window_name in handles_value:
            win32gui.SetForegroundWindow(handles_key)
            break
