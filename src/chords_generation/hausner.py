from typing import List, Tuple

from ..music import Chord, Sound, Key

# https://www.fim.uni-passau.de/fileadmin/dokumente/fakultaeten/fim/lehrstuhl/sauer/geyer/BA_MA_Arbeiten/BA-HausnerChristoph-201409.pdf
'''
Split notes into timeline
Split timeline into windows (bars)
    Extend some bars to prevent changing chord in the middle of sound
For each bar get best chord using scoring lists
'''

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
ALL_CHORDS = [Chord(note=i, kind='minor') for i in range(12)] +\
    [Chord(note=i, kind='major') for i in range(12)]


def points(chord: Chord, sound: Sound):
    if sound.note is None:
        return 0
    diff = (sound.note+12 - chord.note) % 12
    if 'major' in chord.kind:
        return MAJOR_POINTS[diff]
    else:
        return MINOR_POINTS[diff]*MINOR_COEF


def get_chords_hausner(sounds: List[Sound],
                       key: Key,
                       meter: Tuple[int, int]):
    if meter[0] == 2:
        meter = (
            4,
            meter[1]//2
        )

    half_meter_len = meter[0]*meter[1]//2

    t_s = []
    for s in sounds:
        for _ in range(s.duration):
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
        t_c.append(Chord(max_chord.note,
                         duration=half_meter_len,
                         kind=max_chord.kind))
        i += half_meter_len
        while i < len(t_s) and t_s[i] == t_s[i-1]:
            i += 1
            t_c[-1].duration += 1

    chords = []
    for c in t_c:
        if any(chords) and chords[-1].symbol == c.symbol:
            chords[-1].duration += c.duration
        else:
            chords.append(Chord(
                c.note, duration=c.duration, kind=c.kind))

    return chords
