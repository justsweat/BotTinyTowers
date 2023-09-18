import numpy as np
import pyautogui
import cv2

import glob
import re
import time

# Own imports
import ttbot as t


def auto_elevator():
    print("-----------------------")
    print("Auto Elevator Bot Start")
    print("-----------------------")
    # For loop usage
    round = 1
    counter = 0

    while True:
        elevator_button = t.click_moving_object("elevator_button")
        if elevator_button:
            round += 1
            counter = 0

        if not elevator_button:
            counter += 1

        if counter == 20:
            print("Elevator stucked, end app")
            break

        image = t.get_screenshot()
        cv2.imshow("Auto Elevator", image)

        if cv2.waitKey(5000) == ord("q"):
            break

    cv2.destroyAllWindows()


auto_elevator()
