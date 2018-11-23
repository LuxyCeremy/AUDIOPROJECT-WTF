#!/usr/bin/evn python
# -*- coding: utf-8 -*-


import audioconvert
from librosa import load, frames_to_time
import os
from librosa.beat import beat_track
from librosa.onset import onset_strength
from librosa.feature import rmse
import numpy as np
import matplotlib.pyplot as plt
import time

ONSET_DETECT_RATIO = 1.2
TYPE = "kaiser_fast"


# TYPE = 'kaiser_best'


# TYPE = 'scipy'


def getbeatpoint(filename, filepath):
    '''

    :param filename:
    文件名（可以用路径计算出来，我懒）
    :param filepath:
    文件路径
    :return:
    一个包含所有信息的三元数组：BPM，节拍点，强节拍系数

    '''
    try:
        file = open("dat/%s.bpf" % filename, mode="r")
        if (os.path.exists("dat/%s.wav" % filename)):
            os.remove("dat/%s.wav" % filename)

    except Exception as e:
        print("No bpf found, initializing..." + str(e))
        path = writebpf(filename, filepath)
        file = open(path, mode="r")
    content = file.read()
    file.close()
    return content


def writebpf(filename, filepath):
    wav_filename = audioconvert.convert_to_monowav(filename, filepath)
    timestart = time.time()
    y, sr = load(wav_filename, dtype="float32", res_type=TYPE)

    print("{LOAD TIME}:%f" % (time.time() - timestart))
    tempo, beats = beat_track(y=y, tightness=100)  # 计算主要节拍点
    tempo1, beats1 = beat_track(y=y, tightness=1)  # 计算节拍点，tightness就是对节拍的吸附性，越低越混乱
    onset_envelope = onset_strength(y=y)
    rms_envelope = rmse(y=y)
    # -----------RMS ENVELOPE
    # plt.plot(rms_envelope.T)
    # plt.tight_layout()
    # plt.show()

    MAX_RMS = np.max(rms_envelope)
    onset_all_beat = []
    for beat in beats1:
        onset_all_beat.append(onset_envelope[beat])
    AVERAGE_ONSET = np.mean(onset_all_beat)
    new_frames_list = []
    for beat in beats1:
        if onset_envelope[beat] > AVERAGE_ONSET / ONSET_DETECT_RATIO \
                or rms_envelope.T[beat] > MAX_RMS / 1.5:
            new_frames_list.append(beat)
    print("{MAX_ONSET}:%f" % onset_envelope.max())
    new_beats_frame = np.array(new_frames_list)
    mainbeatlocation = frames_to_time(beats)
    beatlocation = frames_to_time(new_beats_frame).tolist()
    beatmain = []
    for beat in beatlocation:  # 分别计算出每个节拍到主要节拍点的距离，也就是这个节拍的主要程度

        p = abs(mainbeatlocation - beat)
        # print("%f:   %f" % (beat, p.min()))
        beatmain.append(p.min())
    file = open("dat/%s.bpf" % filename, mode="w")
    file.write(repr([tempo, beatlocation, beatmain, mainbeatlocation.tolist()]))
    file.close()
    if (os.path.exists("dat/%s.wav" % filename)):
        os.remove("dat/%s.wav" % filename)
    return "dat/%s.bpf" % filename
