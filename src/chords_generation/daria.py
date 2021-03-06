from typing import List, Tuple

from ..music import Chord, Sound, Key
from . import daria_params as params

# https://www.fim.uni-passau.de/fileadmin/dokumente/fakultaeten/fim/lehrstuhl/sauer/geyer/BA_MA_Arbeiten/BA-HausnerChristoph-201409.pdf
'''
Split notes into timeline
Split timeline into windows (bars)
    Extend some bars to prevent changing chord in the middle of sound
For each bar get best chord using scoring lists
'''


def key_chords(key: Key):
    n = key.note
    if key.kind == "major":
        chords = [
            Chord(note=n, kind="major"),
            Chord(note=n+2, kind="minor"),
            Chord(note=n+4, kind="minor"),
            Chord(note=n+5, kind="major"),
            Chord(note=n+7, kind="major7"),
            Chord(note=n+9, kind="minor"),
            Chord(note=n+11, kind="diminished")]
    else:
        chords = [
            Chord(note=n, kind="minor"),
            Chord(note=n+2, kind="diminished"),
            Chord(note=n+3, kind="major"),
            Chord(note=n+5, kind="minor"),
            Chord(note=n+7, kind="major7"),
            Chord(note=n+8, kind="major"),
            Chord(note=n+11, kind="diminished")]
    for i in range(len(chords)):
        chords[i].level = i+1
    return chords


def points_for_sound(chord: Chord, sound: Sound):
    if sound.note is None:
        return 0
    diff = (sound.note+12 - chord.note) % 12
    return params.POINTS[chord.kind][diff]


def point_coef(chord: Chord, first_sound: Sound,
               last_chord_level: int):
    if chord.note == first_sound.note:
        first_sound_coef = params.FIRST_SOUND
    else:
        first_sound_coef = 1
    return params.COEFS[chord.kind] * \
        params.NEXT_CHORD[last_chord_level][chord.level] * \
        first_sound_coef


def get_chords_daria(sounds: List[Sound],
                     key: Key,
                     meter: Tuple[int, int]):
    if meter[0] == 2:
        meter = (
            4,
            meter[1]//2
        )

    # allow changing chords every half bar
    half_bar_len = meter[0]*meter[1]//2

    # create timeline of sounds
    t_s = []
    endings = [0]
    for s in sounds:
        for _ in range(s.duration):
            t_s.append(s)
        endings.append(endings[-1]+s.duration)

    # generate chords
    t_c = []
    i = 0
    # chord level - on which key note the chord is built
    last_chord_level = 0  # 0 means "start of the song"
    while i < len(t_s):

        # split timeline into windows with len of one bar
        window = list(range(i, min(len(t_s), i+half_bar_len)))

        # for each chord in available chords get points
        max_score = -1
        max_chord = None
        for c in key_chords(key):
            score = 0
            # add score for each sound (based on sound length)
            for j in window:
                score += points_for_sound(c, t_s[j])
            # multiply by coefficient
            score *= point_coef(c, t_s[window[0]], last_chord_level)
            if score > max_score:
                max_score = score
                max_chord = c

        t_c.append(Chord(max_chord.note,
                         duration=half_bar_len,
                         kind=max_chord.kind))
        last_chord_level = max_chord.level
        i += half_bar_len
        # prevent adding new chord between notes
        while i < len(t_s) and (i not in endings):
            i += 1
            t_c[-1].duration += 1

    # merge chords with the same note
    chords = []
    for c in t_c:
        if any(chords) and chords[-1].symbol == c.symbol:
            chords[-1].duration += c.duration
        else:
            chords.append(Chord(
                c.note, duration=c.duration, kind=c.kind))

    return chords
