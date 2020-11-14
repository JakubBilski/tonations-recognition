import pathlib
import os

from music.sound import Sound
from music.tonation import Tonation


class TestModel:
    def __init__(self, file_path=None, sounds=None, tonation=None, chords=None):
        self.file_path = file_path
        self.sounds = sounds
        self.tonation = tonation
        self.chords = chords


def get_all_test_models():
    models = get_other_rec_test_models()
    return models


def get_other_rec_test_models():
    result = []
    test_data_file = pathlib.Path(
        os.path.realpath(__file__)).parent / "test_data.txt"

    current_testcase = None
    currect_sounds = None
    with open(test_data_file, 'r') as f:
        for line in f:
            if 'wav' in line:
                if current_testcase is not None:
                    current_testcase.sounds = currect_sounds
                    result.append(current_testcase)
                current_testcase = TestModel(pathlib.Path(line.strip()))
                currect_sounds = []
            elif line.startswith('t'):
                kind = 'major' if line.split()[1].isupper() else 'minor'
                current_testcase.tonation = Tonation(symbol=line.split()[1], kind=kind)
            elif len(line.split()) == 3:
                spl = line.split()
                currect_sounds.append(
                    Sound(symbol=spl[0], duration_signature=spl[2]))
            elif line.startswith('r'):
                spl = line.split()
                currect_sounds.append(
                    Sound(note=None, duration_signature=spl[1]))
    return result
