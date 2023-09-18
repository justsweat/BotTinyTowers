import numpy as np
import pyautogui
import cv2

import time
import glob
from pathlib import Path

import ttbot as t


def scan_for_object(object, limit=0):
    items = glob.glob(f"object/{object}_*.png")
    if not items:
        print("!! Item list is empty, recheck filename !!")
        exit()

    image = t.get_game_screenshot()
    for item in items:
        item_stem = Path(item).stem
        pt = t.get_object_position_sweep(item_stem, image)

        # Skip if the item is at the top area
        if pt[1] <= 65:  # might need adjustment
            continue

        if pt != (0, 0):
            global total_object
            total_object += 1
            print(f"Found {item_stem}! {pt} | Total Found: {total_object}")
            pyautogui.click(pt[0] + 167, pt[1] + 42)
            if total_object == limit:
                print("Found all, end app")
                exit()
            return True

        if pt == (0, 0):
            return False


def sweep_tower_for_object(object, limit):
    round = 1
    print(f"# Round {round}: Scanning for {object}")
    t.go_to_bottom()
    while True:
        scan_for_object(object, limit)
        time.sleep(0.5)
        pyautogui.moveTo(100, 300)
        pyautogui.scroll(1)
        time.sleep(0.5)
        if t.got_crane():
            print("Reached Top, go back to bottom")
            exit()
            image = t.get_screenshot()
            cv2.imshow("TT", image)
            if cv2.waitKey(3000) == ord("q"):
                exit()

            # Start next round
            round += 1
            print(f"# Round {round}: Scanning for fireworks")
            t.go_to_bottom()

            # Do routine checks
            if round % 20 == 0:
                continue
                print("Routine checks every 20 rounds")
                t.check_tech_point()
                t.check_stock_all()

        if cv2.waitKey(1) == ord("q"):
            break


# TODO if the pos is on the top area, skip
total_object = 0
limit = 5
object = "gold"
# object = "ice_popcicle"
# sweep_tower_for_object(object, limit)

# For Ice Cream Event
# sweep_tower_for_object("ice", 0)

# For lucky wheel ticket
sweep_tower_for_object("white_box", 0)
