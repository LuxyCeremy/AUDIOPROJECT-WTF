#!/usr/bin/evn python
# -*- coding: utf-8 -*-


import os
import time
import threading
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process
from matplotlib.font_manager import FontProperties

from librosa import load, frames_to_time
from librosa.beat import beat_track
from librosa.onset import onset_strength
from librosa.feature import rmse

import audioconvert

ONSET_DETECT_RATIO = 1.2
RMS_RATIO = 1.5
TYPE = "kaiser_fast"

font = FontProperties(fname='msyh.ttf')


# TYPE = 'kaiser_best'


# TYPE = 'scipy'


def getbeatpoint(filename, filepath, rewrite=False):
    '''

    :param filename:
    文件名（可以用路径计算出来，我懒）
    :param filepath:
    文件路径
    :return:
    一个包含所有信息的三元数组：BPM，节拍点，强节拍系数

    '''
    if os.path.exists("dat/%s.bpf" % filename) \
            and os.path.exists("dat/plt/%s.plt" % filename) \
            and not rewrite:
        file = open("dat/%s.bpf" % filename, mode="r")
        plt_file = open("dat/plt/%s.plt" % filename, mode="r")
        plt_file_content = eval(plt_file.read())
        plt_process = Process(target=plt_show, args=plt_file_content)
        plt_process.start()
        if (os.path.exists("dat/%s.wav" % filename)):
            os.remove("dat/%s.wav" % filename)
    else:
        print("Initializing...")
        path = initialize_bpf(filename, filepath, rewrite=True)
        file = open(path, mode="r")

    content = file.read()
    file.close()
    return content


def plt_show(TITLE, rms_list, onset_all_beat, frame_all_beat, MAX_RMS, AVERAGE_RMS, AVERAGE_ONSET):
    T = np.array(rms_list)
    Times = frames_to_time(np.array([i for i in range(T.size)]))
    MAXs = []

    MAXs.append(T.max())
    MAXs.append(max(onset_all_beat))
    plt.figure(figsize=[12, 6])
    plot1 = plt.subplot(2, 1, 1)
    plt.title(TITLE, fontproperties=font)
    plt.plot(Times, T)
    plt.hlines(MAX_RMS / RMS_RATIO, 0, Times.max(), colors='r',
               label='MAX_RMS / RMS_RATIO')
    plt.hlines(AVERAGE_RMS, 0, Times.max(), colors='g',
               label='AVERAGE_RMS')
    plt.legend()
    plt.ylabel('RMS_ENVELOPE')
    Times1 = frames_to_time(np.array(frame_all_beat))
    plot2 = plt.subplot(2, 1, 2)
    plt.plot(Times1, np.array(onset_all_beat))
    plt.hlines(AVERAGE_ONSET / ONSET_DETECT_RATIO, 0, Times.max(), colors='r',
               label='AVERAGE_ONSET / ONSET_DETECT_RATIO')
    plt.hlines(AVERAGE_ONSET, 0, Times.max(), colors='G',
               label='AVERAGE_ONSET')
    draw_thread = threading.Thread(target=time_line_draw, args=(MAXs, Times.max(), plot1, plot2))
    draw_thread.start()
    plt.legend()
    plt.ylabel('ONSET_ENVELOPE')
    plt.xlabel('Time (s)')
    plt.show()


def time_line_draw(MAXs, Time, *plots):
    timestart = time.time()
    while True:
        time_lines = []
        for i, plot in enumerate(plots):
            time_lines.append(plot.vlines(time.time() - timestart, 0, MAXs[i], colors='orange'))
        time.sleep(0.2)
        plt.draw()
        for time_line in time_lines:
            time_line.remove()
        if time.time() - timestart > Time:
            return


def plt_show_solo(filename, filepath):
    wav_filename = audioconvert.convert_to_monowav(filename, filepath)
    timestart = time.time()
    y, sr = load(wav_filename, dtype="float32", res_type=TYPE)
    print("{LOAD TIME}:%f" % (time.time() - timestart))

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
    plt_show(filename, rms_envelope.T, onset_all_beat, frame_all_beat, MAX_RMS, AVERAGE_RMS,
             AVERAGE_ONSET)


def normalize_tempo(tempo):
    while tempo > 200 or tempo < 100:
        if tempo < 100:
            tempo = tempo * 2
        if tempo > 200:
            tempo = tempo / 2
    return tempo


def initialize_bpf(filename, filepath, only_show=False, rewrite=False):
    wav_filename = audioconvert.convert_to_monowav(filename, filepath)
    timestart = time.time()
    y, sr = load(wav_filename, dtype="float32", res_type=TYPE)

    print("{LOAD TIME}:%f" % (time.time() - timestart))
    tempo, beats = beat_track(y=y, tightness=100)  # 计算主要节拍点
    tempo1, beats1 = beat_track(y=y, tightness=1)  # 计算节拍点，tightness就是对节拍的吸附性，越低越混乱
    onset_envelope = onset_strength(y=y)
    rms_envelope = rmse(y=y)
    # -----------RMS ENVELOPE
    tempo = normalize_tempo(tempo)
    MAX_RMS = np.max(rms_envelope)
    AVERAGE_RMS = np.mean(rms_envelope)
    onset_all_beat = []
    frame_all_beat = []
    for beat in beats1:
        onset_all_beat.append(onset_envelope[beat])
        frame_all_beat.append(beat)
    AVERAGE_ONSET = np.mean(onset_all_beat)
    new_frames_list = []
    if not os.path.exists("dat/plt/%s.plt" % filename) or rewrite:
        print("No plt found, initializing...")
        plt_file = open("dat/plt/%s.plt" % filename, mode="w")
        plt_file.write(repr((filename, rms_envelope.T.tolist(), onset_all_beat, frame_all_beat, MAX_RMS, AVERAGE_RMS,
                             AVERAGE_ONSET)))
        plt_file.close()
    plt_file = open("dat/plt/%s.plt" % filename, mode="r")
    plt_file_content = eval(plt_file.read())
    plt_process = Process(target=plt_show, args=plt_file_content)
    plt_process.start()
    if not only_show:
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
