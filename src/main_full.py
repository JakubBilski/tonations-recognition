from music.sound import Sound
from pydub import AudioSegment
import argparse
import pathlib

import tonations_generation
import sounds_generation
import chords_generation
import meter_recognition
import music_synthesis


# BEAT_TO_NOTE_VERSION = "compare_adjacent"
BEAT_TO_NOTE_VERSION = "compare_absolute"

def parse_args():
    parser = argparse.ArgumentParser(
        description='Add chords to audio file')
    parser.add_argument('--input', '-I',
                        required=True,
                        help='Input audio file. Formats: [.mp3, .wav]',
                        type=pathlib.Path)
    args = parser.parse_args()
    return args



def example_beat_to_note_value(sounds, beat):
    # this function is only for demonstrational purposes, we need to determine if and where we want to do this
    # finds what note value will be equal to the beat
    # this is equivalent to setting the lower numeral in a time signature
    # this is also probably really bad
    if beat < 0.5:
        # allegro and faster, we use eighth notes
        beat_note_value = 0.125
    elif beat > 0.66:
        # andante and slower, half notes
        beat_note_value = 0.5
    else:
        # moderato-ish, quarter notes
        beat_note_value = 0.25
    return beat_note_value

def example_note_value_to_name(note_value):
    # only for demonstration
    if note_value > 1.5:
        return "Too long, need to divide it"
    # brace yourselves, a float dictionary is coming
    note_value_to_name = {
        1.5: "dotted whole note",
        1: "whole note",
        0.75: "dotted half note",
        0.5: "half note",
        0.375: "dotted quarternote",
        0.25: "quarternote",
        0.1875: "dotted eighth note",
        0.125: "eighth note",
        0.09375: "dotted sixteenth note",
        0.0625: "sixteenth note",
        0.046875: "dotted thirty-second note",
        0.03125: "thirty-second note",
        0.0234375: "dotted sixty-fourth note",
        0.015625: "sixty-fourth note",
        0.01171875: "dotted hundred twenty-eighth note",
        0.0078125: "hundred twenty-eighth note",
    }
    # bottom values are just to show that we still get very short sound values
    return note_value_to_name[note_value]

if __name__ == "__main__":
    args = parse_args()
    file = args.input
    sounds = sounds_generation.get_sounds_from_file(file)

    beat = meter_recognition.get_beat_from_file(file)
    if BEAT_TO_NOTE_VERSION == "compare_adjacent":
        meter_recognition.update_sounds_with_beat_fractions_compare_adjacent(sounds, beat)
    elif BEAT_TO_NOTE_VERSION == "compare_absolute":
        meter_recognition.update_sounds_with_beat_fractions_compare_absolute(sounds, beat)
    else:
        raise(f"BEAT_TO_NOTE_VERSION '{BEAT_TO_NOTE_VERSION}'' not recognized")

    beat_as_note = example_beat_to_note_value(sounds, beat)
    print(f"Beat: {beat}, one beat duration assigned to a {example_note_value_to_name(beat_as_note)}")

    print("Sounds:")
    print("\n".join([f"{sound.timestamp:.3f}: {sound.symbol}\t{sound.duration:.3f} ({example_note_value_to_name(sound.beat_fraction * beat_as_note)})" for sound in sounds]))  # noqa

    tonation = tonations_generation.get_tonations_from_sounds(sounds)
    tonation = tonation[0]
    chords = chords_generation.get_chords(sounds, tonation, beat, sounds[0].timestamp)

    print("Chords:")
    print("\n".join([f"{chord.timestamp:.3f}: {chord}\t{chord.duration:.3f}" for chord in chords]))  # noqa

    music_synthesis.midi_from_sounds(sounds, 'sounds')
    music_synthesis.midi_from_chords(chords, 'chords')

    sound1 = AudioSegment.from_file("sounds.wav")
    sound2 = AudioSegment.from_file("chords.wav")

    # change volume
    sound2 = sound2 - 8

    # mix sounds and chords
    combined = sound1.overlay(sound2)

    combined.export("result.wav", format='wav')

    perfect_sounds = []
    current_end_timestamp = 0.0
    for sound in sounds:
        perfect_sounds.append(Sound(sound.note, current_end_timestamp, sound.beat_fraction*beat))
        current_end_timestamp += sound.beat_fraction*beat

    music_synthesis.midi_from_sounds(perfect_sounds, 'perfect_sounds')
