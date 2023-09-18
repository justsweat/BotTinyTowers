import numpy as np
import pyautogui
import cv2

import glob
import re
import time
import json

# Own imports
import ttbot as t
import rebuild as r

# Defining the button area
btn_x = 7
btn_y = 865
btn_w = 300
btn_h = 75

# Defining the Floor Number area
fnum_w = 30
fnum_h = 21
fabove_x = 105
fabove_y = 431

# Total income
total_income = 0


def enlarge_img(image):
    image_xw = int(image.shape[1] * 2)
    image_xh = int(image.shape[0] * 2)
    dim = (image_xw, image_xh)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def confirm_floor(fnum_found):
    counter = 0

    while True:
        time.sleep(2)
        up_down = t.get_object_position_precise("up_down_button")

        if up_down == (0, 0):
            print("Reached floor")
            return True

        print("Didn't reached floor, moving one floor down")
        pyautogui.moveTo(300, 300)
        pyautogui.mouseDown()
        time.sleep(0.0070)
        pyautogui.mouseUp()
        counter += 1

        if counter == 5:
            print("Stuck for 5 times, adjust timing")
            adjust_fps(fnum_found)

            # send bits back to bottom and restart counter
            print("Sending bits up again")
            pyautogui.moveTo(300, 300)
            pyautogui.mouseDown()
            time.sleep(10)
            pyautogui.mouseUp()
            move_elevator(fnum_found)
            counter = 0


def move_elevator(fnum_found):
    fps = get_fps(fnum_found)
    hold = fps * fnum_found
    hold_rounded = round(hold, 2)

    print(f"Hold For: {hold_rounded}s (rate:{fps}, floor:{fnum_found})")

    pyautogui.moveTo(100, 300)
    pyautogui.mouseDown()
    time.sleep(hold_rounded)
    pyautogui.mouseUp()
    pyautogui.moveTo(2000, 300)
    return True


def send_bits_up():
    fnum_img = t.get_nnum_image()
    fnum_found = t.read_nnum(fnum_img, 0.9)
    move_elevator(fnum_found)

    # Check if reached floor
    confirm_floor(fnum_found)
    calc_income(fnum_found)
    return True


def check_up_down():
    while True:
        up_down = t.get_object_position_precise("up_down_button")
        if up_down != (0, 0):
            return True
        if up_down == (0, 0):
            t.click_object("continue_button")
            time.sleep(0.1)
            t.click_object("elevator_button")
            time.sleep(2)


def build_floor():
    t.go_to_top()
    time.sleep(2)
    t.click_object("build_floor_button")
    time.sleep(0.2)
    t.click_object("yes_button")
    time.sleep(0.2)
    continue_button = t.get_object_position_precise("continue_button")
    if continue_button != (0, 0):
        t.click_object("continue_button")
        return False
    return True


def app():
    print("------------------")
    print("Elevator Bot Start")
    print("------------------")
    # For loop usage
    round = 1
    counter = 0
    build_counter = 1
    complete = False
    tnum_now = 0

    # Run the elevator once if the up down button is present
    print("Checking for elevator mode...", end="")
    up_down_button = t.get_object_position_precise("up_down_button")
    if up_down_button != (0, 0):
        print("already in elevator mode, sending bits up")
        send_bits_up()
    else:
        print("not in elevator mode")

    # Checking the button area
    while True:
        image = t.get_screenshot()
        roi = image[t.y : t.y + t.height, t.x : t.x + t.width]  # nox player roi

        continue_button = t.get_object_position_precise("continue_button")
        if continue_button != (0, 0):
            t.click_object("continue_button")

        elevator_button = t.click_moving_object("elevator_button")
        if elevator_button:
            print("--------------------------------------")
            print(f"Round {round}: ", end="")
            time.sleep(2)  # delay for scroll to bottom animation
            check_up_down()  # make sure in elevator mode
            send_bits_up()
            complete = True

        if not elevator_button:
            counter += 1

        if counter == 30:
            print("Elevator stucked, check for stuck")
            stucked = t.check_stucked()
            if not stucked:
                counter = 0

        cv2.rectangle(roi, (btn_x, btn_y), (btn_x + btn_w, btn_y + btn_h), (0, 255, 0), 2)
        cv2.imshow("ROI", roi)

        if round % 15 == 0:
            build_floor()
            r.get_tower_num()
            tnum_now = t.read_tnum()
            t.sweep_tower_for_object("white_box")
            complete = True

        if round % 50 == 0:
            print(f"Round {round}: Routine checks")
            t.check_raffle()
            t.check_tech_point()
            complete = True

        if complete:
            counter = 0
            round += 1
            complete = False

        if tnum_now >= 50:
            r.rebuild()

        if cv2.waitKey(6000) == ord("q"):
            break

    cv2.destroyAllWindows()


def calc_income(fnum_found):
    S = 10.00 + 1.25  # Speed
    F = fnum_found  # Destination
    G = int(t.get_gt())  # Golden Tickets

    E = 0.05  # Exponential Growth L5
    L = 0.25  # Lift Boy Tips L5

    base_income = 50 + S * F * (1 + G)
    bonus = 1 + L + (F * E)

    income = round(base_income * bonus)

    global total_income
    total_income += income
    print(f"Income: {income:,} | Total income: {total_income:,}")
    print("--------------------------------------")
    return True


def get_fps(fnum_found):
    with open("fps.json", "r") as file:
        fps_dict = json.load(file)

    for key, value in fps_dict.items():
        lower_str, upper_str = key.split("-")
        lower, upper = int(lower_str), int(upper_str)

        if lower <= fnum_found <= upper:
            return value


def adjust_fps(fnum_found):
    with open("fps.json", "r") as file:
        fps_dict = json.load(file)

    for key, value in fps_dict.items():
        lower_str, upper_str = key.split("-")
        lower, upper = int(lower_str), int(upper_str)

        if lower <= fnum_found <= upper:
            fps_dict[key] = value + 0.0005

    with open("fps.json", "w") as file:
        json.dump(fps_dict, file, indent=4)

    print(f"Floor {fnum_found} was adjusted")
    return True


# *##############################
app()
# build_floor()
# t.convert_cone()
# confirm_floor()
# check_stucked()
# send_bits_up()
# get_fnum_image()
# check_stock_all()
