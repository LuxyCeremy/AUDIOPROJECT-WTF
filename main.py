#!/usr/bin/evn python
# -*- coding: utf-8 -*-

import time
import random
import os
import threading

from launchpad_py import Launchpad
from tkinter import Tk, Checkbutton
from tkinter.filedialog import askopenfilename

import pyAA
import playAudio

FILE_NAME = ""
FILE_PATH = ""
R = 0
G = 0
R1 = 0
G1 = 0
CURRENT_POINT = 0
POINT_16 = [(i, 0) for i in range(8)] + [(8, t) for t in range(1, 9)]
inSquad = False
inSpread = False
TOTALCOUNT = 0
FAILURECOUNT = 0
LIGHT_DECREASE = 0
IS_NOT_AUTO = True
BUTTONID = -1
MODE = None


def buttonid_to_style(buttonid):
    pass
    if buttonid == -1:
        return random.randint(1, 4)
    x, y = KEY_TO_XY(buttonid)
    if 2 < x < 5 and 3 < y < 6:
        return 1
    elif 2 < x < 5 or 3 < y < 6:
        return 2
    elif x + 1 == y or x + y == 8:
        return 3
    else:
        return 4


def RANDOM_RGY(number):
    global LIGHT_DECREASE
    RGY = ((0 - LIGHT_DECREASE, 3 - LIGHT_DECREASE) \
               , (3 - LIGHT_DECREASE, 0 - LIGHT_DECREASE) \
               , (3 - LIGHT_DECREASE, 3 - LIGHT_DECREASE) \
               , (3 - LIGHT_DECREASE, 1 - LIGHT_DECREASE) \
               , (1 - LIGHT_DECREASE, 3 - LIGHT_DECREASE))
    # print([random.choice(RGY) for i in range(number)])
    return (random.choice(RGY) for i in range(number))


def KEY_TO_XY(key):
    Y = key // 16 + 1
    X = key % 16
    return (X, Y)


def samebeat(beatpointcut):
    miss = 0.05
    interval = []

    for i in range(len(beatpointcut) - 1):
        interval.append(beatpointcut[i + 1] - beatpointcut[i])
    # print(interval)
    if interval:
        if (max(interval) - min(interval) > miss):
            return False
        return True


def get_button_pressed():
    global BUTTONID
    timestart = time.time()
    if not IS_NOT_AUTO or MODE != 2:
        return -1
    while True:
        time.sleep(0.01)
        if BUTTONID != -1:
            temp_button_id, BUTTONID = BUTTONID, 0
            break
        if time.time() - timestart > 0.2:
            return -1
    return temp_button_id


def spread(key, launchpad, delay, STYLE):
    global inSpread
    x = 0
    y = 0
    if key is None:
        x = random.randint(0, 7)
        y = random.randint(1, 8)
    else:
        (x, y) = KEY_TO_XY(key)

    # print(x,y)
    [(R, G)] = RANDOM_RGY(1)
    launchpad.LedCtrlXY(x, y, R, G)

    lighted = [[False for i in range(8)] for t in range(8)]
    list_to_lightOn = []
    list_to_lightOff = []
    list_to_lightOn.append([x, y - 1])
    time1 = time.time()
    if STYLE == 1:
        while not len(list_to_lightOn) == 0:
            for ITEM in list_to_lightOff:
                if not inSquad:
                    launchpad.LedCtrlXY(ITEM[0], ITEM[1] + 1, 0, 0)
            list_to_lightOff = list_to_lightOn
            # print(len(list_to_lightOn))
            list2 = list_to_lightOn
            list_to_lightOn = []
            for get in list2:
                lighted[get[0]][get[1]] = True
                launchpad.LedCtrlXY(get[0], get[1] + 1, R, G)
                if get[1] + 1 < 8 and lighted[get[0]][get[1] + 1] == False and [get[0],
                                                                                get[1] + 1] not in list_to_lightOn:
                    list_to_lightOn.append([get[0], get[1] + 1])
                if get[1] - 1 >= 0 and lighted[get[0]][get[1] - 1] == False and [get[0],
                                                                                 get[1] - 1] not in list_to_lightOn:
                    list_to_lightOn.append([get[0], get[1] - 1])
                if get[0] + 1 < 8 and lighted[get[0] + 1][get[1]] == False and [get[0] + 1,
                                                                                get[1]] not in list_to_lightOn:
                    list_to_lightOn.append([get[0] + 1, get[1]])
                if get[0] - 1 >= 0 and lighted[get[0] - 1][get[1]] == False and [get[0] - 1,
                                                                                 get[1]] not in list_to_lightOn:
                    list_to_lightOn.append([get[0] - 1, get[1]])
            time.sleep(delay)
            # print(list_to_lightOff)
        for ITEM in list_to_lightOff:
            if not inSquad:
                launchpad.LedCtrlXY(ITEM[0], ITEM[1] + 1, 0, 0)
    if STYLE == 2:
        inSpread = True
        while not len(list_to_lightOn) == 0:
            list_to_lightOff.append(list_to_lightOn)
            # print(len(list_to_lightOn))
            list2 = list_to_lightOn
            list_to_lightOn = []
            for get in list2:
                lighted[get[0]][get[1]] = True
                launchpad.LedCtrlXY(get[0], get[1] + 1, R, G)
                if get[1] + 1 < 8 and lighted[get[0]][get[1] + 1] == False \
                        and [get[0], get[1] + 1] not in list_to_lightOn:
                    list_to_lightOn.append([get[0], get[1] + 1])
                if get[1] - 1 >= 0 and lighted[get[0]][get[1] - 1] == False \
                        and [get[0], get[1] - 1] not in list_to_lightOn:
                    list_to_lightOn.append([get[0], get[1] - 1])
                if get[0] + 1 < 8 and lighted[get[0] + 1][get[1]] == False \
                        and [get[0] + 1, get[1]] not in list_to_lightOn:
                    list_to_lightOn.append([get[0] + 1, get[1]])
                if get[0] - 1 >= 0 and lighted[get[0] - 1][get[1]] == False \
                        and [get[0] - 1, get[1]] not in list_to_lightOn:
                    list_to_lightOn.append([get[0] - 1, get[1]])
            time.sleep(delay)
        # print(list_to_lightOff)
        for sentence in list_to_lightOff:
            for ITEM in sentence:
                if not inSquad:
                    launchpad.LedCtrlXY(ITEM[0], ITEM[1] + 1, 0, 0)
            time.sleep(delay)
        inSpread = False
    print("deltatime:%f0\tspread style:%d" % (time.time() - time1, STYLE))
    # launchpad.Reset()


