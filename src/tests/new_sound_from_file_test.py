import path_magic  # noqa

import argparse

import test_data
import music
import sounds_generation
import meter_recognition


def parse_args():
    parser = argparse.ArgumentParser(
        description='Test convering audio files to notes with time of occurrence')
    args = parser.parse_args()
    return args


def substitution(s1: music.Sound, s2: music.Sound):
    return int((s1.note != s2.note) or (s1.beat_fraction != s2.beat_fraction))


def deletion(s: music.Sound):
    return 1


def insertion(s: music.Sound):
    return 1


def match_sounds(sounds, test_sounds):
    m = len(sounds)+1
    n = len(test_sounds)+1
    d = [[0 for _ in range(n)]
         for _ in range(m)]

    for i in range(m):
        d[i][0] = i
    for j in range(n):
        d[0][j] = j

    for i in range(1, m):
        for j in range(1, n):
            d[i][j] = min(
                d[i-1][j] + deletion(test_sounds[i-1]),
                d[i][j-1] + insertion(sounds[j-1]),
                d[i-1][j-1] + substitution(sounds[j-1, test_sounds[i-1]])
            )

    return d[-1][-1]


def main(args):
    tests = test_data.get_all_test_models()

    print("-----------SOUNDS TEST-----------------")
    for test in tests:
        sounds = sounds_generation.get_sounds_from_file(test.file_path)
        meter, beats = meter_recognition.get_meter(args.input, sounds)
        sounds = meter_recognition.update_sounds(meter, beats, sounds)
        match_factor = match_sounds(sounds, test.sounds)

        print(
            f"{test.file_path}: {round(match_factor*100, 3)}")


if __name__ == "__main__":
    args = parse_args()
    main(args)
