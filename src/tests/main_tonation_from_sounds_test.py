import argparse
from os import times

import test_data
import music
import tonations_generation


def parse_args():
    parser = argparse.ArgumentParser(
        description='Test getting tonations from sounds')
    parser.add_argument('--verbose_factor_threshold', '-Vft',
                required=False,
                help='Color red and print full mismatches list for tests with match factor lesser than VERBOSE_FACTOR_THRESHOLD',
                type=float)
    parser.add_argument('--verbose_duration_threshold', '-Vdt',
                        required=False,
                        help='Print only mismatches with duration greater than VERBOSE_DURATION_THRESHOLD',
                        type=float)
    args = parser.parse_args()
    return args

class Mismatch(music.Tonation):
    def __init__(self, note_computed, note_model, kind_computed, kind_model, timestamp, duration):
        super().__init__(note_computed, timestamp, duration, kind_computed)
        self.note_model = note_model
        self.kind_model = kind_model

    @property
    def tonation_model(self):
        if self.note_model is None:
            symbol = 'None'
        else:
            symbols = ['C', 'C#', 'D', 'D#', 'E',
                    'F', 'F#', 'G', 'G#', 'A', 'A#', 'H']
            symbol = symbols[self.note_model]
        return f"{symbol}-{self.kind_model}"

    def __str__(self):
        return f"{round(self.timestamp, 3)} - {round(self.end_timestamp, 3)}: Expected {self.tonation_model}, got {super().__str__()}"

def match_tonations(tonations_computed, tonations_model):
    duration = tonations_computed[-1].end_timestamp
    duration_model = tonations_model[-1].end_timestamp
    mismatches = []
    i = 0
    j = 0
    timestamp = 0.0
    while i < len(tonations_computed) and j < len(tonations_model):
        note_computed = tonations_computed[i].note
        kind_computed = tonations_computed[i].kind
        note_model = tonations_model[j].note
        kind_model = tonations_model[i].kind
        if tonations_computed[i].end_timestamp < tonations_model[j].end_timestamp:
            next_timestamp = tonations_computed[i].end_timestamp
            i = i + 1
        else:
            next_timestamp = tonations_model[j].end_timestamp
            j = j + 1
        if note_computed != note_model or kind_computed != kind_model:
            mismatches.append(Mismatch(note_computed, note_model, kind_computed, kind_model, timestamp, next_timestamp-timestamp))
        timestamp = next_timestamp

    mismatches_duration = sum([m.duration for m in mismatches])
    if duration != duration_model:
        mismatches_duration += abs(duration - duration_model)
        # not sure what to do when this happens
    return 1-mismatches_duration/duration, mismatches

if __name__ == "__main__":
    verbose_factor_threshold = parse_args().verbose_factor_threshold
    verbose_duration_threshold = parse_args().verbose_duration_threshold
    if verbose_factor_threshold == None:
        verbose_factor_threshold = 0.5
    if verbose_duration_threshold == None:
        verbose_duration_threshold = 0.1
    tests = test_data.get_all_test_models()
    print("-----------TONATIONS TEST-----------------")
    for test in tests:
        tonations = tonations_generation.get_tonations_from_sounds(test.sounds)
        match_factor, mismatches = match_tonations(tonations, test.tonations)
        if match_factor > verbose_factor_threshold:
            color = '\033[92m'
        else:
            color = '\033[91m'
        print(f"{test.file_path}: {color}{round(match_factor*100, 3)}% \033[0m match")
        if match_factor < verbose_factor_threshold:
            print("\tMismatches:")
            no_too_short_mismatches = 0
            for mismatch in mismatches:
                if mismatch.duration > verbose_duration_threshold:
                    print(f"\t\t{mismatch}\n")
                else:
                    no_too_short_mismatches += 1
            print(f"\tRejected {no_too_short_mismatches} mismatches shorter than {verbose_duration_threshold}")
