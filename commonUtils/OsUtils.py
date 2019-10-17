import os
import operation
from time import sleep


# type :reset,shutdown,sleep
def shutdown_computer(self, type):
    sleep(1)
    operation.wait_to_click("start_button.png")
    sleep(1)
    operation.wait_to_click("shutdown.png")
    sleep(1)
    if type == "reset":
        operation.wait_to_click("reset.png")
    elif type == "shutdown":
        operation.wait_to_click("shutdown.png")
    else:
        operation.wait_to_click("sleep.png")
