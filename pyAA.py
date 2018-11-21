#!/usr/bin/evn python
# -*- coding: utf-8 -*-


import audioconvert
from librosa import load, frames_to_time
import os
from librosa.beat import beat_track
from librosa.onset import onset_strength
from librosa.effects import percussive
from librosa.output import write_wav
import numpy as np
import time

ONSET_DETECT_RATIO = 1000
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
    # data, samplerate = sf.read(filename, dtype='float32')
    timestart = time.time()
    y, sr = load(wav_filename, dtype="float32", res_type=TYPE)
    # --------------------WRITE FILE TO TEST

    # maxv = np.iinfo(np.int16).max
    # write_wav("out_int16.wav", y_perc, sr)
    # --------------------
    print("{LOAD TIME}:%f" % (time.time() - timestart))
    tempo, beats = beat_track(y=y, tightness=100)  # 计算主要节拍点
    tempo1, beats1 = beat_track(y=y, tightness=2)  # 计算节拍点，tightness就是对节拍的吸附性，越低越混乱
    onset_envolope = onset_strength(y=y)
    onset_all_beat = []
    for beat in beats1:
        onset_all_beat.append(onset_envolope[beat])
    average_onset = np.mean(onset_all_beat)
    new_frames_list = []
    for beat in beats1:
        if onset_envolope[beat] > average_onset / ONSET_DETECT_RATIO:
            new_frames_list.append(beat)
    print("{MAX_ONSET}:%f" % onset_envolope.max())
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
