from pydub import AudioSegment
import argparse
import pathlib

import tonation_recognition
import sounds_generation
import chords_generation
import meter_recognition
import music_synthesis
import sounds_manipulation
import perfect_sounds_creation


# BEAT_TO_NOTE_VERSION = "compare_adjacent"
# BEAT_TO_NOTE_VERSION = "compare_absolute"
BEAT_TO_NOTE_VERSION = "brojaczj_algorithm"


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

    meter, beats = meter_recognition.get_meter(file, sounds)
    if BEAT_TO_NOTE_VERSION == "compare_adjacent":
        meter_recognition.update_sounds_with_rhytmic_values_compare_adjacent(
            sounds, meter)
    elif BEAT_TO_NOTE_VERSION == "compare_absolute":
        meter_recognition.update_sounds_with_rhytmic_values_compare_absolute(
            sounds, meter)
    elif BEAT_TO_NOTE_VERSION == "brojaczj_algorithm":
        meter_recognition.update_sounds_with_rhytmic_values_brojaczj_algorithm(
            meter, beats, sounds)
    else:
        raise(f"BEAT_TO_NOTE_VERSION '{BEAT_TO_NOTE_VERSION}'' not recognized")

    print(f"Meter: {meter}")

    print("Sounds:")
    print("\n".join([f"{sound.timestamp:.3f}: {sound.symbol}\t{sound.duration_ms:.3f} ({sound.rhytmic_value})" for sound in sounds]))  # noqa

    tonation = tonation_recognition.get_tonation(sounds)

    chords = chords_generation.get_chords(sounds, tonation, (4, 8))

    print("Chords:")
    print("\n".join([f"{chord}\t{chord.duration:.3f}" for chord in chords]))  # noqa

    # music_synthesis.midi_from_sounds(sounds, 'sounds')
    # music_synthesis.midi_from_chords(chords, 'chords')

    # sound1 = AudioSegment.from_file("sounds.mid")
    # sound2 = AudioSegment.from_file("chords.mid")
    # sound1.export("sounds.wav", format='wav')
    # sound2.export("chords.wav", format='wav')

    # # change volume
    # sound2 = sound2 - 8

    # # mix sounds and chords
    # combined = sound1.overlay(sound2)

    # combined.export("result.wav", format='wav')
    # perfect_sounds = perfect_sounds_creation.get_perfect_sounds(sounds, meter)

    # music_synthesis.midi_from_sounds(perfect_sounds, 'perfect_sounds')
    # perfect_sounds_as = AudioSegment.from_file("perfect_sounds.mid")
    # perfect_sounds_as.export("perfect_sounds.wav", format='wav')
