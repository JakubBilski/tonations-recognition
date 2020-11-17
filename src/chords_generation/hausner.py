from typing import List, Tuple

import music
import utils.constants


MINOR_COEF = 0.99

MAJOR_POINTS = [
    1.05,
    0,
    0.3,
    0,
    1,
    0,
    0,
    1,
    0,
    0,
    0.3,
    0.1
]
MINOR_POINTS = [
    1.05,
    0,
    0.3,
    1,
    0,
    0,
    0,
    1,
    0,
    0,
    0.3,
    0
]
ALL_CHORDS = [music.Chord(note=i, kind='minor') for i in range(12)] +\
    [music.Chord(note=i, kind='major') for i in range(12)]


def points(chord: music.Chord, sound: music.Sound):
    if sound.note is None:
        return 0
    diff = (sound.note+12 - chord.note) % 12
    if 'major' in chord.kind:
        return MAJOR_POINTS[diff]
    else:
        return MINOR_POINTS[diff]*MINOR_COEF


def get_chords_hausner(sounds: List[music.Sound],
                       tonation: music.Tonation,
                       meter: Tuple[int, int]):
    meter = (
        meter[0],
        utils.constants.RHYTHMIC_VALUE_TO_TIME[str(meter[1])]
    )
    if meter[0] == 2:
        # make 2 times more notes with 2 times less time duration each
        meter = (
            4,
            meter[1]/2
        )
    if meter[0] != 4:
        raise Exception("Not supported meter in chord duration")

    half_meter_len = 2*int(meter[1]/0.125)

    t_s = []
    for s in sounds:
        for _ in range(int(s.rhythmic_value_time*8)):
            t_s.append(s)

    t_c = []
    i = 0
    while i < len(t_s):
        window = list(range(i, min(len(t_s), i+half_meter_len)))
        max_score = -1
        max_chord = None
        for c in ALL_CHORDS:
            score = 0
            for j in window:
                score += points(c, t_s[j])
            if score > max_score:
                max_score = score
                max_chord = c
        t_c.append(music.Chord(max_chord.note, duration=half_meter_len/4, kind=max_chord.kind))
        i += half_meter_len
        while i < len(t_s) and t_s[i] == t_s[i-1]:
            i += 1
            t_c[-1].duration += 1/4
        
    chords = []
    for c in t_c:
        if any(chords) and chords[-1].symbol == c.symbol:
            chords[-1].duration += c.duration
        else:
            chords.append(music.Chord(c.note, duration=c.duration, kind=c.kind))

    return chords
