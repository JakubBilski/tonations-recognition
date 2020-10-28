import path_magic  # noqa

import argparse

import test_data
import bcolors

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
                (d[i-1][j] + deletion(sounds[i-1]), -1),
                (d[i][j-1] + insertion(test_sounds[j-1]), 1),
                (d[i-1][j-1] + substitution(test_sounds[j-1], sounds[i-1]), 0),
                key=lambda val: val[0]
            )

    return 1-d[-1][-1]/len(test_sounds), d


def visualize_d(d, sounds, test_sounds):
    result = []
    m = len(sounds)
    n = len(test_sounds)
    while (m > 0) and (n > 0):
        act_scoring = d[m][n]
        if act_scoring[1] == -1:
            result.append((sounds[-1], None), act_scoring[1])
            m -= 1
        elif act_scoring[1] == 1:
            result.append((None, test_sounds[-1]), act_scoring[1])
            n -= 1
        else:
            result.append((sounds[-1], test_sounds[-1]), act_scoring[1])
            m -= 1
            n -= 1
    for r in result:
        if r[0] is None:
            r0 = ""
        else:
            r0 = f"{str(r[0].symbol).ljust(5)} {r[0].beat_fraction.ljust(3)}"
        if r[1] is None:
            r1 = ""
        else:
            r1 = f"{str(r[1].symbol).ljust(5)} {r[1].beat_fraction.ljust(3)}"
        
        if (r[2] != 0) or substitution(r[0], r[1]) != 0:
            color = bcolors.FAIL
        else:
            color = bcolors.OKGREEN
        print(f"{color}{r0.ljust(8)}\t{r1.ljust(8)}{bcolors.ENDC}")


def main(args):
    tests = test_data.get_all_test_models()

    print("-----------SOUNDS TEST-----------------")
    for test in tests:
        sounds = sounds_generation.get_sounds_from_file(test.file_path)
        meter, beats = meter_recognition.get_meter(test.file_path, sounds)
        sounds = meter_recognition.update_sounds1(meter, beats, sounds)
        match_factor, d_list = match_sounds(sounds, test.sounds)

        print(
            f"{test.file_path}: {round(match_factor*100, 3)}")
        visualize_d(d_list, sounds, test.sounds)


if __name__ == "__main__":
    args = parse_args()
    main(args)
