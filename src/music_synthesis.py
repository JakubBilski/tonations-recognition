import pathlib

from midiutil.MidiFile import MIDIFile
from midi2audio import FluidSynth


def add_sound(track, sound, start_time, duration_ms_of_32):
    duration = sound.duration * duration_ms_of_32
    if sound.note is not None:
        pitch = sound.note + 60
        track.addNote(0, 0, pitch, start_time, duration, 100)
    return duration


def add_chord(track, chord, start_time, duration_ms_of_32):
    chord_duration = chord.duration * duration_ms_of_32
    if chord.note is not None:
        for sound in chord.sounds():
            pitch = sound.note + 60
            track.addNote(0, 1, pitch, start_time,
                          chord_duration,
                          50)
    return chord_duration


def create_midi(filename, sounds, chords, duration_ms_of_32):
    midifile = MIDIFile(1)

    start_time = 0
    for s in sounds:
        start_time += add_sound(midifile, s, start_time, duration_ms_of_32)

    start_time = 0
    for c in chords:
        start_time += add_chord(midifile, c, start_time, duration_ms_of_32)

    with open(filename, "wb") as output_file:
        midifile.writeFile(output_file)

    return pathlib.Path(filename).absolute()


def save_midifile_as_wav(midi, wav):
    # experimental, only works on linux
    fs = FluidSynth()
    fs.midi_to_audio(midi, wav)
    return pathlib.Path(wav)


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
