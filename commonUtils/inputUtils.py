import time
import keyboard_event
import msvcrt
import windowUtils
import pyperclip
import os


def input_with_txt_end_with_enter(filepath):
    with open(filepath, 'r') as f:
        # 按行读取，/n分割,输入之后按回车结束
        for line in f.readlines():
            windowUtils.set_foreground_window('MobaXterm')
            keyboard_event.key_input(line.strip())
            keyboard_event.input_enter()
            time.sleep(0.2)
            windowUtils.set_foreground_window('Administrator')
            time.sleep(0.1)
            msvcrt.getch()


def input_with_clipboard(filepath):
    for root, dirs, files in os.walk(filepath):
        for name in files:
            with open(os.path.join(root, name), 'r+') as f:
                input_content = f.read()
                pyperclip.copy(input_content)
                windowUtils.set_foreground_window('MobaXterm')
                time.sleep(1)
                msvcrt.getch()