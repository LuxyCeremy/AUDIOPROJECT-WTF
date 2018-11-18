#!/usr/bin/evn python
# -*- coding: utf-8 -*-


import audioconvert
from librosa import load, frames_to_time
import os
from librosa.beat import beat_track
from librosa.onset import onset_strength
import numpy as np

ONSET_DETECT_RATIO = 2

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
        content = file.read()
        file.close()
        if (os.path.exists("dat/%s.wav" % filename)):
            os.remove("dat/%s.wav" % filename)
        return content
    except Exception as e:
        print("No bpf found, initializing..."+str(e))
        pass
    wav_filename = audioconvert.convert_to_monowav(filename, filepath)
    y, sr = load(wav_filename)

    tempo, beats = beat_track(y=y, sr=sr, tightness=100)  # 计算主要节拍点
    tempo1, beats1 = beat_track(y=y, sr=sr, tightness=2)  # 计算节拍点，tightness就是对节拍的吸附性，越低越混乱
    onset_envolope = onset_strength(y=y, sr=sr)
    new_frames_list = []
    for beat in beats1:
        if onset_envolope[beat]> ONSET_DETECT_RATIO:
            new_frames_list.append(beat)
    new_beats_frame = np.array(new_frames_list)
    bigbeatlocation = frames_to_time(beats, sr=sr)
    beatlocation = frames_to_time(new_beats_frame, sr=sr).tolist()
    beatmain = []
    for beat in beatlocation:  # 分别计算出每个节拍到主要节拍点的距离，也就是这个节拍的主要程度

        p = abs(bigbeatlocation - beat)
        print("%f:   %f" % (beat, p.min()))
        beatmain.append(p.min())
    file = open("dat/%s.bpf" % filename, mode="w")
    file.write(repr([tempo, beatlocation, beatmain]))
    file.close()
    if (os.path.exists("dat/%s.wav" % filename)):
        os.remove("dat/%s.wav" % filename)
    return repr([tempo, beatlocation, beatmain])
def getmainbeatpoint(filename, filepath):
    try:
        file = open("dat/%s.mbpf" % filename, mode="r")
        content = file.read()
        file.close()
        if (os.path.exists("dat/%s.wav" % filename)):
            os.remove("dat/%s.wav" % filename)
        return content
    except Exception as e:
        print("No mbpf found, initializing...")
        print(e)
        pass
    wav_filename = audioconvert.convert_to_monowav(filename, filepath)
    y, sr = load(wav_filename)

    tempo, beats = beat_track(y=y, sr=sr, tightness=100)  # 计算主要节拍点
    bigbeatlocation = frames_to_time(beats, sr=sr).tolist()
    file = open("dat/%s.mbpf" % filename, mode="w")
    file.write(repr(bigbeatlocation))
    file.close()
    if(os.path.exists("dat/%s.wav" % filename)):
        os.remove("dat/%s.wav" % filename)
    return repr(bigbeatlocation)