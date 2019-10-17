import random
import time

import cv2 as opencv
import numpy as np
from PIL import ImageGrab
from repository import templateEntity
from hwndInfo import get_hwnd_info

# 获取窗口信息
hwnd_info = get_hwnd_info("魔力宝贝")
hwnd_array = list(hwnd_info.keys())
window_info_dict = hwnd_info[hwnd_array[0]]
window_info_tuple = tuple(window_info_dict.values())

if __name__ != 'main':
    template_cv2_entity = templateEntity.generate_all_template_gray_ndarray_of_cv2()


# threshold : 阈值，越接近1，匹配度要求越高。
# custom_coordinate : 自定义偏移量，用于自行修正坐标偏移量。
def identify_find_template_or_not(template_file_name, threshold, custom_coordinate=None):
    # 返回找到的坐标值，调用方需要根据返回值点击
    result_coordinates = {}
    # 读取cv2所使用的BGR模板
    template_imread = template_cv2_entity[template_file_name]
    if custom_coordinate is None:
        screen = np.array(ImageGrab.grab(window_info_tuple))
    else:
        custom_locale = (window_info_tuple[0] + custom_coordinate[0],
                         window_info_tuple[1] + custom_coordinate[1],
                         window_info_tuple[2] + custom_coordinate[2],
                         window_info_tuple[3] + custom_coordinate[3]
                         )
        screen = np.array(ImageGrab.grab(custom_locale))
    img_bgr = opencv.cvtColor(screen, opencv.COLOR_RGB2BGR)
    gray_img_for_cv2 = opencv.cvtColor(img_bgr, opencv.COLOR_BGR2GRAY)

    match_res = opencv.matchTemplate(gray_img_for_cv2, template_imread, opencv.TM_CCOEFF_NORMED)

    try:
        loc = np.where(match_res >= threshold)
        for pt in zip(*loc[::-1]):
            gps = pt
            # loc中为匹配处左上角位置，正常会加一点点偏移量以保证点到图片中间
            result_coordinates[0] = gps[0] + window_info_dict['window_x_left']
            result_coordinates[1] = gps[1] + window_info_dict['window_y_top']
    except UnboundLocalError:
        print("寻找模板出错了，推测为没找到，想要找的模板为： " + template_file_name)
        result_coordinates = {}
    # 索引0是x轴，1是y轴
    return result_coordinates


# 该方法返回多个模板的坐标
def multi_template_coordinate(template_file_name, threshold, custom_coordinate=None):
    # 返回找到的坐标值元组，调用方需要根据返回的字典进行拆包，得到坐标
    result_list = []
    # 读取cv2所使用的BGR模板
    template_imread = template_cv2_entity[template_file_name]
    if custom_coordinate is None:
        screen = np.array(ImageGrab.grab(window_info_tuple))
    else:
        custom_locale = (window_info_tuple[0] + custom_coordinate[0],
                         window_info_tuple[1] + custom_coordinate[1],
                         window_info_tuple[2] + custom_coordinate[2],
                         window_info_tuple[3] + custom_coordinate[3]
                         )
        screen = np.array(ImageGrab.grab(custom_locale))
    img_bgr = opencv.cvtColor(screen, opencv.COLOR_RGB2BGR)
    gray_img_for_cv2 = opencv.cvtColor(img_bgr, opencv.COLOR_BGR2GRAY)

    match_res = opencv.matchTemplate(gray_img_for_cv2, template_imread, opencv.TM_CCOEFF_NORMED)

    try:
        loc = np.where(match_res >= threshold)
        for pt in zip(*loc[::-1]):
            gps = pt
            # loc中为匹配处左上角位置，正常会加一点点偏移量以保证点到图片中间
            coordinates_x = gps[0] + window_info_dict['window_x_left']
            coordinates_y = gps[1] + window_info_dict['window_y_top']
            result_list.append((coordinates_x, coordinates_y))
    except UnboundLocalError:
        print("寻找模板出错了，推测为没找到，想要找的模板为： " + template_file_name)
        result_list = []

    return result_list
