import win32gui


# return : dict:coordinate of window
def get_hwnd_info(window_name):

    print("getHwndInfo()获取窗口信息")
    # 定义返回类型：dict
    return_result = dict()

    # 定义所有窗口句柄信息类型：字典
    hwnd_title = dict()

    # 获取所有窗口信息
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
    win32gui.EnumWindows(get_all_hwnd, 0)

    # 保存窗口句柄信息数组
    hwnd_array = []

    for handles_key, handles_value in hwnd_title.items():
        if window_name in handles_value:
            hwnd_array.append(handles_key)

    # # 获取窗口焦点
    # win32gui.SetForegroundWindow(omyuji_hwnd_array[0])

    for i in range(hwnd_array.__len__()):
        window_x_left, window_y_top, window_x_right, window_y_bottom = win32gui.GetWindowRect(hwnd_array[i])
        # 当前句柄所对应的坐标，在本辅助程序中经常使用
        window_info_dict = {"window_x_left": window_x_left,
                            "window_y_top": window_y_top,
                            "window_x_right": window_x_right,
                            "window_y_bottom": window_y_bottom
                            }
        # 返回当前窗口的坐标信息
        return_result[hwnd_array[i]] = window_info_dict

    return return_result
