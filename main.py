from launchpad_py import Launchpad
import time
import random
import threading
import pyAA
import playAudio
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

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
BUTTONID = -1


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
    return [X, Y]


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


def spread(key, launchpad, delay, STYLE):
    global inSpread
    x = 0
    y = 0
    if key is None:
        x = random.randint(0, 7)
        y = random.randint(1, 8)
    else:
        XY = KEY_TO_XY(key)
        x = XY[0]
        y = XY[1]
        print("[[[[[[[[[[[[[[%d%d]]]]]]]]]]]]]"%(x,y))
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
            launchpad.LedCtrlXY(0, (8 - t + 1 - 2 * reverse) % 8, 0, 0)
            launchpad.LedCtrlXY(7, (t - 1 + 1 + 2 * reverse) % 8, 0, 0)
            time.sleep(delay)
    launchpad.LedCtrlXY(7, 1, 0, 0)
    launchpad.LedCtrlXY(7, 8, 0, 0)
    launchpad.LedCtrlXY(0, 1, 0, 0)
    launchpad.LedCtrlXY(0, 8, 0, 0)
    print("deltatime:%f\tspin_thin" % (time.time() - timestart))


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


def slash_spread(launchpad, delay, reverse):
    timestart = time.time()
    [(R, G)] = RANDOM_RGY(1)
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


def slash_spread2(launchpad, delay, reverse):
    timestart = time.time()
    [(R, G)] = RANDOM_RGY(1)

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


def listen():
    while True:
        time.sleep(0.001)
        a = launchpad.EventRaw()
        if a != []:
            if a[0][0][2] == 127:
                print(a)
                # t1 = threading.Thread(target=lightAllRandom,args=(launchpad,0.2))
                t1 = threading.Thread(target=spread, args=(a[0][0][1], launchpad, 0.2, 1))
                t1.start()


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
    for i in range(len(beatpoint)):
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
        if inCircle == -1:
            if beatmain[i] < 0.005:  # 如果强节拍系数小于5毫秒就判断是一个强拍（然而真正的强拍差都是0.0f，我这就算网开拌面了）
                if interval > beatsecond:  # 如果是一个长拍
                    style = random.randint(1, 5)
                    if style == 1:
                        if samebeat(beatpoint[i:i + 4]):
                            inCircle = 31
                    if style == 2:
                        flash_thread = threading.Thread(target=slash_spread2,
                                                        args=(launchpad, (interval - 0.13) / 24, random.randint(0, 1)))
                    if style == 4:  # LONG
                        flash_thread = threading.Thread(target=slash_spread,
                                                        args=(launchpad, (interval - 0.13) / 15, random.randint(0, 1)))

                    if style == 3:
                        flash_thread = threading.Thread(target=spread,
                                                        args=(BUTTONID if BUTTONID != -1 else None, launchpad,
                                                              (interval - 0.13) / 16, 1))
                    if flash_thread is None and inCircle == -1:
                        flash_thread = threading.Thread(target=spread,
                                                        args=(BUTTONID if BUTTONID != -1 else None, launchpad,
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
                    style = random.choice([3, 4, 5])
                    if style == 4:
                        if samebeat(beatpoint[i:i + 6]):
                            inCircle = 1
                    if style == 5:
                        if samebeat(beatpoint[i:i + 3]):
                            inCircle = 51
                        REVERSE = random.randint(0, 1)
                    if style == 3:  # LONG
                        flash_thread = threading.Thread(target=spin,
                                                        args=(
                                                            launchpad, (interval - 0.15) / 16 if interval > 0.15 else 0,
                                                            2))
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


def blink_point(launchpad):
    global CURRENT_POINT
    (X, Y) = POINT_16[CURRENT_POINT]
    (X1, Y1) = POINT_16[CURRENT_POINT - 1 if CURRENT_POINT > 0 else 15]
    launchpad.LedCtrlXY(X, Y, 3, 3)
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
    pass


def input2(mainbeatpoint):
    global TOTALCOUNT, FAILURECOUNT, LIGHT_DECREASE, BUTTONID
    while not playAudio.isplaying():
        pass
        time.sleep(0.01)
    print("[AUDIO IS PLAYING]%f" % time.time())
    timestart = time.time()
    for i in range(len(mainbeatpoint)):
        while time.time() - timestart < mainbeatpoint[i] - 0.1:
            # 如果从开始播放到现在的时间还没到绝对节拍时间，那就sleep
            # 这一条保证了任何一个节拍的误差都在10ms之内
            # 也保证了不会出现单线程的脱节情况
            time.sleep(0.01)
        while time.time() - timestart < mainbeatpoint[i] + 0.1:
            a = launchpad.EventRaw()

            time.sleep(0.01)
            if a != []:
                launchpad.ButtonFlush()
                print(a)
                if a[0][0][2] == 127:
                    TOTALCOUNT += 1
                    FAILURECOUNT = 0
                    BUTTONID = a[0][0][1]
                    print("[{:_^30}]".format(TOTALCOUNT))
                    break
        else:
            FAILURECOUNT += 1
            print("[{:^^30}]".format(FAILURECOUNT))
        if FAILURECOUNT < 2:
            LIGHT_DECREASE = 0
        elif FAILURECOUNT < 4:
            LIGHT_DECREASE = 1
        elif FAILURECOUNT < 8:
            LIGHT_DECREASE = 2
        else:
            LIGHT_DECREASE = 3


def START():
    mode1_data = eval(pyAA.getbeatpoint(FILE_NAME, FILE_PATH))
    tempo = mode1_data[0]
    beatpoint = mode1_data[1]
    beatmain = mode1_data[2]
    print("[TEMPO]:%f" % tempo)
    print("[TOTAL BEATPOINT]:%d" % len(beatpoint))
    print("[STARTFLASH]%f" % time.time())
    flash_thread = threading.Thread(target=flash, args=(beatpoint, beatmain, 55 / tempo))
    flash_thread.start()
    playAudio.play(FILE_PATH)


def START2():
    mode2_data = eval(pyAA.getmainbeatpoint(FILE_NAME, FILE_PATH))
    flash2_thread = threading.Thread(target=flash2, args=(mode2_data,))
    flash2_thread.start()
    input_thread = threading.Thread(target=input2, args=(mode2_data,))
    input_thread.start()
    START()


launchpad = Launchpad()
# launchpad.ListAll()
launchpad.Open()


def get_file():
    global FILE_NAME, FILE_PATH
    FILE_PATH = askopenfilename()
    FILE_NAME = os.path.basename(os.path.realpath(FILE_PATH))


if __name__ == "__main__":

    if launchpad.Check():  # 如果launchpad已经连接
        launchpad.Reset()
        mode = 1
        # 0：监听模式1:播放模式；2：简易模式
        if mode == 0:
            listen()
        else:
            tk = Tk()
            tk.withdraw()
            FILE_PATH = askopenfilename()  # 打开文件，要求MP3格式
            tk.quit()
            if FILE_PATH:
                FILE_NAME = os.path.basename(os.path.realpath(FILE_PATH))
                if mode == 1:
                    START()
                elif mode == 2:
                    START2()
            else:
                pass


    else:
        print("[{:-^60}]".format("Can't Find Launchpad"))
