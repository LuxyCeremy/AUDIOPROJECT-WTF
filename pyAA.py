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
import threading

ONSET_DETECT_RATIO = 1.2
RMS_RATIO = 1.5
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


def plt_show(TITLE, T, onset_all_beat, frame_all_beat, MAX_RMS, AVERAGE_RMS, AVERAGE_ONSET):
    Times = frames_to_time(np.array([i for i in range(T.size)]))
    plt.subplot(2, 1, 1)
    plt.title(TITLE)
    plt.plot(Times, T)
    plt.hlines(MAX_RMS / RMS_RATIO, 0, Times.max(), colors='r',
               label='MAX_RMS / RMS_RATIO')
    plt.hlines(AVERAGE_RMS, 0, Times.max(), colors='g',
               label='AVERAGE_RMS')
    plt.legend()
    plt.ylabel('RMS_ENVELOPE')
    Times1 = frames_to_time(np.array(frame_all_beat))
    plt.subplot(2, 1, 2)
    plt.plot(Times1, np.array(onset_all_beat))
    plt.hlines(AVERAGE_ONSET / ONSET_DETECT_RATIO, 0, Times.max(), colors='r',
               label='AVERAGE_ONSET / ONSET_DETECT_RATIO')
    plt.legend()
    plt.ylabel('ONSET_ENVELOPE')
    plt.xlabel('Time (s)')
    plt.show()


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

    MAX_RMS = np.max(rms_envelope)
    AVERAGE_RMS = np.mean(rms_envelope)
    onset_all_beat = []
    frame_all_beat = []
    for beat in beats1:
        onset_all_beat.append(onset_envelope[beat])
        frame_all_beat.append(beat)
    AVERAGE_ONSET = np.mean(onset_all_beat)
    new_frames_list = []
    t1 = threading.Thread(target=plt_show,
                          args=(filename,rms_envelope.T, onset_all_beat, frame_all_beat, MAX_RMS, AVERAGE_RMS, AVERAGE_ONSET))
    t1.start()
    for beat in beats1:
        if onset_envelope[beat] > AVERAGE_ONSET / ONSET_DETECT_RATIO \
                or rms_envelope.T[beat] > MAX_RMS / RMS_RATIO:
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
