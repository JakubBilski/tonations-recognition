from typing import List

import music


def get_sounds_at_metrum(sounds: List[music.Sound], metrum: int, start: int):
    s = []
    last_metrum = start
    for sound in sounds:
        while sound.timestamp >= last_metrum:
            s.append(sound)
            last_metrum += metrum
    return s


def get_tonation_chord(tonation: music.Tonation, sound: music.Sound):
    for chord in [tonation.tonic, tonation.dominant, tonation.subdominant]:
        if sound in chord.sounds():
            return chord
    return tonation.tonic


def get_chords(sounds: List[music.Sound], tonation: music.Tonation, metrum: int, start: int):
    print(tonation)
    sounds_at_metrum = get_sounds_at_metrum(sounds, metrum, start)
    print(f"Sounds at metrum: {sounds_at_metrum}")
    chords = [get_tonation_chord(tonation, sound)
              for sound in sounds_at_metrum]
    return chords
