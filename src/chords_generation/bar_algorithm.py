from typing import List, Tuple

import music
import utils.constants


def get_sounds_at_metrum(sounds: List[music.Sound], meter: Tuple[int, int]):
    s = []
    next_accent = 0
    accent_duration = meter[0] * meter[1] / 2
    current_timestamp = 0
    for sound in sounds:
        current_timestamp += sound.rhythmic_value_time
        while sound.timestamp >= next_accent:
            s.append(sound)
            next_accent += accent_duration
    return s


def get_tonation_chord(tonation: music.Tonation, sound: music.Sound):
    for chord in [tonation.tonic, tonation.dominant, tonation.subdominant]:
        if sound in chord.sounds():
            return chord
    return tonation.tonic


def get_chords_bar_algorithm(sounds: List[music.Sound],
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

    sounds_at_metrum = get_sounds_at_metrum(sounds, meter)
    chords = [get_tonation_chord(tonation, sound)
              for sound in sounds_at_metrum]

    c1 = []
    # chord_duration = half of meter * how many eigth fits in one meter note
    chord_duration = (meter[0]/2) * (meter[1]/0.5)
    for i, c in enumerate(chords):
        tmp = music.Chord(c.note, duration=chord_duration, kind=c.kind)
        c1.append(tmp)
    chords = c1

    return c1
