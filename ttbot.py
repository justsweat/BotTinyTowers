import numpy as np
import pyautogui
import cv2

import time
import glob
import re
from pathlib import Path
from datetime import datetime, timedelta
import json


# Defining the nox player coordinates
x = 0  # top left coordinates
y = 0
width = 600
height = 1080
ys = 40
ht = 100

fnum_w = 30
fnum_h = 21


def get_screenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    return image[y : y + height, x : x + width]  # nox player roi


def get_short_screenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    return image[ys : ys + height, x : x + width]  # nox player roi


def get_top_screenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    return image[ys : ys + ht, x : x + width]  # nox player roi


def get_game_screenshot():
    image = get_screenshot()
    coins_min = get_object_position_precise("coins_min")
    if coins_min == (0, 0):
        print("Couldn't find Coins/Min, end app")
        exit()

    game_x = coins_min[0] - 75
    game_y = coins_min[1] - 20
    game_h = 770
    game_w = 312
    return image[game_y : game_y + game_h, game_x : game_x + game_w]


## Checks
def get_position(folder, object, threshold=0.9):
    image = get_screenshot()
    image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    template = cv2.imread(f"{folder}/{object}.png")
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)  # get location if matched
    try:
        if locations[0][0]:
            return (locations[1][0], locations[0][0])
    except:
        return (0, 0)


def get_object_position_precise(object, threshold=0.9):
    image = get_screenshot()
    image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    template = cv2.imread(f"object/{object}.png")
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)  # get location if matched
    try:
        if locations[0][0]:
            return (locations[1][0], locations[0][0])
    except:
        return (0, 0)


def get_object_position(object):
    image = get_screenshot()
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


def get_object_position_sweep(object, image):
    image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    template = cv2.imread(f"object/{object}.png")
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9  # check it to set matching value
    locations = np.where(result >= threshold)  # get location if matched
    try:
        if locations[0][0]:
            return (locations[1][0], locations[0][0])
    except:
        return (0, 0)


def got_crane():
    crane = get_object_position("crane")
    if crane[0] > 200:
        return True
    return False


## Click Objects
def click_object(object, offset=(0, 0)):
    print(f"Checking for {object} (fast)...", end="")
    first_loc = get_object_position(object)

    if first_loc == (0, 0):
        print("Not Found")
        return False

    if first_loc != (0, 0):
        pt = (first_loc[0] + 30 + offset[0], first_loc[1] + 20 + offset[1])
        print(f"Found: {pt}")
        time.sleep(1)
        pyautogui.moveTo(pt[0], pt[1])
        pyautogui.click(pt[0], pt[1])
        return True


def click_moving_object(object):
    print(f"Checking for {object}...", end="")
    first_loc = get_object_position(object)
    time.sleep(2)
    second_loc = get_object_position(object)

    if first_loc == (0, 0):
        print("Not Found")
        return False

    if first_loc == second_loc:
        pt = (first_loc[0] + 30, first_loc[1] + 20)
        print(f"Found: {pt}")
        time.sleep(1)
        pyautogui.moveTo(pt[0], pt[1])
        time.sleep(0.1)
        pyautogui.click(pt[0], pt[1])
        return True

    if first_loc != second_loc:
        print("First image moved..rechecking")
        click_moving_object(object)
        return True


def go_to_bottom():
    print("Going back to bottom")
    pyautogui.click(388, 958)
    time.sleep(1)


def go_to_top():
    if got_crane():
        print("Already at top")
        return

    print("Going to top")
    click_object("coins_min")
    return


def check_stock_all():
    print("-- Check for Stock All --")
    go_to_bottom()
    time.sleep(3)
    click_object("stock_all_button")
    time.sleep(1)
    yes = click_object("yes_button")

    if not yes:
        print("Don't need restock")
        print("-- End Check --")
        return False

    if yes:
        print("Stocks Refilled")
        time.sleep(1)
        click_object("continue_button")
        print("Exited back to main")
        print("-- End Check --")
        return True


