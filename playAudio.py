from pyaudio import PyAudio
import time
from pydub import AudioSegment
from io import BytesIO

isPlaying = False


# testGit
def play(filepath):
    fp = open(filepath, 'rb')
    data = fp.read()
    fp.close()
    aud = BytesIO(data)
    sound = AudioSegment.from_file(aud, format='mp3')  # LONG

    global isPlaying
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(sound.sample_width), channels=sound.channels,
                    rate=sound.frame_rate, output=True)
    print("[PLAYAUDIO INTERVAL]%f" % (time.time()))
    datas = sound.raw_data

    isPlaying = True

    stream.write(datas)  # ------------这里，接住！
    '''
    来来来兄弟们，来看看网上大神的代码↓（稍加修改，但是思想融会贯通）
    # framewidth = sound.frame_width
    # i = 0
    # while True:
    #     data = datas[i*framewidth:(i+1)*framewidth]
    #     if data == b"":
    #         break
    #     i += 1
    #     stream.write(data)
    这个人教我一帧一帧的去写，我一想好像没什么毛病。
    当然后果就是CPU必须时刻保持有一定空闲，让出来给这一线程。
    总之就是说CPU必须不能跑高了，稍微高一点就爆音。
    然而我TM发现这东西可以一次全写进去！(如上一句话↑)
    让我们看看官方的注释：
        def write(self, frames, num_frames=None,
              exception_on_underflow=False):

        """
        Write samples to the stream.  Do not call when using
        *non-blocking* mode.

        :param frames:#音频的数据帧
           The frames of data.
        :param num_frames:#帧的数量
           The number of frames to write.
           Defaults to None, in which this value will be
           automatically computed.#你如果不输就是None，系统自动给你判断
    结果网上的代码让我一帧一帧些，他每次都会判断一次帧的数量为1。
    求CPU心理阴影面积。
    不过感谢这位老哥指导我用了pydub这个库。
    改完之后妈妈再也不用担心我音频卡顿了，哪怕我主线程写个while True：pass也不怕了！
    '''

    stream.stop_stream()  # 停止数据流
    stream.close()
    p.terminate()  # 关闭 PyAudio


def isplaying():
    return isPlaying

