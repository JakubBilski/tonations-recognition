import argparse
from os import times

import test_data
import music
import sounds_generation


def parse_args():
    parser = argparse.ArgumentParser(
        description='Test convering audio files to notes with time of occurrence')
    parser.add_argument('--verbose_factor_threshold', '-Vft',
                        required=False,
                        help='Color red and print full mismatches list for files with match factor lesser than VERBOSE_FACTOR_THRESHOLD',
                        type=float)
    parser.add_argument('--verbose_duration_threshold', '-Vdt',
                        required=False,
                        help='Print only mismatches with duration greater than VERBOSE_DURATION_THRESHOLD',
                        type=float)
    args = parser.parse_args()
    return args


class Mismatch(music.Sound):
    def __init__(self, note_computed, note_model, timestamp, duration):
        super().__init__(note_computed, timestamp, duration)
        self.note_model = note_model

    @property
    def symbol_model(self):
        if self.note_model is None:
            return 'None'
        symbols = ['C', 'C#', 'D', 'D#', 'E',
                   'F', 'F#', 'G', 'G#', 'A', 'A#', 'H']
        return symbols[self.note_model]

    def __str__(self):
        return f"{round(self.timestamp, 3)} - {round(self.end_timestamp, 3)}: Expected {self.symbol_model}, got {self.symbol}"


def match_sounds(sounds_computed, sounds_model):
    duration = sounds_computed[-1].end_timestamp
    duration_model = sounds_model[-1].end_timestamp
    mismatches = []
    i = 0
    j = 0
    timestamp = 0.0
    while i < len(sounds_computed) and j < len(sounds_model):
        note_computed = sounds_computed[i].note
        note_model = sounds_model[j].note
        if sounds_computed[i].end_timestamp < sounds_model[j].end_timestamp:
            next_timestamp = sounds_computed[i].end_timestamp
            i = i + 1
        else:
            next_timestamp = sounds_model[j].end_timestamp
            j = j + 1
        if note_computed != note_model:
            mismatches.append(Mismatch(note_computed, note_model,
                                       timestamp, next_timestamp-timestamp))
        timestamp = next_timestamp

    mismatches_duration = sum([m.duration for m in mismatches])
    if duration != duration_model:
        mismatches_duration += abs(duration - duration_model)
    return 1-mismatches_duration/duration, mismatches


if __name__ == "__main__":
    args = parse_args()
    verbose_factor_threshold = args.verbose_factor_threshold
    verbose_duration_threshold = args.verbose_duration_threshold
    if verbose_factor_threshold == None:
        verbose_factor_threshold = 0.5
    if verbose_duration_threshold == None:
        verbose_duration_threshold = 0.1
    tests = test_data.get_all_test_models()
    print("-----------SOUNDS TEST-----------------")
    for test in tests:
        sounds = sounds_generation.get_sounds_from_file(test.file_path)
        match_factor, mismatches = match_sounds(sounds, test.sounds)
        if match_factor > verbose_factor_threshold:
            color = '\033[92m'
        else:
            color = '\033[91m'
        print(
            f"{test.file_path}: {color}{round(match_factor*100, 3)}% \033[0m match")
        if match_factor < verbose_factor_threshold:
            print("\tMismatches:")
            no_too_short_mismatches = 0
            for mismatch in mismatches:
                if mismatch.duration > verbose_duration_threshold:
                    print(f"\t\t{mismatch}\n")
                else:
                    no_too_short_mismatches += 1
            print(
                f"\tRejected {no_too_short_mismatches} mismatches shorter than {verbose_duration_threshold}")