def check_tech_point():
    print("-- Checking for Tech Point -- ")
    click_object("menu_button")
    time.sleep(1)
    tech_point = click_object("tech_point_button")
    if not tech_point:
        print("No tech point yet")
        click_object("x_button")
        return False

    collect_point = click_object("collect_point_button")

    if collect_point:
        click_object("awesome_button")
        print("Point Collected")
        time.sleep(0.5)
        x_first = click_object("x_button")
        time.sleep(0.5)
        x_second = click_object("x_button")
        print("Exited back to main")
        print("-- End Check --")
        return True


def join_raffle():
    click_object("menu_button")
    click_object("raffle_button")
    time.sleep(5)
    enter_clicked = click_object("enter_button")

    if enter_clicked:
        print("Entered raffle...", end="")
        now = datetime.now()
        json_string = json.dumps(now, default=str)
        with open("last_raffle.json", "w") as file:
            file.write(json_string)
        print("Updated last_raffle.json")
        time.sleep(2)
        continue_clicked = click_object("continue_button")

    if not enter_clicked:
        print("Joined")
        continue_clicked = True

    x_first = click_object("x_button")
    time.sleep(0.1)
    x_second = click_object("x_button")

    if x_second:
        print("Exited back to main")
        return True


def check_raffle():
    print("-- Checking for Raffle -- ")
    print("Can join raffle? ", end="")
    with open("last_raffle.json", "r") as file:
        last_raffle_string = json.load(file)

    last_raffle = datetime.strptime(last_raffle_string, "%Y-%m-%d %H:%M:%S.%f")
    next_raffle = last_raffle + timedelta(hours=1)
    next_raffle = next_raffle.replace(minute=0, second=0, microsecond=0)
    now = datetime.now()

    if now < next_raffle:
        print("Can't join raffle yet, check later")
        print("-- End Check --")
        return False

    if now > next_raffle:
        print("Can join raffle now")
        join_raffle()
        print("-- End Check --")
        return True


def scan_for_object(object):
    items = glob.glob(f"object/{object}_*.png")
    for item in items:
        item_stem = Path(item).stem
        pt = get_object_position_precise(item_stem)

        if pt != (0, 0):
            print(f"Found {item_stem}! {pt}")
            pyautogui.click(pt[0] + 10, pt[1] + 10)
            return True

        if pt == (0, 0):
            return False


def sweep_tower_for_object(object):
    print(f"-- Sweeping tower for {object} --")
    go_to_bottom()
    while True:
        scan_for_object(object)
        time.sleep(0.3)
        pyautogui.moveTo(100, 300)
        pyautogui.scroll(1)
        time.sleep(0.3)
        if got_crane():
            pyautogui.scroll(1)
            print("Reached Top, done sweeping")
            print("-- End Sweep --")
            return True


