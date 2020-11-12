from music.sound import Sound
from pydub import AudioSegment
import argparse
import pathlib

import tonations_generation
import sounds_generation
import chords_generation
import meter_recognition
import music_synthesis
import sounds_manipulation
import perfect_sounds_creation


# BEAT_TO_NOTE_VERSION = "compare_adjacent"
# BEAT_TO_NOTE_VERSION = "compare_absolute"
BEAT_TO_NOTE_VERSION = "brojaczj_algorithm"
# BEAT_TO_NOTE_VERSION = "compare_adjacent"

def parse_args():
    parser = argparse.ArgumentParser(
        description='Add chords to audio file')
    parser.add_argument('--input', '-I',
                        required=True,
                        help='Input audio file. Formats: [.mp3, .wav]',
                        type=pathlib.Path)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    file = args.input
    sounds = sounds_generation.get_sounds_from_file(file)
    # sounds = sounds_manipulation.change_tonation(sounds, 2)

    beat, accents = meter_recognition.get_meter(file, sounds)
    if BEAT_TO_NOTE_VERSION == "compare_adjacent":
        meter_recognition.update_sounds_with_beat_fractions_compare_adjacent(sounds, beat)
    elif BEAT_TO_NOTE_VERSION == "compare_absolute":
        meter_recognition.update_sounds_with_beat_fractions_compare_absolute(sounds, beat)
    elif  BEAT_TO_NOTE_VERSION == "brojaczj_algorithm":
        meter_recognition.update_sounds_brojaczj_algorithm(beat, accents, sounds)
    else:
        raise(f"BEAT_TO_NOTE_VERSION '{BEAT_TO_NOTE_VERSION}'' not recognized")

    print(f"Beat: {beat}")

    print("Sounds:")
    print("\n".join([f"{sound.timestamp:.3f}: {sound.symbol}\t{sound.duration:.3f} ({sound.duration_signature})" for sound in sounds]))  # noqa

    tonation = tonations_generation.get_tonations_from_sounds(sounds)
    tonation = tonation[0]

    chords = chords_generation.get_chords(sounds, tonation, beat, sounds[0].timestamp)

    print("Chords:")
    print("\n".join([f"{chord.timestamp:.3f}: {chord}\t{chord.duration:.3f}" for chord in chords]))  # noqa

    music_synthesis.midi_from_sounds(sounds, 'sounds')
    music_synthesis.midi_from_chords(chords, 'chords')

    sound1 = AudioSegment.from_file("sounds.mid")
    sound2 = AudioSegment.from_file("chords.mid")
    sound1.export("sounds.wav", format='wav')
    sound2.export("chords.wav", format='wav')

    # change volume
    sound2 = sound2 - 8

    # mix sounds and chords
    combined = sound1.overlay(sound2)
    
    combined.export("result.wav", format='wav')
    perfect_sounds = perfect_sounds_creation.get_perfect_sounds(sounds, beat)

    music_synthesis.midi_from_sounds(perfect_sounds, 'perfect_sounds')
    perfect_sounds_as = AudioSegment.from_file("perfect_sounds.mid")
    perfect_sounds_as.export("perfect_sounds.wav", format='wav')
