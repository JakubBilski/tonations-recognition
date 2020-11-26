from pydub import AudioSegment
from flask import Flask, request, jsonify
import argparse
import pathlib
import logging

import music
import vextab_parsing
import music_synthesis
import sounds_generation
import chords_generation
import meter_recognition
import sounds_manipulation
import tonation_recognition
import chords_simplification
from utils import constants


BEAT_TO_NOTE_VERSION = "fit_to_bar"

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
    parser.add_argument('--tonation', '-T',
                        help='Use correct tonation instead of detected',
                        type=str)
    parser.add_argument('--wav',
                        action="store_true",
                        help='Save file as WAVE; works only on linux')
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
    return jsonify(render_result(notes, chords, tonation, preview_file, 4, 8))


@app.route('/music_simple', methods=['GET', 'POST'])
def frontend_communication_simple():
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
    notes, chords, tonation, preview_file = \
        chords_simplification.simplify(*process_file(filename))
    return jsonify(render_result(notes, chords, tonation, preview_file, 4, 8))

def render_result(notes, chords, tonation, preview_file, metrum_upper, metrum_lower):
    return {
        "notes": vextab_parsing.generate_vextab_notes(notes, tonation, metrum_upper,metrum_lower),
        "key": vextab_parsing.generate_vextab_key(tonation),
        "metrum": vextab_parsing.generate_vextab_metrum(metrum_upper, metrum_lower),
        "chord_types": vextab_parsing.generate_vextab_chord_types(chords),
        "chords": [
            {
                "symbol": chord.symbol,
                "kind": chord.kind,
                "duration": chord.duration*4
            }
            for chord in chords
        ],
        "tonation": {
            "symbol": tonation.symbol,
            "kind": tonation.kind
        },
        "preview_file": preview_file
    }

def print_debug_info(sounds, chords):
    logger.debug("Melody with chords:")
    sounds_i = 0
    sounds_time = 0
    chords_i = 0
    chords_time = 0
    while sounds_i < len(sounds) or chords_i < len(chords):
        if chords_i >= len(chords) or sounds_time < chords_time:
            logger.debug(f"\t\t{sounds[sounds_i]}")
            sounds_time += sounds[sounds_i].duration
            sounds_i += 1
        elif sounds_i >= len(sounds) or sounds_time > chords_time:
            logger.debug(f"\t\t\t\t\t{chords[chords_i]}")
            chords_time += chords[chords_i].duration
            chords_i += 1
        else:
            logger.debug(f"\t\t{sounds[sounds_i]}\t{chords[chords_i]}")
            sounds_time += sounds[sounds_i].duration
            sounds_i += 1
            chords_time += chords[chords_i].duration
            chords_i += 1


def process_file(filename):
    logger.debug(f"Procesing {filename}")
    sounds = sounds_generation.get_sounds_from_file(filename)
    # sounds = sounds_manipulation.change_tonation(sounds, 2)

    meter, beats = meter_recognition.get_meter(filename, sounds)
    if BEAT_TO_NOTE_VERSION == "fit_to_bar":
        meter_recognition.update_sounds_with_rhythmic_values_fit_to_bar(
            meter, beats, sounds)
    else:
        raise(f"BEAT_TO_NOTE_VERSION '{BEAT_TO_NOTE_VERSION}'' not recognized")

    if args.tonation:
        if args.tonation.islower():
            kind = "minor"
        else:
            kind = "major"
        tonation = music.Tonation(symbol=args.tonation.lower(), kind=kind)
    else:
        tonation = tonation_recognition.get_tonation(sounds)

    chords = chords_generation.get_chords_daria(sounds, tonation, (4, 8))

    duration_ms_of_32 = meter / 4
    result_file = music_synthesis.create_midi("output.midi", sounds,
                                              chords, duration_ms_of_32)
    if args.wav:
        result_file = music_synthesis.save_midifile_as_wav("output.midi",
                                                           "output.wav")

    logger.debug(f"Meter:\t\t{meter}")
    logger.debug(f"Tonation:\t\t{tonation}")
    print_debug_info(sounds, chords)
    logger.debug(f"Result file:\t\t{result_file}")

    return sounds, chords, tonation, str(result_file)


if __name__ == "__main__":
    args = parse_args()
    if args.http:
        app.run()
    else:
        process_file(args.input)
