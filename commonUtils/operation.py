import win32api
import win32con
from time import sleep
import keycode
import numpy as np
import cvUtils
import cv2 as opencv
from PIL import ImageGrab


# 鼠标点击操作
def mouse_click(x=None, y=None):
    if x is not None and y is not None:
        mouse_move(x, y)
        sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 带有视觉的鼠标点击操作，如果点击之后没反应，会做出布尔值返回
# x,y为鼠标点击坐标,点3次如果无效，返回True表示可能程序执行顺序发生了异常
def mouse_click_cv(x, y, template_name=None, window_info_tuple=None):
    for i in range(2):
        mouse_move(x, y)
        sleep(0.1)
        screen_before = np.array(ImageGrab.grab(window_info_tuple))
        mouse_click(x, y)
        sleep(0.5)
        screen_after = np.array(ImageGrab.grab(window_info_tuple))
        # 先是RGB转换为BGR，然后再转为灰度图
        gray_img_before = opencv.cvtColor(opencv.cvtColor(screen_before, opencv.COLOR_RGB2BGR), opencv.COLOR_BGR2GRAY)
        gray_img_after = opencv.cvtColor(opencv.cvtColor(screen_after, opencv.COLOR_RGB2BGR), opencv.COLOR_BGR2GRAY)

        match_res = opencv.matchTemplate(gray_img_before, gray_img_after, opencv.TM_CCOEFF_NORMED)

        loc = np.where(match_res > 0.99)
        for pt in zip(*loc[::-1]):
            if pt:
                print("点击" + str(template_name) + "没反应，重点")
                continue
        return


# 鼠标双击
def mouse_dclick(x=None, y=None):
    if x is not None and y is not None:
        mouse_move(x, y)
        sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 鼠标移动
def mouse_move(x, y):
    win32api.SetCursorPos((x, y))
    # windll.user32.SetCursorPos(x, y)


# 输入
def key_input(str):
    for c in str:
        win32api.keybd_event(keycode[c],0,0,0)
        sleep(0.01)
        win32api.keybd_event(keycode[c],0,win32con.KEYEVENTF_KEYUP,0)
        sleep(0.02)


# 鼠标拖拽至目标处
def mouse_drag_to_target(x, y, target_x, target_y):
    mouse_move(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    sleep(0.2)
    # GetSystemMetrics()函数参数为索引，共75个索引，具体可在网上查到
    # 目前我们仅需要第0索引：当前x轴分辨率；第1索引：当前y轴分辨率
    mw = int(target_x * 65535 / win32api.GetSystemMetrics(0))
    mh = int(target_y * 65535 / win32api.GetSystemMetrics(1))
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE + win32con.MOUSEEVENTF_MOVE, mw, mh, 0, 0)
    sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# win32con.MOUSEEVENTF_WHEEL代表鼠标中轮，第四个参数正数代表往上轮滚，负数代表往下

def scroll_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -256)


def wait_to_click(template_file_name):
    while True:
        aim_coordinate = cvUtils.identify_find_template_or_not(template_file_name, 0.8)
        if aim_coordinate:
            mouse_click(aim_coordinate['x'],['y'])
            break
        sleep(1)
    return
