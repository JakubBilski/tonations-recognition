from flask import Flask, request, jsonify

import datetime
import pathlib
import logging
import shutil
import pydub
import os

from . import chords_simplification
from . import key_recognition
from . import chords_generation
from . import sounds_generation
from . import meter_recognition
from . import music_synthesis
from . import vextab_parsing
from . import music

pydub.AudioSegment.converter = \
    str(pathlib.Path(__file__).parent.parent / "ffmpeg" / "ffmpeg.exe")


BEAT_TO_NOTE_VERSION = "fit_to_bar"

logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger('key_recognition')
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
app.config['TEMP_FOLDER'] = pathlib.Path('data\\temp')


@app.route('/recorded', methods=['POST'])
def frontend_communication_upload_recorded():
    """Used to upload a previously recorded audio file

    Request body:
    files.recordingTemp (binary file) : recorded file in .ogg format

    Response:
    filename (str) : path to a recorded file saved in .wav format
    """
    try:
        file = request.files['recordingTemp']
    except Exception as e:
        logger.error(f"Bad request: {request}\n Exception: {e}")
        return jsonify({
            "error": "Expected file named recordingTemp"
        })
    filename_ogg = app.config['TEMP_FOLDER'] / "recordingTemp.ogg"
    file.save(filename_ogg)
    filename = app.config['TEMP_FOLDER'] / "recordingTemp.wav"
    convert_recorded_to_wav(filename_ogg, filename)
    return jsonify({"filename": str(filename)})


@app.route('/saveWithChords', methods=['POST'])
def frontend_communication_save_with_chords():
    """Used to copy generated music file to a chosen file

    Request body:
    output_file (str) : path to the chosen file
    """
    try:
        filename_dest = request.json["output_file"]
    except Exception as e:
        logger.error(f"Bad request: {request}\n Exception: {e}")
        return jsonify({
            "error": "Expected json with output_file key"
        })
    filename_src = app.config['TEMP_FOLDER'] / "output.wav"
    shutil.copyfile(filename_src, filename_dest)
    return jsonify({})


@app.route('/saveRecorded', methods=['POST'])
def frontend_communication_save_recorded():
    """Used to copy recorded track file to a chosen file

    Request body:
    output_file (str) : path to the chosen file
    """
    try:
        filename_dest = request.json["output_file"]
    except Exception as e:
        logger.error(f"Bad request: {request}\n Exception: {e}")
        return jsonify({
            "error": "Expected json with output_file key"
        })
    print(filename_dest)
    filename_src = app.config['TEMP_FOLDER'] / "recordingTemp.wav"
    print(filename_src)
    shutil.copyfile(filename_src, filename_dest)
    return jsonify({})


@app.route('/music', methods=['GET', 'POST'])
def frontend_communication():
    """Used to obtain all the information about chosen music file

    Request body:
    input_file (str) : path to the chosen file

    Response:
    notes (List[str]): Lines of notes prepared for displaying
    key (str): Key of the whole piece, prepared for displaying
    metrum (str): Metrum of the whole piece, prepared for displaying
    chord_types (list[str]) : All chords used in the piece,
        prepared for displaying
    chords: (list[{
        symbol (str): symbol of the chord, see: Chord
        kind (str): kind of the chord, see: Chord
        duration: duration of the chord, see: Chord
    }]) : Chords used in the piece
    key ({
        symbol (str): symbol of the key, see: Key
        kind: kind of the key, see: Key
    }): The key the piece is in
    preview_file (str) : Path to the audio file
        with melody and chords played together
    """
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
    notes, chords, key, preview_file = process_file(filename, False)
    return jsonify(render_result(notes, chords, key, preview_file, 4, 8))


@app.route('/music_simple', methods=['GET', 'POST'])
def frontend_communication_simple():
    """Used to obtain all the information about chosen music file
    transposed into some easier key"""
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
    notes, chords, key, preview_file = process_file(filename, True)
    return jsonify(render_result(notes, chords, key, preview_file, 4, 8))


def render_result(notes, chords, key, preview_file,
                  metrum_upper, metrum_lower):
    return {
        "notes": vextab_parsing.generate_vextab_notes(
            notes, metrum_upper, metrum_lower),
        "chords": vextab_parsing.generate_vextab_chords(
            chords, metrum_upper, metrum_lower),
        "key": vextab_parsing.generate_vextab_key(key),
        "metrum": vextab_parsing.generate_vextab_metrum(
            metrum_upper, metrum_lower),
        "chord_types": vextab_parsing.generate_vextab_chord_types(chords),
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


def process_file(filename, is_simplified: bool, force_key=None):
    logger.debug(f"Procesing {filename}")
    sounds = sounds_generation.get_sounds_from_file(filename)
    # sounds = sounds_manipulation.change_key(sounds, 2)

    meter, beats = meter_recognition.get_meter(filename, sounds)
    if BEAT_TO_NOTE_VERSION == "fit_to_bar":
        meter_recognition.update_sounds_with_rhythmic_values_fit_to_bar(
            meter, beats, sounds)
    else:
        raise(f"BEAT_TO_NOTE_VERSION '{BEAT_TO_NOTE_VERSION}'' not recognized")

    if force_key:
        if force_key.islower():
            kind = "minor"
        else:
            kind = "major"
        key = music.Key(symbol=force_key.lower(), kind=kind)
    else:
        key = key_recognition.get_key(sounds)

    chords = chords_generation.get_chords_daria(sounds, key, (4, 8))

    duration_ms_of_32 = meter / 4

    if is_simplified:
        sounds, chords, key =\
            chords_simplification.simplify(sounds, chords, key)

    for x in app.config['TEMP_FOLDER'].iterdir():
        if x.is_file():
            file_str = str(x.name)
            if len(file_str) >= 7:
                if is_simplified and file_str[0:7] == "outbase":
                    x.unlink()
                elif not is_simplified and file_str[0:7] == "outsimp":
                    x.unlink()

    temp_file = music_synthesis.create_midi(
        app.config['TEMP_FOLDER'] / "output.midi",
        sounds,
        chords,
        duration_ms_of_32)
    if os.name == 'nt':
        temp_file = music_synthesis.save_midifile_as_wav_windows(
            app.config['TEMP_FOLDER'] / "output.midi",
            app.config['TEMP_FOLDER'] / "output.wav")
    else:
        temp_file = music_synthesis.save_midifile_as_wav_linux(
            app.config['TEMP_FOLDER'] / "output.midi",
            app.config['TEMP_FOLDER'] / "output.wav")

    timestamp = datetime.datetime.now().strftime('%m%d%H%M%S')
    if is_simplified:
        unique_preview_file = f"outbase{timestamp}.ogg"
    else:
        unique_preview_file = f"outsimp{timestamp}.ogg"
    prev_file = app.config['TEMP_FOLDER'] / unique_preview_file
    convert_wav_to_ogg(
        temp_file,
        prev_file,
    )
    logger.debug(f"Meter:\t\t{meter}")
    logger.debug(f"Key:\t\t{key}")
    print_debug_info(sounds, chords)
    logger.debug(f"Preview file:\t\t{prev_file}")

    return sounds, chords, key, str(prev_file.absolute())


def convert_recorded_to_wav(source_file, destination_file):
    sound = pydub.AudioSegment.from_file(source_file)
    sound.export(destination_file, format="wav")


def convert_wav_to_ogg(source_file, destination_file):
    sound = pydub.AudioSegment.from_wav(source_file)
    sound.export(destination_file, format="ogg")


def start_server(args):
    if args.http:
        app.run()
    else:
        process_file(args.input, False, args.key)