def spread_return(key, launchpad, interval):
    global inSpread
    x = 0
    y = 0
    if key is None:
        x = random.randint(0, 7)
        y = random.randint(1, 8)
    else:
        (x, y) = KEY_TO_XY(key)
        print("[[[[[[[[[[[[[[%d%d]]]]]]]]]]]]]" % (x, y))
    delay_rate = max(abs(x + y - 8), abs(y - x - 1))
    delay = (interval - 0.255) / (36 + (delay_rate * 4))
    [(R, G)] = RANDOM_RGY(1)
    launchpad.LedCtrlXY(x, y, R, G)

    lighted = [[False for i in range(8)] for t in range(8)]
    list_to_lightOn = []
    list_to_lightOff = []
    list_to_return = []
    list_to_lightOn.append([x, y - 1])
    timestart = time.time()
    inSpread = True
    while not len(list_to_lightOn) == 0:
        list_to_return.append(list_to_lightOn)
        list_to_lightOff.append(list_to_lightOn)
        # print(len(list_to_lightOn))
        list2 = list_to_lightOn
        list_to_lightOn = []
        for get in list2:
            lighted[get[0]][get[1]] = True
            launchpad.LedCtrlXY(get[0], get[1] + 1, R, G)
            if get[1] + 1 < 8 and lighted[get[0]][get[1] + 1] == False \
                    and [get[0], get[1] + 1] not in list_to_lightOn:
                list_to_lightOn.append([get[0], get[1] + 1])
            if get[1] - 1 >= 0 and lighted[get[0]][get[1] - 1] == False \
                    and [get[0], get[1] - 1] not in list_to_lightOn:
                list_to_lightOn.append([get[0], get[1] - 1])
            if get[0] + 1 < 8 and lighted[get[0] + 1][get[1]] == False \
                    and [get[0] + 1, get[1]] not in list_to_lightOn:
                list_to_lightOn.append([get[0] + 1, get[1]])
            if get[0] - 1 >= 0 and lighted[get[0] - 1][get[1]] == False \
                    and [get[0] - 1, get[1]] not in list_to_lightOn:
                list_to_lightOn.append([get[0] - 1, get[1]])
        time.sleep(delay)
    # print(list_to_lightOff)
    for sentence in list_to_lightOff:
        for ITEM in sentence:
            if not inSquad:
                launchpad.LedCtrlXY(ITEM[0], ITEM[1] + 1, 0, 0)
        time.sleep(delay)
    list_to_return_clone = list_to_return.copy()
    while list_to_return:
        for ITEM in list_to_return.pop():
            if not inSquad:
                launchpad.LedCtrlXY(ITEM[0], ITEM[1] + 1, R, G)
        time.sleep(delay)
    while list_to_return_clone:
        for ITEM in list_to_return_clone.pop():
            if not inSquad:
                launchpad.LedCtrlXY(ITEM[0], ITEM[1] + 1, 0, 0)
        time.sleep(delay)
    inSpread = False
    print("deltatime:%f0\tspread_return" % (time.time() - timestart))


def squad_part(launchpad, delay, style):
    global R, G, inSquad
    inSquad = True
    timestart = time.time()
    # launchpad.Reset()
    if style == 1:
        [(R, G)] = RANDOM_RGY(1)
        for x in range(4):
            for y in range(1, 5):
                # ---------<^-----------------
                launchpad.LedCtrlXY(x, y, R, G)
            time.sleep(delay)
    if style == 2:
        for x in range(4):
            for y in range(1, 5):
                # --------->_-----------------
                launchpad.LedCtrlXY(7 - x, 9 - y, R, G)
            time.sleep(delay)
    if style == 3:
        [(R, G)] = RANDOM_RGY(1)
        for x in range(4):
            for y in range(1, 5):
                # ---------<_-----------------
                launchpad.LedCtrlXY(y - 1, 8 - x, R, G)
            time.sleep(delay)

    if style == 4:
        for x in range(4):
            for y in range(1, 5):
                # --------->^-----------------
                launchpad.LedCtrlXY(8 - y, 1 + x, R, G)
            time.sleep(delay)
    if style == 5:
        for x in range(3, -1, -1):
            for y in range(4, 0, -1):
                # ---------<^-----------------
                launchpad.LedCtrlXY(x, y, 0, 0)
                # --------->_-----------------
                launchpad.LedCtrlXY(7 - x, 9 - y, 0, 0)
                # ---------<_-----------------
                launchpad.LedCtrlXY(y - 1, 8 - x, 0, 0)
                # --------->^-----------------
                launchpad.LedCtrlXY(8 - y, 1 + x, 0, 0)
            time.sleep(delay / 2)
        inSquad = False
    print("deltatime:%f0\tsquadpart" % (time.time() - timestart))


