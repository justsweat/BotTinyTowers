#! Old timings
def get_fps(fnum_found):
    # Current Elevator 10.00 + 1.25)
    if fnum_found >= 80:  # ok
        return 0.0815  # (max) 0.0800 > 0.0815
    if fnum_found >= 75:  # ok 75, 77, 78, 81
        return 0.0820  # (max) 0.0805 > 0.0810 > 0.0820
    if fnum_found >= 70:  # ok 73
        return 0.0810  # (max) 0.0845 > 0.0810
    if fnum_found >= 65:  # ok 67
        return 0.0810  # (max) 0.0810 > 0.0805 > 0.0810
    if fnum_found >= 60:  # ok 59, 60, 61, 64
        return 0.0815  # (max) 0.0805 > 0.0810 > 0.0815
    if fnum_found >= 55:  # ok
        return 0.0810  # (max) 0.0800 > 0.0805 > 0.0810
    if fnum_found >= 50:  # ok
        return 0.0805  # (max) 0.0795 > 0.0800 > 0.0805
    if fnum_found >= 45:  # ok
        return 0.0805  # (max) 0.0795 > 0.0800 > 0.0805
    if fnum_found >= 40:  # ok 41, 42, 43
        return 0.0805  # (max) 0.0790 > 0.0800 > 0.0805
    if fnum_found >= 35:  # ok 37, 39
        return 0.0805  # (max) 0.0795 > 0.0800 > 0.0805
    if fnum_found >= 30:  # ok 37, 39
        return 0.0790  # (max) 0.0780 > 0.0790
    if fnum_found >= 25:  # ok 25, 28, 30
        return 0.0770  # (max) 0.0770 > 0.0760 > 0.0770
    if fnum_found >= 20:  # ok 22, 24
        return 0.0780  # (max) 0.0760 > 0.0770 > 0.0780
    if fnum_found >= 15:  # ok 15
        return 0.0750  # (max) 0.0730 > 0.0740 > 0.0750
    if fnum_found >= 10:  # ok
        return 0.0710  # (max) 0.0710 > 0.0700 > 0.0710
    if fnum_found >= 6:  # ok 8
        return 0.0660  # (max) 0.0550 > 0.0650 > 0.0660
    if fnum_found >= 5:  # ok 5
        return 0.0490  # (max) 0.0590 > 0.0500 > 0.0490
    if fnum_found >= 3:  # ok 4
        return 0.0350  # (max) 0.0390 > 0.0350
    return 0.0200  # ok


def get_fps_dict(fnum_found):
    fps_dict = {
        "80-100": 0.0815,
        "75-80": 0.0820,
        "70-75": 0.0810,
        "65-70": 0.0810,
        "60-65": 0.0815,
        "55-60": 0.0810,
        "50-55": 0.0805,
        "45-50": 0.0805,
        "40-45": 0.0805,
        "35-40": 0.0805,
        "30-35": 0.0790,
        "25-30": 0.0770,
        "20-25": 0.0780,
        "15-20": 0.0750,
        "10-15": 0.0710,
        "6-10": 0.0660,
        "5-6": 0.0490,
        "3-5": 0.0350,
        "1-3": 0.0200,
    }

    for key, value in fps_dict.items():
        lower_str, upper_str = key.split("-")
        lower, upper = int(lower_str), int(upper_str)

        if lower <= fnum_found <= upper:
            return value


import json

with open("fps.json", "r") as file:
    fps_dict = json.load(file)

print(fps_dict)