# For elevator
def get_fnum_image():
    elevator_pos = get_object_position_precise("elevator")

    fnum_x = elevator_pos[0] + 32
    fnum_y = elevator_pos[1] + 64

    time.sleep(1)
    image = get_screenshot()
    fnum_img = image[fnum_y : fnum_y + fnum_h, fnum_x : fnum_x + fnum_w]  # floor number roi

    # Modifying floor number image
    fnum_xw = int(fnum_img.shape[1] * 2)
    fnum_xh = int(fnum_img.shape[0] * 2)
    dim = (fnum_xw, fnum_xh)
    fnum_img = cv2.resize(fnum_img, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("floor_number_image.png", fnum_img)
    return cv2.cvtColor(fnum_img, cv2.COLOR_BGR2GRAY)


def get_nnum_image():
    elevator_pos = get_object_position_precise("elevator")

    fnum_x = elevator_pos[0]
    fnum_y = elevator_pos[1]
    fnum_w = 90
    fnum_h = 150

    nnum_x = elevator_pos[0] + 32
    nnum_y = elevator_pos[1] + 64
    nnum_w = 30
    nnum_h = 21

    time.sleep(1)
    image = get_screenshot()
    fnum_img = image[fnum_y : fnum_y + fnum_h, fnum_x : fnum_x + fnum_w]  # floor number roi
    nnum_img = image[nnum_y : nnum_y + nnum_h, nnum_x : nnum_x + nnum_w]  # floor number roi

    # Modifying floor number image
    fnum_xw = int(fnum_img.shape[1] * 2)
    fnum_xh = int(fnum_img.shape[0] * 2)
    dim = (fnum_xw, fnum_xh)
    fnum_img = cv2.resize(fnum_img, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("nnum/new_elevator_image.png", fnum_img)

    nnum_xw = int(nnum_img.shape[1] * 2)
    nnum_xh = int(nnum_img.shape[0] * 2)
    dim = (nnum_xw, nnum_xh)
    nnum_img = cv2.resize(nnum_img, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("nnum/new_nnum.png", nnum_img)

    return cv2.cvtColor(fnum_img, cv2.COLOR_BGR2GRAY)


def read_floor_number(image, threshold=0.99):
    print("Reading elevator button number...", end="")

    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    fnums = glob.glob("fnum/fnum_*.jpg")
    for fnum in fnums:
        template = cv2.imread(fnum)
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        if result[0][0] >= threshold:
            all_digits = re.findall(r"\d+", fnum)
            fnum_found = int(all_digits[0])
            print(fnum_found)
            return fnum_found

    print("Not Found")
    # This is to make sure there's no sudden pop-up of new shop
    time.sleep(1)
    continue_button = click_object("continue_button")
    if continue_button:
        return True

    cv2.imwrite("fnum/new_floor_number.jpg", image)
    scnshot = get_screenshot()
    cv2.imwrite("ending_screenshot.jpg", scnshot)
    print("Saved New Floor Image.. ending app")
    cv2.destroyAllWindows()
    exit()


def read_nnum(image, threshold=0.9):
    print("Reading new elevator number...")
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    nnums = glob.glob("nnum/nnum_*.png")
    digits = []
    all_digits = 0
    debug_nums = []
    found_left = False
    found_right = False
    found_mid = False

    for nnum in nnums:
        template = cv2.imread(nnum)
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        (y_points, x_points) = np.where(result >= threshold)

        for x, y in zip(x_points, y_points):
            debug_nums.append(x)
            if x > 89 and found_right == False:
                print("found right", nnum)  # Right num
                digits.append(re.findall(r"\d+", nnum)[0])
                all_digits += 1
                found_right = True

            if x < 76 and found_left == False:
                print("found left", nnum)  # Left Num
                digits.insert(0, re.findall(r"\d+", nnum)[0])
                all_digits += 1
                found_left = True

            if 76 <= x <= 89 and found_mid == False:  # Single Num
                print("found mid", nnum)
                digits = [(re.findall(r"\d+", nnum)[0])]
                all_digits = 2
                found_mid = True

            if all_digits == 2:
                print(digits)
                digits_str = "".join(digits)
                nnum_found = int(digits_str)
                return nnum_found

    if all_digits != 2:
        print(debug_nums)
        print("Not enough digits, ending app")
        cv2.destroyAllWindows()
        exit()


def read_tnum():
    image = get_screenshot()
    tnums = glob.glob(f"tnum/tnum_*.png")
    for tnum in tnums:
        tnum_stem = Path(tnum).stem
        tnum_exist = get_position("tnum", tnum_stem, 0.99)

        if tnum_exist != (0, 0):
            tnum_now = re.findall(r"\d+", tnum_stem)[0]
            print(f"Tower now: {tnum_now}")
            return True


def get_gt():
    with open("gt.json", "r") as file:
        return json.load(file)


## Ice Cream Event
def convert_cone():
    click_object("bing_ice")
    time.sleep(2)
    click_object("bing_exchange")
    time.sleep(1)
    if get_object_position_precise("claim_button") != (0, 0):
        click_object("claim_button")
    pyautogui.moveTo(300, 300)
    time.sleep(0.2)
    pyautogui.scroll(-1)
    time.sleep(1.5)
    in_progress = get_object_position_precise("bing_in_progress")
    if in_progress != (0, 0):
        print("Still converting, check later")
        click_object("x_button")
        return False
    time.sleep(0.2)
    bing_30m = click_object("bing_30m", (50, 50))
    time.sleep(1)
    click_object("x_button", (10, 10))
    return True


def check_stucked():
    stucked = []
    stucked.append(click_object("continue_button"))
    stucked.append(click_object("x_button"))
    stucked.append(check_stock_all())
    if True in stucked:
        print("Stucked fix")
        return False

    print("Still stucked, end app")
    cv2.destroyAllWindows()
    exit()