def squad_part_2(launchpad, delay, style):
    global R, G, inSquad
    [(R, G)] = RANDOM_RGY(1)
    inSquad = True
    timestart = time.time()
    # launchpad.Reset()
    if style == 31:
        for x in range(4):
            for y in range(1, 5):
                # ---------<^-----------------
                launchpad.LedCtrlXY(x, y, R, G)

                launchpad.LedCtrlXY(7 - x, 9 - y, R, G)
            time.sleep(delay)
    if style == 32:
        for x in range(4):
            for y in range(1, 5):
                # --------->_-----------------

                launchpad.LedCtrlXY(y - 1, 8 - x, R, G)
                launchpad.LedCtrlXY(8 - y, 1 + x, R, G)
            time.sleep(delay)
    if style == 33:
        for x in range(3, -1, -1):
            for y in range(4, 0, -1):
                # ---------<^-----------------
                launchpad.LedCtrlXY(x, y, 0, 0)
                # --------->_-----------------
                launchpad.LedCtrlXY(7 - x, 9 - y, 0, 0)
                # ---------<_-----------------
                launchpad.LedCtrlXY(y - 1, 8 - x, 0, 0)
                # --------->^-----------------
                launchpad.LedCtrlXY(8 - y, 1 + x, 0, 0)
            time.sleep(delay / 2)
        inSquad = False
    print("deltatime:%f0\tsquadpart" % (time.time() - timestart))


def instantAll(launchpad, delay):
    timestart = time.time()
    c = launchpad.LedGetColor(random.randint(2, 4), random.randint(2, 4))

    matrix = [c for i in range(64)]
    launchpad.LedCtrlRawRapid(matrix)
    time.sleep()
    launchpad.LedCtrlRawRapid([0 for i in range(64)])
    # launchpad.Reset()
    print("deltatime:%f\tinstantAll" % (time.time() - timestart))


def randomblink(launchpad, interval):
    c = launchpad.LedGetColor(random.randint(2, 4), random.randint(2, 4))
    timestart = time.time()
    [(R, G)] = RANDOM_RGY(1)
    for i in range(int(interval / 0.1)):
        for x in range(8):
            for y in range(1, 9):
                if random.randint(0, 1) == 1:
                    launchpad.LedCtrlXY(x, y, R, G)
        for x in range(8):
            for y in range(1, 9):
                launchpad.LedCtrlXY(x, y, 0, 0)

    print("deltatime:%f\trandomblink" % (time.time() - timestart))


def spin_thin(launchpad, delay, round=2):
    timestart = time.time()
    reverse = random.randint(0, 1)
    [(R, G)] = RANDOM_RGY(1)
    for r in range(round):
        for x in range(8):
            if inSquad or inSpread:
                return
            t = x
            if reverse == 1:
                t = 7 - x

            launchpad.LedCtrlXY(t, 1, R, G)
            launchpad.LedCtrlXY(7 - t, 8, R, G)
            launchpad.LedCtrlXY(0, 8 - t, R, G)
            launchpad.LedCtrlXY(7, t + 1, R, G)

            launchpad.LedCtrlXY((t - 1 + 2 * reverse) % 8, 1, 0, 0)
            launchpad.LedCtrlXY((7 - t + 1 - 2 * reverse) % 8, 8, 0, 0)
            launchpad.LedCtrlXY(0, (8 - t + 1 - 2 * reverse - 1) % 8 + 1, 0, 0)
            launchpad.LedCtrlXY(7, (t - 1 + 1 + 2 * reverse - 1) % 8 + 1, 0, 0)
            time.sleep(delay)
    launchpad.LedCtrlXY(7, 1, 0, 0)
    launchpad.LedCtrlXY(7, 8, 0, 0)
    launchpad.LedCtrlXY(0, 1, 0, 0)
    launchpad.LedCtrlXY(0, 8, 0, 0)
    print("deltatime:%f\tspin_thin" % (time.time() - timestart))


def spin_thin_loop(launchpad, interval):
    timestart = time.time()
    reverse = random.randint(0, 1)
    [(R, G)] = RANDOM_RGY(1)
    spin_round = int(interval / 0.22)
    for r in range(spin_round):
        if r % 4 == 0:
            [(R, G)] = RANDOM_RGY(1)
        for x in range(8):
            if inSquad or inSpread:
                return
            t = x
            if reverse == 1:
                t = 7 - x

            launchpad.LedCtrlXY(t, 1, R, G)
            launchpad.LedCtrlXY(7 - t, 8, R, G)
            launchpad.LedCtrlXY(0, 8 - t, R, G)
            launchpad.LedCtrlXY(7, t + 1, R, G)

            launchpad.LedCtrlXY((t - 1 + 2 * reverse) % 8, 1, 0, 0)
            launchpad.LedCtrlXY((7 - t + 1 - 2 * reverse) % 8, 8, 0, 0)
            launchpad.LedCtrlXY(0, (8 - t + 1 - 2 * reverse) % 8, 0, 0)
            launchpad.LedCtrlXY(7, (t - 1 + 1 + 2 * reverse) % 8, 0, 0)
            time.sleep(0.02)
    launchpad.LedCtrlXY(7, 1, 0, 0)
    launchpad.LedCtrlXY(7, 8, 0, 0)
    launchpad.LedCtrlXY(0, 1, 0, 0)
    launchpad.LedCtrlXY(0, 8, 0, 0)
    print("deltatime:%f\tspin_thin_loop" % (time.time() - timestart))


def spin(launchpad, delay, round):
    timestart = time.time()
    reverse = random.randint(0, 1)
    [(R, G)] = RANDOM_RGY(1)
    for r in range(round):
        for x in range(2, 6):
            if inSquad or inSpread:
                return
            t = x
            if reverse == 1:
                t = 7 - x

            launchpad.LedCtrlXY(t, 3, R, G)
            launchpad.LedCtrlXY(7 - t, 6, R, G)
            launchpad.LedCtrlXY(2, 8 - t, R, G)
            launchpad.LedCtrlXY(5, t + 1, R, G)

            launchpad.LedCtrlXY((t - 1 + 2 * reverse + 2) % 4 + 2, 3, 0, 0)
            launchpad.LedCtrlXY((7 - t + 1 - 2 * reverse + 2) % 4 + 2, 6, 0, 0)
            launchpad.LedCtrlXY(2, (8 - t + 1 - 2 * reverse + 2) % 4 + 2, 0, 0)
            launchpad.LedCtrlXY(5, (t - 1 + 1 + 2 * reverse + 2) % 4 + 2, 0, 0)
            time.sleep(delay)
    launchpad.LedCtrlXY(5, 3, 0, 0)
    launchpad.LedCtrlXY(5, 6, 0, 0)
    launchpad.LedCtrlXY(2, 3, 0, 0)
    launchpad.LedCtrlXY(2, 6, 0, 0)
    print("deltatime:%f\tspin" % (time.time() - timestart))


