import numpy as np
import pyautogui
import cv2

import time
import glob
from pathlib import Path


import ttbot as t


def get_x_position(object):
    image = t.get_short_screenshot()
    image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    template = cv2.imread(f"object/{object}.png")
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # check it to set matching value
    locations = np.where(result >= threshold)  # get location if matched
    try:
        if locations[0][0]:
            return (locations[1][0], locations[0][0])
    except:
        return (0, 0)


def check_for_parachute_and_click(object):
    parachute = t.get_object_position(object)

    if parachute == (0, 0):
        return False

    if parachute:
        pt = (parachute[0] + 30, parachute[1] + 20)
        print(f"Found: {pt}")
        # pyautogui.moveTo(pt[0], pt[1])
        pyautogui.click(pt[0], pt[1])
        return True


def get_object_mid(object):
    btn = cv2.imread(f"object/{object}.png")
    hf, wf, c = btn.shape
    h = hf / 2
    w = wf / 2
    return (w, h)


def check_for_close_and_click(object):
    close_button = get_x_position(object)

    if close_button == (0, 0):
        return False

    if close_button:
        dm = get_object_mid(object)
        pt = (close_button[0] + dm[0], close_button[1] + dm[0] + 40)
        print(f"Found: {object}.png {pt}")
        # pyautogui.moveTo(pt[0], pt[1])
        pyautogui.click(pt[0], pt[1])
        return True


def got_crane():
    crane = t.get_object_position("crane")
    if crane[0] > 200:
        return True
    return False


def scroll_to_top():
    if got_crane():
        print("Already at top")
        return

    t.click_object("coins_min")
    return


def get_parachute_position(object):
    image = t.get_screenshot()
    image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    template = cv2.imread(f"object/{object}.png")
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # check it to set matching value
    locations = np.where(result >= threshold)  # get location if matched

    try:
        if locations[0][0]:
            return (locations[1][0], locations[0][0])
    except:
        return (0, 0)


def watch_gift():
    print("# Check for Gifts #")
    gift = t.click_object("gift_button")

    if not gift:
        print("No gift available now, check later")
        return

    if gift:
        time.sleep(1)
        open_gift = t.click_object("open_gift_button")

    if open_gift:
        time.sleep(1)
        continue_button = t.click_object("continue_button")

    if continue_button:
        x_first = t.click_object("x_button")

    if x_first:
        print("Exited to main")


def check_extra_popup():
    google_play = t.get_object_position("google_play")
    if google_play != (0.0):
        print("Extra pop up found, closing...")
        dm = get_object_mid("google_play")
        pt = (google_play[0] + dm[0] + 455, google_play[1] + dm[0])
        pyautogui.moveTo(pt[0], pt[1])
        pyautogui.click(pt[0], pt[1])
    return


def close_ads():
    print("Finding X button...", end="")
    close_buttons = glob.glob("object/ad_*.png")
    image = t.get_short_screenshot()

    for btn in close_buttons:
        object = Path(btn).stem
        close_clicked = check_for_close_and_click(object)
        if close_clicked:
            # time.sleep(0.5)
            # check_extra_popup()
            break

    if not close_clicked:
        print("no X is found, saving new X")
        image = t.get_top_screenshot()
        cv2.imwrite("object/top_screenshot.png", image)
        exit()

    if close_clicked:
        time.sleep(1)
        continue_1 = t.click_object("continue_button")

    if continue_1:
        time.sleep(0.5)
        continue_2 = t.click_object("continue_button")


def watch_parachute():
    print("Scanning for parachutes...", end="")
    parachutes = glob.glob("object/parachute_*.png")
    for parachute in parachutes:
        guy = Path(parachute).stem
        para = check_for_parachute_and_click(guy)
        if para:
            time.sleep(0.5)
            t.click_object("continue_button")
            time.sleep(1)
            golden_ticket = t.get_object_position("golden_ticket_icon")
            print("Got ads? ", end="")
            if golden_ticket[0] == 0:
                print("Watching ad now...")
                time.sleep(70)
                print("Times up")
                close_ads()
            else:
                print("No ads")
            break

    if not para:
        print("Not Found")
        return False
    return True


def ads():
    print("----------------------")
    print("Catching Parachute Bot")
    print("----------------------")
    stuck_counter = 0
    round = 1

    scroll_to_top()
    while True:
        print(f"Round {round}:", end="")
        if watch_parachute():
            stuck_counter = 0

        round += 1
        stuck_counter += 1

        if stuck_counter == 100:
            if t.click_object("continue_button"):
                ads()
            print("¯\_(ツ)_/¯  Stuck for 100 scans, end app")
            exit()

        # Do routine checks
        if round % 60 == 0:  # Every 5 minutes
            print("### Do a sweep ###")
            t.sweep_tower_for_object("white_box")

        if round % 720 == 0:  # Every hour
            print("### Do some routine checks ###")
            t.check_tech_point()
            t.check_raffle()
            t.check_stock_all()
            scroll_to_top()

        if cv2.waitKey(5000) == ord("q"):
            break


ads()
# close_ads()
# scroll_to_top()
# check_extra_popup()
# check_raffle()

# TODO find the dimension of the file, divide by 2, so shift it to the middle,
