import argparse

from . import test_data
from .. import music
from .. import key_recognition


def parse_args():
    parser = argparse.ArgumentParser(
        description='Test getting key from sounds')
    parser.add_argument('--verbose_factor_threshold', '-Vft',
                        required=False,
                        help='Color red and print full mismatches list for tests with match factor lesser than VERBOSE_FACTOR_THRESHOLD',  # noqa
                        type=float)
    parser.add_argument('--verbose_duration_threshold', '-Vdt',
                        required=False,
                        help='Print only mismatches with duration greater than VERBOSE_DURATION_THRESHOLD',  # noqa
                        type=float)
    args = parser.parse_args()
    return args


class Mismatch(music.Key):
    def __init__(self, note_computed, note_model, kind_computed, kind_model,
                 timestamp, duration_ms):
        super().__init__(note_computed, timestamp, duration_ms, kind_computed)
        self.note_model = note_model
        self.kind_model = kind_model

    @property
    def key_model(self):
        if self.note_model is None:
            symbol = 'None'
        else:
            symbols = ['C', 'C#', 'D', 'D#', 'E',
                       'F', 'F#', 'G', 'G#', 'A', 'A#', 'H']
            symbol = symbols[self.note_model]
        return f"{symbol}-{self.kind_model}"

    def __str__(self):
        return f"{round(self.timestamp, 3)} - {round(self.end_timestamp, 3)}: Expected {self.key_model}, got {super().__str__()}"  # noqa


def run_tests():
    verbose_factor_threshold = parse_args().verbose_factor_threshold
    verbose_duration_threshold = parse_args().verbose_duration_threshold
    if verbose_factor_threshold is None:
        verbose_factor_threshold = 0.5
    if verbose_duration_threshold is None:
        verbose_duration_threshold = 0.1
    tests = test_data.get_all_test_models()
    print("-----------TONATIONS TEST-----------------")
    for test in tests:
        key = key_recognition.get_key(test.sounds)
        match = key == test.key
        if match:
            color = '\033[92m'
            print(f"{test.file_path}: {color} {key} matches {test.key} \033[0m")  # noqa
        else:
            color = '\033[91m'
            print(f"{test.file_path}: {color}{key} doesn't match {test.key} \033[0m")  # noqa
