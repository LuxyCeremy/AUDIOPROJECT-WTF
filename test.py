import librosa

y, sr = librosa.load("Beautiful lies.mp3.wav")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, tightness=100)  # 计算主要节拍点
beatsA =beats.tolist()