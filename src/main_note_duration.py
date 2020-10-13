import argparse
from math import floor
import pathlib
import librosa
from mingus.containers.bar import Bar

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

    def add_sound(t, sound, duration):
        v = 32
        for i in range(duration-1):
            v = value.add(v, 32)
        if sound.note is None:
            print(t.add_notes(None, v))
        else:
            print(t.add_notes(s.symbol, v))

    v_sum = sum([round(sound.duration*8/first) for sound in sounds])

    t = Track()
    t.add_bar(Bar(meter=(round(v_sum/32)+1, 1)))
    v_bar = 32
    for s in sounds:
        v_act = round(s.duration*8/first)
        
        # while v_act > v_bar:
        #     print(f"{v_bar}:{v_act}")
        #     add_sound(t, s, v_bar)
        #     v_act -= v_bar
        #     v_bar = 32

        # if v_act == 0:
        #     continue

        # print(f"{v_bar}:{v_act}")
        add_sound(t, s, v_act)
        # v_bar -= v_act

        # if v_bar == 0:
        #     v_bar = 32


            
        
    # print(t)
    midi_file_out.write_Track("test.mid", t)
    fs = FluidSynth()
    fs.midi_to_audio('test.mid', 'test.wav')

