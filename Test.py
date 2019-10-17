from time import sleep
from PIL import ImageGrab
import cv2
from PIL import Image
import os
import pytesseract
import win32api
import time, datetime
import psutil
from repository import CharacterAttribute
path = r"C:\study\CrossGateAssistant\ico\temp\train_ico"


for root, dirs, files in os.walk(path):
    for file in files:
        abs_path = os.path.join(root, file)
        img = cv2.imread(abs_path)
        # img = cv2.resize(im, (750, 130), interpolation=cv2.INTER_CUBIC)
        # cv2.imwrite(root+"\\"+str(int(time.time()))+".png", img)
        print("result : "+pytesseract.image_to_string(img,lang='num_money'))
        # Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        sleep(0.3)
# # win32api.SetCursorPos((1444,521))
# # print(str(int(time.time())))

# while True:
#     a=ImageGrab.grab((393,225,468,238))
#     a.save("ico//temp//"+str(int(time.time()))+".png")
#     sleep(0.5)
