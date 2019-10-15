from hwndInfo import get_hwnd_info
from cvUtils import identify_find_template_or_not
from cvUtils import multi_template_coordinate
from operation import mouse_move
from time import sleep
import pytesseract
import win32api
import time, datetime
import psutil
# while True:
#     a = identify_find_template_or_not("map_east.png", 0.95)
#     b = multi_template_coordinate("map_east.png", 0.95)
#     print(a,b)
#     # mouse_move(a[0],a[1])
#     sleep(0.5)

from readContentOfScreen import read_number_of_screen
from readContentOfScreen import read_chi_of_screen
# a = identify_find_template_or_not("map_east.png", 0.95)
while True:
    # print("东："+read_number_of_screen(489,73,513,87),end="")
    # print("  南："+read_number_of_screen(599,73,619,87))
    print(read_number_of_screen(419,273,433,292))
    sleep(0.5)

# win32api.SetCursorPos((1444,521))
# print(str(int(time.time())))