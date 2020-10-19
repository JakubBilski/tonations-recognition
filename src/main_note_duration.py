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

    y, sr = librosa.load(args.input)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    metrum = 60.0/tempo
    print(f"Metrum: {metrum}")

    print("Sounds:")
    print("\n".join([f"{sound.duration:.3f}: {sound.symbol}\t{round(sound.duration*8/metrum)/8}" for sound in sounds]))  # noqa

    music_synthesis.wav_from_sounds(sounds, 'sounds')
    ton = tonations_generation.get_tonations_from_sounds(sounds)[0].tonation
    cho = chords_generation.get_chords(sounds, ton, metrum,
                                       sounds[0].timestamp)

    print("Chords:")
    print("\n".join([f"{chord.duration:.3f}: {chord}\t{round(chord.duration*8/metrum)/8}" for chord in cho]))  # noqa

    music_synthesis.wav_from_chords(cho, 'chords')

    from pydub import AudioSegment
    sound1 = AudioSegment.from_file("sounds.wav")
    sound2 = AudioSegment.from_file("chords.wav")

    sound2 = sound2 - 13

    combined = sound1.overlay(sound2)

    combined.export("result.wav", format='wav')