def randomchar(launchpad, interval):
    timestart = time.time()
    random_char = random.choice("AXHIUOV")
    [(R, G)] = RANDOM_RGY(1)
    for i in range(int(interval / 0.1)):
        if i % 2 == 0:
            random_char = random.choice("AXHIUOV")
        launchpad.LedCtrlChar(random_char, R, G)
        launchpad.LedCtrlRawRapid([0 for i in range(64)])
        R -= 1
        G -= 1
    print("deltatime:%f\trandomchar" % (time.time() - timestart))


def windcar(launchpad, delay, PERIOD, reverse):
    global inSpread, inSquad
    timestart = time.time()
    global R, G, R1, G1
    backbling = 2
    if PERIOD == 11:
        [(R, G), (R1, G1)] = RANDOM_RGY(2)
    for r in range(7 + backbling):

        for x in range(8):
            for y in range(1, 9):
                if inSpread or inSquad:
                    return
                    # <^
                ty = y
                if (reverse == 1 or PERIOD == 12) and not (reverse == 1 and PERIOD == 12):
                    ty = 9 - y
                if r < 7 and x <= 3 and y <= 4 and y - x == 4 - r:
                    launchpad.LedCtrlXY(x, ty, R, G)
                if r > 1 and x <= 3 and y <= 4 and y - x == 4 + backbling - r:
                    launchpad.LedCtrlXY(x, ty, 0, 0)
                # >_
                if r < 7 and x > 3 and y > 4 and y - x == r - 2:
                    launchpad.LedCtrlXY(x, ty, R, G)
                if r > 1 and x > 3 and y > 4 and y - x == r - 2 - backbling:
                    launchpad.LedCtrlXY(x, ty, 0, 0)
                # <_
                if r < 7 and x <= 3 and y > 4 and y + x == 11 - r:
                    launchpad.LedCtrlXY(x, ty, R1, G1)
                if r > 1 and x <= 3 and y > 4 and y + x == 11 + backbling - r:
                    launchpad.LedCtrlXY(x, ty, 0, 0)
                # >^
                if r < 7 and x > 3 and y <= 4 and y + x == 2 + backbling + r:
                    launchpad.LedCtrlXY(x, ty, R1, G1)
                if r > 1 and x > 3 and y <= 4 and y + x == 3 + r:
                    launchpad.LedCtrlXY(x, ty, 0, 0)

        time.sleep(delay)
    print("deltatime:%f\twindcar" % (time.time() - timestart))


