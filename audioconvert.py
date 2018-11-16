from pydub import AudioSegment  ###需要安装pydub、ffmpeg
from wave import open as waveopen
from io import BytesIO


def convert_to_monowav(filename, filepath):
    '''

    :param filename:
    文件名（可以用路径计算出来，我懒）
    :param filepath:
    文件路径
    :return:
    还是文件名

    把MP3转换为单声道wav，存到文件里，专门用来计算beatpoint。
    真正播放的还是MP3，防止单声道过敏。
    '''
    # 打开然后关闭
    fp = open(filepath, 'rb')
    data = fp.read()
    fp.close()
    # 主要部分
    aud = BytesIO(data)  # 通过BytesIO读取音频？
    sound = AudioSegment.from_file(aud, format='mp3')  # 通过pydub的AudioSegment处理出音频信号（可以直接作为wav播放的）
    channels = sound.channels  # 获取音轨数（单声道or立体声一般）
    frame_rate = sound.frame_rate  # 帧率（直译），一般叫采样率？
    raw_data = sound.raw_data  # 作为wav的数据
    sample_width = sound.sample_width  # 采样宽度？
    # 打开文件，写成一个单声道wav文件，便于计算beatpoint
    wav_filename = "dat/%s.wav" % filename
    f = waveopen(wav_filename, 'wb')
    f.setnchannels(1)
    f.setsampwidth(sample_width)
    f.setframerate(frame_rate * channels)
    f.setnframes(1)
    f.writeframes(raw_data)
    f.close()
    return (wav_filename)  # 只返回路径
