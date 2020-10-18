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

from midiutil.MidiFile import MIDIFile


def add_sound(t, sound, duration):
    v = 32
    for _ in range(duration-1):
        v = value.add(v, 32)
    if sound.note is None:
        (t.add_notes(None, v))
    else:
        (t.add_notes(sound.symbol, v))

    
def add_sound1(t, sound, duration):
    for _ in range(duration):
        if sound.note is None:
            (t.add_notes(None, 32))
        else:
            (t.add_notes(sound.symbol, 32))
    

def add_sound2(t, sound, duration):
    if sound.note is not None:
        pitch = sound.note + 60
        t.addNote(0, 0, pitch, sound.timestamp, sound.duration, 100)


def add_chord(t, chord, duration):
    v = 32
    for _ in range(duration-1):
        v = value.add(v, 32)
    if chord.note is None:
        (t.add_notes(None, v))
    else:
        sounds = [s.symbol for s in chord.sounds()]
        (t.add_notes(NoteContainer(sounds), v))


def add_chord1(t, chord, duration):
    for _ in range(duration):
        if chord.note is None:
            (t.add_notes(None, 1))
        else:
            sounds = [s.symbol for s in chord.sounds()]
            (t.add_notes(NoteContainer(sounds), 1))


def add_chord2(t, chord, duration):
    if chord.note is not None:
        for sound in chord.sounds():
            pitch = sound.note + 60
            t.addNote(0, 0, pitch, chord.timestamp, chord.duration, 100)
    

def wav_from_sounds(sounds, beat_duration, filename):
    v_sum = sum([round(sound.duration*8/beat_duration) for sound in sounds])
    print(v_sum)

    t = Track()
    # t.add_bar(Bar(meter=(round(v_sum/32)+1, 1)))

    for s in sounds:
        v_act = round(s.duration*8/beat_duration)

        add_sound1(t, s, v_act)

    midi_file_out.write_Track(filename + ".mid", t)
    fs = FluidSynth()
    fs.midi_to_audio(filename + '.mid', filename + '.wav')
    return pathlib.Path(filename + '.wav')


def wav_from_sounds1(sounds, beat_duration, filename):
    MyMIDI = MIDIFile(1)

    for s in sounds:
        v_act = round(s.duration*8/beat_duration)

        add_sound2(MyMIDI, s, v_act)

    with open(filename + ".mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
    fs = FluidSynth()
    fs.midi_to_audio(filename + '.mid', filename + '.wav')
    return pathlib.Path(filename + '.wav')



def wav_from_chords(sounds, beat_duration, filename):
    v_sum = sum([round(sound.duration*8/beat_duration) for sound in sounds])
    print(v_sum)

    t = Track()
    # t.add_bar(Bar(meter=(round(v_sum/32)+1, 1)))

    for s in sounds:
        v_act = round(s.duration*8/beat_duration)

        add_chord1(t, s, v_act)

    midi_file_out.write_Track(filename + ".mid", t)
    fs = FluidSynth()
    fs.midi_to_audio(filename + '.mid', filename + '.wav')
    return pathlib.Path(filename + '.wav')



def wav_from_chords1(sounds, beat_duration, filename):
    MyMIDI1 = MIDIFile(1)

    for s in sounds:
        v_act = round(s.duration*8/beat_duration)

        add_chord2(MyMIDI1, s, v_act)

    with open(filename + ".mid", "wb") as output_file:
        MyMIDI1.writeFile(output_file)
    fs = FluidSynth()
    fs.midi_to_audio(filename + '.mid', filename + '.wav')
    return pathlib.Path(filename + '.wav')



