import pathlib

from midiutil.MidiFile import MIDIFile
from midi2audio import FluidSynth


def add_sound(track, sound):
    if sound.note is not None:
        pitch = sound.note + 60
        track.addNote(0, 0, pitch, sound.timestamp, sound.duration, 100)


def add_chord(track, chord):
    if chord.note is not None:
        for sound in chord.sounds():
            pitch = sound.note + 60
            track.addNote(0, 0, pitch, chord.timestamp, chord.duration, 100)


def save_midifile_as_wav(midifile, filename):
    with open(filename + ".mid", "wb") as output_file:
        midifile.writeFile(output_file)
    fs = FluidSynth()
    fs.midi_to_audio(filename + '.mid', filename + '.wav')
    return pathlib.Path(filename + '.wav')


def midi_from_sounds(sounds, filename):
    midifile = MIDIFile(1)

    for s in sounds:
        add_sound(midifile, s)

    return save_midifile_as_wav(midifile, filename)


def midi_from_chords(chords, filename):
    midifile = MIDIFile(1)

    for c in chords:
        add_chord(midifile, c)

    return save_midifile_as_wav(midifile, filename)