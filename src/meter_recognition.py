import librosa


def get_meter(filename, sounds):
    # TODO use sounds?
    y, sr = librosa.load(filename)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return 60.0/tempo


def update_sounds(meter, sounds):
    # TODO update length of sounds to fit meter
    # round(sound.duration*8/meter)/8  <- it is an idea
    return sounds
