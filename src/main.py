from pydub import AudioSegment
from flask import Flask, request
import argparse
import pathlib
import logging

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

logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger('tonation_recognision')
logger.setLevel(logging.DEBUG)

app = Flask(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Add chords to audio file')
    parser.add_argument('--http', '-H',
                        action="store_true",
                        help='Run program as http server')
    parser.add_argument('--input', '-I',
                        default="data/other_rec/ach_spij_C.wav",
                        help='Input audio file. Formats: [.mp3, .wav]',
                        type=pathlib.Path)
    args = parser.parse_args()
    return args


@app.route('/', methods=['GET', 'POST'])
def process_file(filename):
    logger.debug(f"Procesing {filename}")
    sounds = sounds_generation.get_sounds_from_file(filename)
    # sounds = sounds_manipulation.change_tonation(sounds, 2)

    meter, beats = meter_recognition.get_meter(filename, sounds)
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

    logger.debug(f"Meter: {meter}")

    logger.debug("Sounds:")
    for sound in sounds:
        logger.debug(f"{sound.timestamp:.3f}: {sound.symbol}\t{sound.duration_ms:.3f} ({sound.rhytmic_value})")  # noqa

    tonation = tonation_recognition.get_tonation(sounds)

    chords = chords_generation.get_chords(sounds, tonation, (4, 8))

    logger.debug("Chords:")
    for chord in chords:
        logger.debug(f"{str(chord).ljust(20)}\t{chord.duration:.3f}")  # noqa

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


if __name__ == "__main__":
    args = parse_args()
    if args.http:
        app.run()
    else:
        process_file(args.input)
    