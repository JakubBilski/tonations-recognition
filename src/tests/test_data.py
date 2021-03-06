import pathlib
import os

from ..music.sound import Sound
from ..music.key import Key
from ..utils import constants


class TestModel:
    def __init__(self, file_path=None, sounds=None, key=None,
                 chords=None):
        self.file_path = file_path
        self.sounds = sounds
        self.key = key
        self.chords = chords


def get_all_test_models():
    models = get_other_rec_test_models()
    models.extend(get_carol_test_models())
    models.extend(get_perfect_test_models())
    return models


def get_other_rec_test_models():
    test_data_file = pathlib.Path(
        os.path.realpath(__file__)).parent / "test_data.txt"
    return _get_test_models(test_data_file)


def get_carol_test_models():
    test_data_file = pathlib.Path(
        os.path.realpath(__file__)).parent / "test_carol.txt"
    return _get_test_models(test_data_file)


def get_perfect_test_models():
    test_data_file = pathlib.Path(
        os.path.realpath(__file__)).parent / "test_perfect.txt"
    return _get_test_models(test_data_file)


def get_perfect_guitar_test_models():
    test_data_file = pathlib.Path(
        os.path.realpath(__file__)).parent / "test_perfect_guitar.txt"
    return _get_test_models(test_data_file)


def _get_test_models(test_data_file):
    result = []
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
                current_testcase.key = Key(
                    symbol=line.split()[1], kind=kind)
            elif len(line.split()) == 3:
                spl = line.split()
                currect_sounds.append(
                    Sound(symbol=spl[0],
                          duration=constants.RHYTMIC_VALUE_TO_DURATION[spl[2]])
                )
            elif line.startswith('r'):
                spl = line.split()
                currect_sounds.append(
                    Sound(note=None,
                          duration=constants.RHYTMIC_VALUE_TO_DURATION[spl[1]])
                )
    current_testcase.sounds = currect_sounds
    result.append(current_testcase)
    return result
