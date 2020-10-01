import argparse
import pathlib

from typing import List

from tonation import Tonation
from chord import Sound, Sounds


def get_sounds_at_metrum(sounds: List[Sound], metrum: int, start: int):
    s = []
    last_metrum = start
    for sound in sounds:
        while sound.timestamp >= last_metrum:
            s.append(sound)
            last_metrum += metrum
    return s


def get_tonation_chord(tonation: Tonation, sound: Sound):
    for chord in [tonation.tonic, tonation.dominant, tonation.subdominant]:
        if sound in chord.sounds():
            return chord
    return tonation.tonic


def get_chords(sounds: List[Sound], tonation: Tonation, metrum: int, start: int):
    print(tonation)
    sounds_at_metrum = get_sounds_at_metrum(sounds, metrum, start)
    print(f"Sounds at metrum: {sounds_at_metrum}")
    chords = [get_tonation_chord(tonation, sound)
              for sound in sounds_at_metrum]
    return chords


# def parse_args():
#     parser = argparse.ArgumentParser(
#         description='Convert auio file to notes with time of occurrence')
#     parser.add_argument('--input', '-I',
#                         required=True,
#                         help='Audio file. Formats: [.mp3, .wav]',
#                         type=pathlib.Path)
#     args = parser.parse_args()
#     return args


if __name__ == "__main__":
    s = Sounds()
    print(f"song: {s.sounds}")
    chords = get_chords(s.sounds, Tonation(0, 0, 0, "dur"), 3, 1)
    print(f"chords: {chords}")
