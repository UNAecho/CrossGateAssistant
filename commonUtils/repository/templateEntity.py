import os
import cv2


# key值为模板名称，value为图片对应的cv2使用的BGR转化为GRAY数组，注意转换前是BGR不是RGB。type为ndarray。
# opencv所使用的读取图片方式与其他库不同，都是使用BGR形式，在其他库与其兼容时，需要注意
def generate_all_template_gray_ndarray_of_cv2():
    print("开始读取所有模板cv2的BGR对象")
    template_gray_ndarray_of_cv2 = {}
    for root, dirs, files in os.walk("ico"):
        for name in files:
            template_gray_ndarray_of_cv2[name] = cv2.imread(os.path.join(root, name), 0)
    return template_gray_ndarray_of_cv2