def windcar2(launchpad, delay, PERIOD, reverse):
    timestart = time.time()
    global R, G
    if PERIOD == 21:
        [(R, G)] = RANDOM_RGY(1)
        for r in range(4):
            for x in range(8):
                for y in range(1, 9):
                    if (x == y - 1 or x + y == 8) and (x == 3 - r or x == 4 + r):
                        launchpad.LedCtrlXY(x, y, R, G)
            time.sleep((delay - 0.05) / 4)
    if PERIOD == 22:
        rangeV = range(1, 16)
        if reverse == 1:
            rangeV = range(15, 0, -1)
        launchpad.LedCtrlXY(3, 4, R, G)
        launchpad.LedCtrlXY(3, 5, R, G)
        launchpad.LedCtrlXY(4, 4, R, G)
        launchpad.LedCtrlXY(4, 5, R, G)
        for r in rangeV:
            if r % 5 == 0:
                launchpad.LedCtrlXY(1 + reverse + r // 5, 3, 0, 0)
                launchpad.LedCtrlXY(2 - reverse + r // 5, 3, R, G)

                launchpad.LedCtrlXY(6 - reverse - r // 5, 6, 0, 0)
                launchpad.LedCtrlXY(5 + reverse - r // 5, 6, R, G)

                launchpad.LedCtrlXY(5, 2 + reverse + r // 5, 0, 0)
                launchpad.LedCtrlXY(5, 3 - reverse + r // 5, R, G)

                launchpad.LedCtrlXY(2, 7 - reverse - r // 5, 0, 0)
                launchpad.LedCtrlXY(2, 6 + reverse - r // 5, R, G)
            if r % 3 == 0:
                launchpad.LedCtrlXY(0 + reverse + r // 3, 2, 0, 0)
                launchpad.LedCtrlXY(1 - reverse + r // 3, 2, R, G)

                launchpad.LedCtrlXY(7 - reverse - r // 3, 7, 0, 0)
                launchpad.LedCtrlXY(6 + reverse - r // 3, 7, R, G)

                launchpad.LedCtrlXY(6, 1 + reverse + r // 3, 0, 0)
                launchpad.LedCtrlXY(6, 2 - reverse + r // 3, R, G)

                launchpad.LedCtrlXY(1, 8 - reverse - r // 3, 0, 0)
                launchpad.LedCtrlXY(1, 7 + reverse - r // 3, R, G)
            if r % 2 == 0:
                launchpad.LedCtrlXY(-1 + reverse + r // 2, 1, 0, 0)
                launchpad.LedCtrlXY(0 - reverse + r // 2, 1, R, G)

                launchpad.LedCtrlXY(8 - reverse - r // 2, 8, 0, 0)
                launchpad.LedCtrlXY(7 + reverse - r // 2, 8, R, G)

                launchpad.LedCtrlXY(7, 0 + reverse + r // 2, 0, 0)
                launchpad.LedCtrlXY(7, 1 - reverse + r // 2, R, G)

                launchpad.LedCtrlXY(0, 9 - reverse - r // 2, 0, 0)
                launchpad.LedCtrlXY(0, 8 + reverse - r // 2, R, G)
            time.sleep((delay - 0.15) / 15)
    # launchpad.Reset()
    launchpad.LedCtrlRawRapid([0 for i in range(64)])
    print("deltatime:%f\twindcarII" % (time.time() - timestart))


def testblink(launchpad):
    launchpad.LedAllOn()
    time.sleep(0.05)
    launchpad.Reset()


def slash_spread(key, launchpad, delay, reverse):
    timestart = time.time()
    [(R, G)] = RANDOM_RGY(1)
    if key:
        (x, y) = KEY_TO_XY(key)
        if abs(x + y - 8) < abs(y - x - 1):
            reverse = 0
        if abs(x + y - 8) > abs(y - x - 1):
            reverse = 1
    for r in range(10):
        for x in range(8):
            t = x
            if reverse == 1:
                t = 7 - x
            for y in range(1, 9):
                if r < 8 and (y + x == 8 + r or y + x == 8 - r):
                    launchpad.LedCtrlXY(t, y, R, G)
                if r > 1 and (y + x == 6 + r or y + x == 10 - r):
                    launchpad.LedCtrlXY(t, y, 0, 0)
        time.sleep(delay)
    print("deltatime:%f\tslash_spread" % (time.time() - timestart))  # 0.13


def slash_spread2(key, launchpad, delay, reverse):
    timestart = time.time()
    [(R, G)] = RANDOM_RGY(1)
    if key:
        (x, y) = KEY_TO_XY(key)
        if abs(x + y - 8) < abs(y - x - 1):
            reverse = 0
        if abs(x + y - 8) > abs(y - x - 1):
            reverse = 1
    for r in range(16):
        for x in range(8):
            t = x
            if reverse == 1:
                t = 7 - x
            for y in range(1, 9):
                if r < 8 and (y + x == 8 + r or y + x == 8 - r):
                    launchpad.LedCtrlXY(t, y, R, G)
                if r > 7 and (y + x == 8 - 8 + r or y + x == 8 + 8 - r):
                    launchpad.LedCtrlXY(t, y, 0, 0)
        time.sleep(delay)
    print("deltatime:%f\tslash_spreadII" % (time.time() - timestart))


def edge_cut(launchpad, delay, reverse, PERIOD):
    timestart = time.time()
    [(R, G)] = RANDOM_RGY(1)
    rangeE = range(18)
    for r in rangeE:
        for x in range(8):
            for y in range(1, 5):
                tx, ty = x, y
                if PERIOD == 52:
                    tx, ty = 7 - x, 5 - y
                if reverse == 1:
                    tx, ty = ty - 1, tx + 1
                if r < 11:
                    if x + y == 11 - r:
                        launchpad.LedCtrlXY(tx, ty, R, G)
                        launchpad.LedCtrlXY(7 - tx, 9 - ty, R, G)
                if r > 6:
                    if x + y == 11 - r + 7:
                        launchpad.LedCtrlXY(tx, ty, 0, 0)
                        launchpad.LedCtrlXY(7 - tx, 9 - ty, 0, 0)
        time.sleep(delay)
    print("deltatime:%f\tedge_cut" % (time.time() - timestart))


def star_stream_get_txty(x, y, direction):
    if direction == 1:
        tx = x
        tx_shutdown = (tx - 1) % 8
        ty = y
        ty_shutdown = y
    if direction == 2:
        tx = 7 - x
        tx_shutdown = (tx + 1) % 8
        ty = 9 - y
        ty_shutdown = ty
    if direction == 3:
        tx = y - 1
        tx_shutdown = tx
        ty = x + 1
        ty_shutdown = (ty - 2) % 8 + 1
    if direction == 4:
        tx = 7 - (y - 1)
        tx_shutdown = tx
        ty = 9 - (x + 1)
        ty_shutdown = (ty - 1) % 8 + 2
    return (tx, ty, tx_shutdown, ty_shutdown)


def star_stream(launchpad, interval):
    timestart = time.time()
    stars = []
    DIRECTION = random.randint(1, 4)
    stars_count = int((interval - 0.4) / 0.0667)
    stars_to_pop = []
    last_two_y = []
    for r in range(stars_count + 8):

        if r < stars_count:
            y = -1
            while y == -1 or y in last_two_y:
                y = random.randint(1, 8)
            [(temp_color_r, temp_color_g)] = RANDOM_RGY(1)
            stars.append((0, y, temp_color_r, temp_color_g))
            last_two_y.append(y)
            if len(last_two_y) > 2:
                last_two_y.pop(0)
        for i in range(len(stars)):
            (x, y, temp_color_r, temp_color_g) = stars[i]
            (tx, ty, tx_shutdown, ty_shutdown) = star_stream_get_txty(x, y, DIRECTION)

            launchpad.LedCtrlXY(tx, ty, temp_color_r, temp_color_g)
            launchpad.LedCtrlXY(tx_shutdown, ty_shutdown, 0, 0)
            if x == 7:
                stars_to_pop.append(i)
            else:
                stars[i] = (x + 1, y, temp_color_r, temp_color_g)
        time.sleep(0.05)
        for stp in stars_to_pop:
            (x, y, r, g) = stars.pop(stp)
            (tx, ty, tx_shutdown, ty_shutdown) = star_stream_get_txty(x, y, DIRECTION)
            launchpad.LedCtrlXY(tx, ty, 0, 0)
        stars_to_pop = []
    print("deltatime:%f\tstar_stream" % (time.time() - timestart))


def snake_key_locate(key, x, y):
    if key and key != -1:
        if KEY_TO_XY(key) == (3, 4):
            tx, ty = x, y
        elif KEY_TO_XY(key) == (3, 5):
            tx, ty = x, 9 - y
        elif KEY_TO_XY(key) == (4, 5):
            tx, ty = 9 - x, 9 - y
        elif KEY_TO_XY(key) == (4, 4):
            tx, ty = 9 - x, y
    else:
        tx,ty = x,y
    return tx, ty


def spread_snake(key, launchpad, delay):
    timestart = time.time()
    # 空间换时间
    key_to_spread = [(4, 4), (4, 5), (5, 5), (5, 4),  # 1
                     (5, 3), (4, 3), (3, 3), (3, 4), (3, 5), (3, 6), (4, 6), (5, 6), (6, 6), (6, 5), (6, 4), (6, 3),
                     # 2
                     (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
                     (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (7, 6), (7, 5), (7, 4), (7, 3), (7, 2),  # 3
                     (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1),
                     (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
                     (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8),
                     (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1)]  # 4
    tail_length = 5
    [(r, g)] = RANDOM_RGY(1)
    for i in range(len(key_to_spread) + tail_length):
        if i < len(key_to_spread):
            x, y = key_to_spread[i]
            tx, ty = snake_key_locate(key, x, y)
            launchpad.LedCtrlXY(tx - 1, ty, r, g)
        if i > tail_length - 1:
            x, y = key_to_spread[i - tail_length]
            tx, ty = snake_key_locate(key, x, y)
            launchpad.LedCtrlXY(tx - 1, ty, 0, 0)
        time.sleep(delay)
    print("deltatime:%f\tspread_snake" % (time.time() - timestart))


def spread_square(key, launchpad, delay):
    timestart = time.time()
    if key:
        key_x, key_y = KEY_TO_XY(key)
    else:
        key_x = random.randint(0, 7)
    [(r, g)] = RANDOM_RGY(1)
    if 2 < key_x < 5:
        for round_r in range(4):
            for x in range(8):
                for y in range(1, 9):
                    if x == 4 + round_r or x == 3 - round_r:
                        launchpad.LedCtrlXY(x, y, r, g)
            time.sleep(delay)
        for round_r in range(4):
            for x in range(8):
                for y in range(1, 9):
                    if x == 4 + round_r or x == 3 - round_r:
                        launchpad.LedCtrlXY(x, y, 0, 0)
            time.sleep(delay)
    else:
        for round_r in range(4):
            for x in range(8):
                for y in range(1, 9):
                    if y == 5 + round_r or y == 4 - round_r:
                        launchpad.LedCtrlXY(x, y, r, g)
            time.sleep(delay)
        for round_r in range(4):
            for x in range(8):
                for y in range(1, 9):
                    if y == 5 + round_r or y == 4 - round_r:
                        launchpad.LedCtrlXY(x, y, 0, 0)
            time.sleep(delay)
    print("deltatime:%f\tspread_square" % (time.time() - timestart))
    pass


def flash(beatpoint, beatmain, beatsecond):  # 用来瞎JB闪的模块
    '''

    :param beatpoint:
    节拍点
    :param beatmain:
    强节拍系数
    :param beatsecond:
    一个判断是否是长节拍的临界秒数
    :return:
    返回个P，用来终止的
    '''
    while not playAudio.isplaying():
        pass
        time.sleep(0.01)
    print("[AUDIO IS PLAYING]%f" % time.time())
    timestart = time.time()
    inCircle = -1  # 有很多动画不是一拍就能完成的，如果没有完成，不会生成新的动画，直到这一动画序列结束
    REVERSE = 0  # 由于某些连续动画的方向是相关的，存在这里方便调用
    # for i in range(len(beatpoint)):
    i = 0
    while i < len(beatpoint):
        interval = -1.0
        if (i < len(beatpoint) - 1):
            interval = beatpoint[i + 1] - beatpoint[i]  # 计算与下一个音符的间隔，决定使用长节拍动画还是短节拍动画
            print("[interval]%f" % interval, end="\t")
        while time.time() - timestart < beatpoint[i]:
            # 如果从开始播放到现在的时间还没到绝对节拍时间，那就sleep
            # 这一条保证了任何一个节拍的误差都在10ms之内
            # 也保证了不会出现单线程的脱节情况
            time.sleep(0.01)
        flash_thread = None  # 一开始动画不设置

        # ---------------------------
        if interval < 0:  # END
            launchpad.LedCtrlString("END", 3, 3, direction=-1, waitms=30)
            launchpad.LedAllOn(0)
            launchpad.Close()  # 防止报错，记得关闭
            return
        if interval > 6 * beatsecond:
            while True and i < len(beatpoint) - 2:
                temp_interval = beatpoint[i + 2] - beatpoint[i + 1]

                if temp_interval > 6 * beatsecond:
                    interval += temp_interval
                    i = i + 1
                else:
                    break
            print("{%d}{%f}" % (i, interval))
            flash_thread = threading.Thread(target=star_stream,
                                            args=(launchpad, interval))
        elif interval > 2 * beatsecond:
            temp_button_id = get_button_pressed()
            button_style = buttonid_to_style(temp_button_id)
            print("{BUTTON STYLE}%d" % button_style)
            if button_style == 1:
                flash_thread = threading.Thread(target=spread_snake,
                                                args=(temp_button_id if temp_button_id != -1 else None,
                                                      launchpad,
                                                      (interval - 0.15) / 64))

            elif button_style == 3:
                flash_thread = threading.Thread(target=slash_spread2,
                                                args=(
                                                    temp_button_id if temp_button_id != -1 else None,
                                                    launchpad,
                                                    (interval - 0.13) / 24, random.randint(0, 1)))
            else:
                flash_thread = threading.Thread(target=spread_return,
                                                args=(
                                                    temp_button_id if temp_button_id != -1 else None, launchpad,
                                                    interval))

        elif inCircle == -1:
            if beatmain[i] < 0.005:  # 如果强节拍系数小于5毫秒就判断是一个强拍（然而真正的强拍差都是0.0f，我这就算网开拌面了）
                if interval > beatsecond:  # 如果是一个长拍
                    style = random.randint(1, 6)
                    if True:
                        temp_button_id = get_button_pressed()
                        button_style = buttonid_to_style(temp_button_id)
                        print("{BUTTON STYLE}%d" % button_style)
                        if button_style == 1:
                            flash_thread = threading.Thread(target=spin,
                                                            args=(
                                                                launchpad,
                                                                (interval - 0.15) / 16 if interval > 0.15 else 0,
                                                                4))
                        if button_style == 2:
                            flash_thread = threading.Thread(target=spread_square,
                                                            args=(
                                                                temp_button_id if temp_button_id != -1 else None,
                                                                launchpad,
                                                                (interval - 0.15) / 8))
                        if button_style == 3:  # LONG
                            flash_thread = threading.Thread(target=slash_spread,
                                                            args=(
                                                                temp_button_id if temp_button_id != -1 else None,
                                                                launchpad,
                                                                (interval - 0.13) / 15, random.randint(0, 1)))

                        if button_style == 4:
                            if style == 1 and samebeat(beatpoint[i:i + 4]):
                                inCircle = 31
                            elif style == 2 and samebeat(beatpoint[i:i + 3]):
                                inCircle = 51
                            else:
                                flash_thread = threading.Thread(target=spread,
                                                                args=(
                                                                    temp_button_id if temp_button_id != -1 else None,
                                                                    launchpad,
                                                                    (interval - 0.13) / 16, 1))

                        if flash_thread is None and inCircle == -1:
                            flash_thread = threading.Thread(target=spread,
                                                            args=(
                                                                temp_button_id if temp_button_id != -1 else None,
                                                                launchpad,
                                                                (interval - 0.13) / 32, 2))

                else:  # 如果是一个短拍
                    style = random.choice([1, 2, 3])
                    if style == 2:
                        flash_thread = threading.Thread(target=spin,
                                                        args=(
                                                            launchpad, (interval - 0.15) / 8 if interval > 0.15 else 0,
                                                            2))
                    if style == 1:  # SHORT
                        flash_thread = threading.Thread(target=randomblink, args=(launchpad, interval))
                    if style == 3:  # SHORT
                        flash_thread = threading.Thread(target=spin_thin,
                                                        args=(
                                                            launchpad, (interval - 0.15) / 8 if interval > 0.15 else 0,
                                                            1))

            else:  # 如果不是强拍
                if interval > beatsecond:  # 如果是一个长拍
                    style = random.choice([4, 5])
                    if style == 4:
                        if samebeat(beatpoint[i:i + 6]):
                            inCircle = 1
                    if style == 5:
                        if samebeat(beatpoint[i:i + 3]):
                            inCircle = 51
                        REVERSE = random.randint(0, 1)
                    if flash_thread is None and inCircle == -1:
                        flash_thread = threading.Thread(target=spin_thin,
                                                        args=(
                                                            launchpad, (interval - 0.15) / 16 if interval > 0.15 else 0,
                                                            2))
                else:  # 如果是一个短拍
                    style = random.choice([1, 3, 7, 8])
                    if style == 7:
                        if samebeat(beatpoint[i:i + 3]):
                            inCircle = 11
                            REVERSE = random.randint(0, 1)

                    if style == 8:
                        if samebeat(beatpoint[i:i + 3]):
                            inCircle = 21
                            REVERSE = random.randint(0, 1)
                    if style == 3:  # SHORT
                        flash_thread = threading.Thread(target=spin_thin,
                                                        args=(
                                                            launchpad, (interval - 0.15) / 8 if interval > 0.15 else 0,
                                                            1))
                    if inCircle == -1 and flash_thread is None:  # SHORT
                        flash_thread = threading.Thread(target=randomchar, args=(launchpad, interval))
        if inCircle != -1:
            print("[{:-^60}]".format("inCircle:%d" % inCircle))
            # 进行完上面的分配工作之后，如果分配到多段动画，那么紧接着就进入这部分
            # 当多段动画结束前不会进入上面那部分
            # 如你所见，每个不重复的范围代表一个完整的动画
            if inCircle in range(1, 6):
                flash_thread = threading.Thread(target=squad_part, args=(launchpad, interval / 5, inCircle))
                inCircle += 1
                if inCircle == 6:
                    inCircle = -1
                pass
            if inCircle in range(11, 13):

                flash_thread = threading.Thread(target=windcar,
                                                args=(launchpad, (interval - 0.125) / 10, inCircle, REVERSE))
                inCircle += 1
                if inCircle == 13:
                    inCircle = -1
                pass
            if inCircle in range(21, 23):

                flash_thread = threading.Thread(target=windcar2, args=(launchpad, interval, inCircle, REVERSE))
                inCircle += 1
                if inCircle == 23:
                    inCircle = -1
            if inCircle in range(31, 34):

                flash_thread = threading.Thread(target=squad_part_2, args=(launchpad, interval / 5, inCircle))
                inCircle += 1
                if inCircle == 34:
                    inCircle = -1
            if inCircle in range(51, 53):

                flash_thread = threading.Thread(target=edge_cut,
                                                args=(launchpad, (interval - 0.13) / 18, REVERSE, inCircle))
                inCircle += 1
                if inCircle == 53:
                    inCircle = -1
        # ----------------------------
        if flash_thread == None:
            flash_thread = threading.Thread(target=testblink, args=(launchpad,))
            # 如果到这里什么都没分配进来，那么闪烁警告

        flash_thread.start()
        i += 1


def blink_point(launchpad):
    global CURRENT_POINT
    (X, Y) = POINT_16[CURRENT_POINT]
    (X1, Y1) = POINT_16[CURRENT_POINT - 1 if CURRENT_POINT > 0 else 15]
    (r, g) = (3, 3) if IS_NOT_AUTO else (0, 3)
    launchpad.LedCtrlXY(X, Y, r, g)
    launchpad.LedCtrlXY(X1, Y1, 0, 0)
    CURRENT_POINT += 1
    if CURRENT_POINT == 16:
        CURRENT_POINT = 0


def flash2(mainbeatpoint):
    while not playAudio.isplaying():
        pass
        time.sleep(0.01)
    print("[AUDIO IS PLAYING]%f" % time.time())
    timestart = time.time()
    for i in range(len(mainbeatpoint)):
        while time.time() - timestart < mainbeatpoint[i]:
            # 如果从开始播放到现在的时间还没到绝对节拍时间，那就sleep
            # 这一条保证了任何一个节拍的误差都在10ms之内
            # 也保证了不会出现单线程的脱节情况
            time.sleep(0.01)
        blink_point(launchpad)


def input2(mainbeatpoint, beatsecond):
    global TOTALCOUNT, FAILURECOUNT, LIGHT_DECREASE, BUTTONID, IS_NOT_AUTO
    while not playAudio.isplaying():
        pass
        time.sleep(0.01)
    print("[AUDIO IS PLAYING]%f" % time.time())
    timestart = time.time()
    for i in range(len(mainbeatpoint)):
        while time.time() - timestart < mainbeatpoint[i] - 0.2:
            # 如果从开始播放到现在的时间还没到绝对节拍时间，那就sleep
            # 这一条保证了任何一个节拍的误差都在10ms之内
            # 也保证了不会出现单线程的脱节情况
            launchpad.ButtonFlush()
            time.sleep(0.01)
        BUTTONID = -1
        while time.time() - timestart < mainbeatpoint[i] + 0.2:
            a = launchpad.EventRaw()

            time.sleep(0.01)
            if a != []:
                launchpad.ButtonFlush()
                print(a)
                if a[0][0][2] == 127:
                    TOTALCOUNT += 1
                    FAILURECOUNT = 0
                    BUTTONID = a[0][0][1]
                    if KEY_TO_XY(BUTTONID) in POINT_16:
                        IS_NOT_AUTO = False
                        BUTTONID = -1
                        LIGHT_DECREASE = 0
                    elif not IS_NOT_AUTO:
                        IS_NOT_AUTO = True
                        FAILURECOUNT = 0
                        LIGHT_DECREASE = 0
                    # print("[{:_^30}]".format(TOTALCOUNT))
                    break
        else:
            if i + 1 < len(mainbeatpoint) and mainbeatpoint[i + 1] - mainbeatpoint[i] < 6 * beatsecond:
                FAILURECOUNT += 1
                # print("[{:^^30}]".format(FAILURECOUNT))
            else:
                FAILURECOUNT = 0
        if IS_NOT_AUTO == True:
            if FAILURECOUNT < 4:
                LIGHT_DECREASE = 0
            elif FAILURECOUNT < 6:
                LIGHT_DECREASE = 1
            elif FAILURECOUNT < 8:
                LIGHT_DECREASE = 2
            else:
                LIGHT_DECREASE = 3


def START(data=None, rewrite=False):
    if not data:
        data = eval(pyAA.getbeatpoint(FILE_NAME, FILE_PATH, rewrite))
    tempo = data[0]
    beatpoint = data[1]
    beatmain = data[2]
    print("[TEMPO]:%f" % tempo)
    print("[TOTAL BEATPOINT]:%d" % len(beatpoint))
    print("[STARTFLASH]%f" % time.time())
    flash_thread = threading.Thread(target=flash, args=(beatpoint, beatmain, 55 / tempo))
    flash_thread.start()
    playAudio.play(FILE_PATH)
    os._exit(0)


def START2():
    data = eval(pyAA.getbeatpoint(FILE_NAME, FILE_PATH))
    mode2_beatpoint = data[3]
    tempo = data[0]
    flash2_thread = threading.Thread(target=flash2, args=(mode2_beatpoint,))
    flash2_thread.start()
    input_thread = threading.Thread(target=input2, args=(mode2_beatpoint, 55 / tempo))
    input_thread.start()
    START(data=data)


launchpad = Launchpad()
# launchpad.ListAll()
launchpad.Open()


def get_file():
    global FILE_NAME, FILE_PATH
    FILE_PATH = askopenfilename()
    FILE_NAME = os.path.basename(os.path.realpath(FILE_PATH))


def listen():
    while True:
        time.sleep(0.001)
        a = launchpad.EventRaw()
        if a != []:
            if a[0][0][2] == 127:
                print(a)
                # t1 = threading.Thread(target=lightAllRandom,args=(launchpad,0.2))
                interval = 1
                delay = (interval - 0.25) / 64
                t1 = threading.Thread(target=spread_snake, args=(a[0][0][1], launchpad, (interval - 0.15) / 8))
                t1.start()


if __name__ == "__main__":
    MODE = 2
    # 0:监听模式;
    # 1:播放模式;
    # 2:简易模式;
    # 3:重写播放模式;
    # 10:画图模式;
    if launchpad.Check():  # 如果launchpad已经连接
        launchpad.Reset()
    else:
        print("[{:-^60}]".format("Can't Find Launchpad"))
    if MODE == 0:
        listen()
    else:
        tk = Tk()
        tk.withdraw()
        FILE_PATH = askopenfilename()  # 打开文件，要求MP3格式
        tk.destroy()
        if FILE_PATH:
            FILE_NAME = os.path.basename(os.path.realpath(FILE_PATH))
            if MODE == 1:
                START()
            elif MODE == 2:
                START2()
            elif MODE == 3:
                START(rewrite=True)
            elif MODE == 10:
                pyAA.initialize_bpf(FILE_NAME, FILE_PATH, True)
                playAudio.play(FILE_PATH)
        else:
            print("[{:-^60}]".format("Mode Error"))
