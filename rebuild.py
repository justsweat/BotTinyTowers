import numpy as np
import pyautogui
import cv2

import time
import glob
from datetime import datetime
from pathlib import Path

import ttbot as t


def reset_tower():
    while True:
        menu = t.click_object("menu_button")
        if menu:
            break
        t.click_object("x_button")
        t.click_object("continue_button")

    t.click_object("rebuild_button")
    t.click_object("rebuild_tower_button")

    time.sleep(1)
    t.click_object("rebuild_confirm_button_blue")
    time.sleep(0.5)
    t.click_object("continue_button")


def click_mission_button():
    pt = t.get_object_position_precise("menu_button")
    mission_x = pt[0] - 440
    mission_y = pt[1] - 830
    pyautogui.moveTo(mission_x, mission_y)
    pyautogui.click(mission_x, mission_y)


def click_floor(fnum):
    pt = t.get_object_position_precise("menu_button")
    floor_x = pt[0] - 200
    floor_y = pt[1] - 235 - ((fnum - 1) * 135)

    pyautogui.moveTo(floor_x, floor_y)
    pyautogui.click(floor_x, floor_y)


def move_elevator_tuts():
    hold = 0.020

    print(f"Hold For: {hold}s")

    pyautogui.moveTo(100, 300)
    pyautogui.mouseDown()
    time.sleep(hold)
    pyautogui.mouseUp()
    return True


def complete_mission():
    click_mission_button()
    t.click_object("collect_bux_button")


def send_bits_up_tuts():
    t.click_object("elevator_button")
    move_elevator_tuts()
    return True


def do_task_1():
    print("# Task 1: Build Floor:")
    time.sleep(1)
    t.click_object("continue_button")
    t.click_object("build_floor_button")
    time.sleep(1)
    t.click_object("build_yes_button")
    complete_mission()


def do_task_2():
    print("# Task 2: Build Residential Floor")
    time.sleep(1)
    t.click_object("continue_button")
    click_floor(2)
    t.click_object("residential_floor_button")
    time.sleep(1)
    t.click_object("continue_button")
    complete_mission()


def do_task_3():
    print("# Task 3: Send bits up")
    time.sleep(1)
    t.click_object("continue_button")
    send_bits_up_tuts()
    time.sleep(3)
    t.click_object("continue_button")
    complete_mission()


def do_task_4():
    print("# Task 4: Build Food Floor")
    time.sleep(1)
    t.click_object("continue_button")
    t.click_object("build_floor_button")
    time.sleep(1)
    t.click_object("build_yes_button")
    click_floor(3)
    t.click_object("food_floor_button")
    time.sleep(1)
    t.click_object("continue_button")
    complete_mission()


def do_task_5():
    print("# Task 5: Hire Bits")
    time.sleep(1)
    t.click_object("continue_button")
    click_floor(3)
    t.click_object("hire_button")
    t.click_object("unemployed_button")
    time.sleep(1)
    t.click_object("hire_bits_button")
    time.sleep(1)
    t.click_object("continue_button")
    t.click_object("x_button")
    complete_mission()


def do_task_6():
    print("# Task 6: Stock Floor")
    time.sleep(1)
    t.click_object("continue_button")
    click_floor(3)
    t.click_object("upgrade_button", (10, 70))
    time.sleep(7)
    t.click_object("restock_button")
    # t.click_object("continue_button")
    complete_mission()


def do_task_7():
    ("# Task 7: Upgrade Floor")
    time.sleep(1)
    t.click_object("continue_button")
    click_floor(3)
    time.sleep(1)
    t.click_object("upgrade_button")
    time.sleep(1)
    t.click_object("yes_button")
    time.sleep(1)
    t.click_object("continue_button")
    t.click_object("x_button")
    complete_mission()
    t.click_object("collect_bux_button")


# Housekeeping
def delete_diner():
    # Remove worker
    click_floor(4)
    time.sleep(0.2)
    t.click_object("upgrade_button", (-120, 90))
    time.sleep(0.1)
    t.click_object("job_button")
    t.click_object("no_job_button")
    t.click_object("yes_button")

    # Remove worker
    click_floor(4)
    time.sleep(0.1)
    t.click_object("delete_button")
    time.sleep(0.1)
    t.click_object("yes_button")


def change_elevator():
    t.go_to_top()
    time.sleep(1)
    t.click_object("crane")
    time.sleep(0.1)
    t.click_object("customize_elevator_button")

    while True:
        t.click_object("left_button")
        time.sleep(0.2)
        switch = t.get_object_position_precise("switch_button")
        if switch != (0, 0):
            t.click_object("switch_button")
            break

    t.click_object("x_button")


def get_tower_num():
    now = datetime.now().strftime("%m%d%H%M%S")

    image = t.get_screenshot()
    tnums = glob.glob(f"tnum/tnum_*.png")
    for tnum in tnums:
        tnum_stem = Path(tnum).stem
        tnum_exist = t.get_position("tnum", tnum_stem, 0.99)

        if tnum_exist != (0, 0):
            print(f"Tnum exists: {tnum_stem}")
            return True

    tower_icon = t.get_object_position_precise("tower_icon")

    tower_x = tower_icon[0]
    tower_y = tower_icon[1]
    tower_w = 50
    tower_h = 24

    if tower_icon == (0, 0):
        print("can't find tower icon.. end app")
        exit()

    tnum_img = image[tower_y : tower_y + tower_h, tower_x : tower_x + tower_w]
    cv2.imwrite(f"tnum/tnum_new_{now}.png", tnum_img)


#######################
def housekeeping():
    # delete_diner()
    change_elevator()


def rebuild():
    reset_tower()
    do_task_1()
    do_task_2()
    do_task_3()
    do_task_4()
    do_task_5()
    do_task_6()
    do_task_7()
    time.sleep(1)
    housekeeping()


# *############


if __name__ == "__main__":
    get_tower_num()
    # opening()
    # housekeeping()
