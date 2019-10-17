import pytesseract
from PIL import ImageGrab
import shutil
from datetime import datetime
from screenshot import getScreenshot
import time
import os
from FileUtils import del_file_from_dir
import numpy as np
import cv2


# 读取截图中的数字，多数用于各种挑战的数量剩余
# params:
# file_path:识别图片的路径
# screenshot_x:被截图左上角那一点的x轴坐标
# screenshot_y:被截图左上角那一点的y轴坐标
# screenshot_wight_x:图片x轴长度
# screenshot_high_y:图片y轴长度

# 灰度以及二值化图片，将想要留下的target_pixel灰度值设置成0黑色，其它设置为255白色
# 理由是想做成白纸黑字的形式，便于OCR读取。
def gray_and_binaryzation(im, target_pixel):
    # point设定除了255白色的像素点，都转为纯黑色0像素，而其它任何颜色，都转为255白色。
    # lambda是隐式函数的写法，具体网上可以搜到用法。
    gray_im = im.convert(
        'L').point(lambda x: 0 if x == target_pixel else 255)
    return gray_im


# 去除噪音点，目前是去除【周围颜色都和自身不同的点】
def dislodge_noise_point(im, noise_pixel_value):
    # 获取宽度
    width = im.size[0]
    # 获取长度
    height = im.size[1]
    # 读取噪音点位置
    coordinate_info = np.where(np.array(im) == noise_pixel_value)
    # 由于where方法返回的是列list+行list索引下标，需要zip转化为(行+列)组合下标，便于使用。
    # where返回的list，1是行，0是列
    noise_coordinate_tuple = zip(*coordinate_info)
    for pt in noise_coordinate_tuple:
        # 注意下面im.getpixel所使用得x和y是坐标值，而pt包含的是行列值，二者顺序正好相反，需要反过来使用
        pt_x = int(pt[1])
        pt_y = int(pt[0])
        # pt为每个噪音点的索引下标元组
        # 开始循环判断像素八个方向的像素值时，首先判断是否是边界点，如果是，则直接置底色。以免后续计算时数组越界。
        if pt_x in [0, width - 1] or pt_y in [0, height - 1]:
            # print("噪音点 x:%d , y:%d 在图片四周，跳过去噪" % (pt_x, pt_y))
            im.putpixel((pt_x, pt_y), (255))
            continue
        # 本def核心算法，判断噪音点八个方向是否有和自己一样的点，如果没有，则判断为噪音点
        # 举例：(pt_x-1,pt_y-1)为当前pt的左上角一点
        if noise_pixel_value in [im.getpixel((pt_x - 1, pt_y - 1)), im.getpixel((pt_x - 1, pt_y)),
                                 im.getpixel((pt_x - 1, pt_y + 1)),
                                 im.getpixel((pt_x + 1, pt_y - 1)), im.getpixel((pt_x + 1, pt_y)),
                                 im.getpixel((pt_x + 1, pt_y + 1)),
                                 im.getpixel((pt_x, pt_y - 1)), im.getpixel((pt_x - 1, pt_y + 1))]:
            pass
        # 如果周围的点都跟自己不同，则视为噪音点，变为白色处理
        else:
            im.putpixel((pt_x, pt_y), (255))
    return im


def resize_img(input_img, width, hight):
    # 用cv2缩放图片,interpolation为插值方法，本次使用INTER_CUBIC，适用于图像放大
    img = cv2.resize(input_img, (width, hight), interpolation=cv2.INTER_CUBIC)
    return img


def read_number_of_screen(screenshot_x_left, screenshot_y_upper, screenshot_x_right, screenshot_y_bottom):
    # 截屏，图片直接加入内存中
    im = ImageGrab.grab((screenshot_x_left, screenshot_y_upper, screenshot_x_right, screenshot_y_bottom))
    # 灰度以及二值化，然后进行消噪。
    # 本次认为0像素黑点为干扰分析的噪音点，因为OCR想要读取的数字也是被处理为0像素
    im = dislodge_noise_point(gray_and_binaryzation(im, 255), 0)
    # PIL图片转化为cv2图片格式(RGB2BGR)
    im = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
    # 将图像缩放至960*560，方便识别
    im_cv2 = resize_img(im, 960, 560)
    read_screen_text = pytesseract.image_to_string(im_cv2, lang='num')
    if read_screen_text is None or "":
        print("没读出来，这程序写的什么破玩意")
    # 返回正常读出的int数字
    if read_screen_text.isdigit():
        return read_screen_text
    # 如果读出来非正常数字，保存为文件留以后训练集使用
    else:
        error_dir = "TestDir"
        error_file_list = os.listdir(error_dir)
        if error_file_list.__len__() > 100:
            del_file_from_dir(error_dir)
        cv2.imwrite(error_dir + "//error_num" + str(int(time.time())) + ".png",im)
    return read_screen_text
    # return "0"


# except Exception as e:
#     print("读取数字出错！错误信息：" + str(e))
#     # 输出读取错误的图片，方便人工debug原因
#     # 请定期清理文件，不然文件夹体积会越来越大
#     # error_image_filepath = 'errorImage\\' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png'
#     # shutil.copyfile(file_path, error_image_filepath)
#     # print("读取出错的图片路径为：" + error_image_filepath+"，请定期清理，防止文件夹越来越大")
#     return "0"


def read_chi_of_screen(screenshot_x_left, screenshot_y_upper, screenshot_x_right, screenshot_y_bottom):
    # 截屏，图片直接加入内存中
    im = ImageGrab.grab((screenshot_x_left, screenshot_y_upper, screenshot_x_right, screenshot_y_bottom))
    # 灰度以及二值化，然后进行消噪。
    # 本次认为0像素黑点为干扰分析的噪音点，因为OCR想要读取的数字也是被处理为0像素
    im = dislodge_noise_point(gray_and_binaryzation(im, 255), 0)
    # PIL图片转化为cv2图片格式(RGB2BGR)
    im = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
    # 将图像缩放至960*560，方便识别
    im_cv2 = resize_img(im, 960, 560)
    read_screen_text = pytesseract.image_to_string(im_cv2, lang='chi_sim')
    return read_screen_text
