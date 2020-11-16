from pydub import AudioSegment
from flask import Flask, request, jsonify
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


# BEAT_TO_NOTE_VERSION = "compare_absolute"
BEAT_TO_NOTE_VERSION = "brojaczj_algorithm"

logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger('tonation_recognition')
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


@app.route('/music', methods=['GET', 'POST'])
def frontend_communication():
    try:
        filename = request.json["input_file"]
    except Exception as e:
        logger.error(f"Bad request: {request}\n Exception: {e}")
        return jsonify({
            "error": "Expected json with input_file key"
        })
    filename = pathlib.Path(filename)
    if not filename.is_file():
        logger.error(f"File {filename} does not exist.")
        return jsonify({
            "error": f"File {filename} does not exist."
        })
    notes, chords, tonation, preview_file = process_file(filename)
    result = {
        "notes": [
            {
                "symbol": note.symbol,
                "rhythmic_value": note.rhythmic_value
            }
            for note in notes
        ],
        "chords": [
            {
                "symbol": chord.symbol,
                "kind": chord.kind,
                "duration": chord.duration
            }
            for chord in chords
        ],
        "tonation": {
            "symbol": tonation.symbol,
            "kind": tonation.kind
        },
        "preview_file": preview_file
    }
    return jsonify(result)


def process_file(filename):
    logger.debug(f"Procesing {filename}")
    sounds = sounds_generation.get_sounds_from_file(filename)
    # sounds = sounds_manipulation.change_tonation(sounds, 2)

    meter, beats = meter_recognition.get_meter(filename, sounds)
    if BEAT_TO_NOTE_VERSION == "compare_absolute":
        meter_recognition.update_sounds_with_rhythmic_values_compare_absolute(
            sounds, meter)
    elif BEAT_TO_NOTE_VERSION == "brojaczj_algorithm":
        meter_recognition.update_sounds_with_rhythmic_values_brojaczj_algorithm(
            meter, beats, sounds)
    else:
        raise(f"BEAT_TO_NOTE_VERSION '{BEAT_TO_NOTE_VERSION}'' not recognized")

    logger.debug(f"Meter: {meter}")

    logger.debug("Sounds:")
    for sound in sounds:
        logger.debug(f"{sound.timestamp:.3f}: {sound.symbol}\t{sound.duration_ms:.3f} ({sound.rhythmic_value})")  # noqa

    tonation = tonation_recognition.get_tonation(sounds)

    chords = chords_generation.get_chords(sounds, tonation, (4, 8))

    logger.debug("Chords:")
    for chord in chords:
        logger.debug(f"{str(chord).ljust(20)}\t{chord.duration:.3f}")  # noqa

    return sounds, chords, tonation, "NOT SUPPORTED YET"


if __name__ == "__main__":
    args = parse_args()
    if args.http:
        app.run()
    else:
        process_file(args.input)
    