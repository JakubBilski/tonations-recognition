import argparse
from math import floor
import pathlib
import librosa
from mingus.containers.bar import Bar

import sounds_generation

from mingus.containers import Track
from mingus.containers import NoteContainer
from mingus.midi import midi_file_out
from mingus.core import value

from midi2audio import FluidSynth


def add_sound(t, sound, duration):
    v = 32
    for _ in range(duration-1):
        v = value.add(v, 32)
    if sound.note is None:
        print(t.add_notes(None, v))
    else:
        print(t.add_notes(sound.symbol, v))


def add_chord(t, chord, duration):
    v = 32
    for _ in range(duration-1):
        v = value.add(v, 32)
    if chord.note is None:
        print(t.add_notes(None, v))
    else:
        sounds = [s.symbol for s in chord.sounds]
        print(t.add_notes(NoteContainer(sounds), v))


def wav_from_sounds(sounds, beat_duration):
    v_sum = sum([round(sound.duration*8/beat_duration) for sound in sounds])

    t = Track()
    t.add_bar(Bar(meter=(round(v_sum/32)+1, 1)))

    for s in sounds:
        v_act = round(s.duration*8/beat_duration)

        add_sound(t, s, v_act)

    midi_file_out.write_Track("test.mid", t)
    fs = FluidSynth()
    fs.midi_to_audio('test.mid', 'test.wav')
    return pathlib.Path('test.wav')


def wav_from_chords(sounds, beat_duration):
    v_sum = sum([round(sound.duration*8/beat_duration) for sound in sounds])

    t = Track()
    t.add_bar(Bar(meter=(round(v_sum/32)+1, 1)))

    for s in sounds:
        v_act = round(s.duration*8/beat_duration)

        add_chord(t, s, v_act)

    midi_file_out.write_Track("test.mid", t)
    fs = FluidSynth()
    fs.midi_to_audio('test.mid', 'test.wav')
    return pathlib.Path('test.wav')
