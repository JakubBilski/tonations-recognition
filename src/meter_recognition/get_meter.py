import librosa


def get_meter(file_path, sounds):
    y, sr = librosa.load(file_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
    return 60.0/tempo, beats
