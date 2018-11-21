import librosa
import soundfile as sf

# Get example audio file
filename = "英雄联盟 - 刀锋舞者艾瑞莉娅-登录界面音乐.mp3.wav"

data, samplerate = sf.read(filename, dtype='float32')
data = data.T
data_22k = librosa.resample(data, samplerate, 22050)
a=0