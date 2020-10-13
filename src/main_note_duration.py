import argparse
from math import floor
import pathlib
import librosa

import sounds_generation

from mingus.containers import Track
from mingus.midi import midi_file_out
from mingus.core import value

from midi2audio import FluidSynth


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

    t = Track()
    for s in sounds:
        # v0 = round(s.duration*8/first)
        # if v0 >= 32:
        #     v = 1
        # elif v0 >= 16:
        #     v = 2
        # elif v0 >=8:
        #     v = 4
        # elif v0 >= 4:
        #     v = 8
        # elif v0 >=2:
        #     v = 16
        # else:
        #     v = 32
        # # v1  = floor(32/v)
        # # if v0 - v1 >= v1/2:
        # #     v = value.dots(v)

        # v = 32
        # for i in range(round(s.duration*8/first)-1):
        #     v = value.add(v, 32)

        for i in range(round(s.duration*8/first)):
            if s.note is None:
                print(t.add_notes(None, 32))
            else:
                print(t.add_notes(s.symbol, 32))

            
        
    # print(t)
    midi_file_out.write_Track("test.mid", t)
    fs = FluidSynth()
    fs.midi_to_audio('test.mid', 'test.wav')


1 - 32
2 - 16
4 - 8
8 - 4
16 - 2
32 - 1