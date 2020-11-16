import pathlib

from midiutil.MidiFile import MIDIFile
from midi2audio import FluidSynth

from utils import constants


def add_sound(track, sound, start_time):
    duration = sound.rhythmic_value_time
    if sound.note is not None:
        pitch = sound.note + 60
        track.addNote(0, 0, pitch, start_time, duration, 100)
    return duration


def add_chord(track, chord, start_time):
    chord_duration = constants.RHYTHMIC_VALUE_TO_TIME["8"]*chord.duration
    if chord.note is not None:
        for sound in chord.sounds():
            pitch = sound.note + 60
            track.addNote(0, 1, pitch, start_time,
                          chord_duration,
                          50)
    return chord_duration


def create_midi(filename, sounds, chords):
    midifile = MIDIFile(1)

    start_time = 0
    for s in sounds:
        start_time += add_sound(midifile, s, start_time)

    start_time = 0
    for c in chords:
        start_time += add_chord(midifile, c, start_time)

    with open(filename, "wb") as output_file:
        midifile.writeFile(output_file)

    return pathlib.Path(filename).absolute()


def ly_from_sounds(sounds, filename):
    with open(filename, 'w') as f:
        print('\\version "2.12.3"', file=f)
        print('\\score {', file=f)
        print('\\relative c\' {', file=f)
        print('\\time 4/4', file=f)
        for s in sounds:
            if s.note is None:
                f.write(f" r{s.beat_fraction}")
            else:
                f.write(
                    f" {s.symbol.lower().replace('#', 'is')}{s.beat_fraction}")
        print('', file=f)
        print('}', file=f)
        print('\\midi{}', file=f)
        print('}', file=f)
