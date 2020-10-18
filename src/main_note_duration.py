import argparse
from math import comb, floor
import pathlib
import librosa
from mingus.containers.bar import Bar

import sounds_generation

from mingus.containers import Track
from mingus.midi import midi_file_out
from mingus.core import value

from midi2audio import FluidSynth

import music_synthesis
import tonations_generation
import chords_generation


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert audio file to notes with time of occurrence')
    parser.add_argument('--input', '-I',
                        required=True,
                        help='Input audio file. Formats: [.mp3, .wav]',
                        type=pathlib.Path)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    sounds = sounds_generation.get_sounds_from_file(args.input)
    # sounds = [s for s in sounds if s.timestamp < 10]

    # sounds = [sound for sound in sounds if sound.duration >= 0.1 and sound.note is not None]

    # print("\n".join([str(sound) for sound in sounds]))
    # print("\n".join([f"{sound.duration:.3f}: {sound.symbol}" for sound in sounds]))

    # d = {}
    # for s in sounds:
    #     d[round(100*s.duration)] = d.get(round(100*s.duration), 0)+1

    # ids = sorted(list(d))
    # for id in ids:
    #     print(f"{id}: {d[id]}")

    y, sr = librosa.load(args.input)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    first = 60.0/tempo
    print(first)

    # longest = max(sounds, key=lambda s: s.duration if s.note is not None else 0).duration
    # print(round(longest*8/first)/8)

    print("\n".join([f"{sound.duration:.3f}: {sound.symbol}\t{round(sound.duration*8/first)/8}" for sound in sounds]))

    music_synthesis.wav_from_sounds1(sounds, first, 'sounds')
    ton = tonations_generation.get_tonations_from_sounds(sounds)[0].tonation
    cho = chords_generation.get_chords(sounds, ton, first, sounds[0].timestamp)
    music_synthesis.wav_from_chords1(cho, first, 'chords')

    from pydub import AudioSegment
    sound1 = AudioSegment.from_file("sounds.wav")
    sound2 = AudioSegment.from_file("chords.wav")

    sound2 = sound2 - 5

    combined = sound1.overlay(sound2)

    combined.export("result.wav", format='wav')
