from typing import List, Tuple

import music
import utils.constants

# https://www.fim.uni-passau.de/fileadmin/dokumente/fakultaeten/fim/lehrstuhl/sauer/geyer/BA_MA_Arbeiten/BA-HausnerChristoph-201409.pdf
'''
Split notes into timeline
Split timeline into windows (bars)
    Extend some bars to prevent changing chord in the middle of sound
For each bar get best chord using scoring lists
'''

POINTS = {
    "major": [
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
    ],
    "minor": [
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
    ],
    "diminished": [
        1.05,
        0,
        0,
        1.03,
        0,
        0,
        1.03,
        0,
        0,
        0,
        0,
        0
    ]
}
POINTS["major7"] = POINTS["major"]

COEFS = {
    "major": 1,
    "major7": 1,
    "minor": 0.99,
    "diminished": 0.5
}


def tonation_chords(tonation: music.Tonation):
    n = tonation.note
    if tonation.kind == "major":
        return [
            music.Chord(note=n, kind="major"),
            music.Chord(note=n+2, kind="minor"),
            music.Chord(note=n+4, kind="major"),
            music.Chord(note=n+5, kind="major"),
            music.Chord(note=n+7, kind="major7"),
            music.Chord(note=n+9, kind="minor"),
            music.Chord(note=n+11, kind="diminished")]
    else:
        return [
            music.Chord(note=n, kind="minor"),
            music.Chord(note=n+2, kind="diminished"),
            music.Chord(note=n+4, kind="major"),
            music.Chord(note=n+5, kind="minor"),
            music.Chord(note=n+7, kind="major7"),
            music.Chord(note=n+9, kind="major"),
            music.Chord(note=n+11, kind="diminished")]


def points(chord: music.Chord, sound: music.Sound):
    if sound.note is None:
        return 0
    diff = (sound.note+12 - chord.note) % 12
    return POINTS[chord.kind][diff] * COEFS[chord.kind]


def get_chords_daria(sounds: List[music.Sound],
                     tonation: music.Tonation,
                     meter: Tuple[int, int]):
    meter = (
        meter[0],
        utils.constants.RHYTHMIC_VALUE_TO_TIME[str(meter[1])]
    )
    if meter[0] == 2:
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
        for c in tonation_chords(tonation):
            score = 0
            for j in window:
                score += points(c, t_s[j])
            if score > max_score:
                max_score = score
                max_chord = c
        t_c.append(music.Chord(max_chord.note,
                               duration=half_meter_len/4,
                               kind=max_chord.kind))
        i += half_meter_len
        while i < len(t_s) and t_s[i] == t_s[i-1]:
            i += 1
            t_c[-1].duration += 1/4

    chords = []
    for c in t_c:
        if any(chords) and chords[-1].symbol == c.symbol:
            chords[-1].duration += c.duration
        else:
            chords.append(music.Chord(
                c.note, duration=c.duration, kind=c.kind))

    return chords
