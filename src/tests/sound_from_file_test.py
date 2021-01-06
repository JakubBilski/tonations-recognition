import argparse

from . import test_data
from . import bcolors

from .. import music
from .. import sounds_generation
from .. import meter_recognition
from ..utils import constants


def parse_args():
    parser = argparse.ArgumentParser(
        description='Test convering audio files to notes with '
        'time of occurrence')
    parser.add_argument('--verbose', '-V',
                        action="store_true",
                        help='Print detailed info about tests')
    args = parser.parse_args()
    return args


def substitution(s1: music.Sound, s2: music.Sound):
    return int((s1.note != s2.note) or (s1.duration != s2.duration))


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
        d[i][0] = (i, -1)
    for j in range(n):
        d[0][j] = (j, 1)

    for i in range(1, m):
        for j in range(1, n):
            d[i][j] = min(
                (d[i-1][j][0] + deletion(sounds[i-1]), -1),
                (d[i][j-1][0] + insertion(test_sounds[j-1]), 1),
                (d[i-1][j-1][0] +
                    substitution(test_sounds[j-1], sounds[i-1]), 0),
                key=lambda val: val[0]
            )

    return 1-d[-1][-1][0]/len(test_sounds), d


def visualize_d(d, sounds, test_sounds):
    result = []
    m = len(sounds)
    n = len(test_sounds)
    sounds = sounds
    test_sounds = test_sounds
    while (m > 0) or (n > 0):
        act_scoring = d[m][n]
        if act_scoring[1] == -1:
            m -= 1
            result.append((sounds[m], None, act_scoring[1]))
        elif act_scoring[1] == 1:
            n -= 1
            result.append((None, test_sounds[n], act_scoring[1]))
        else:
            m -= 1
            n -= 1
            result.append((sounds[m], test_sounds[n], act_scoring[1]))
    for r in result:
        if r[0] is None:
            r0 = ""
        else:
            r0 = f"{str(r[0].symbol).ljust(5)} {str(r[0].duration).ljust(3)}"
        if r[1] is None:
            r1 = ""
        else:
            r1 = f"{str(r[1].symbol).ljust(5)} {str(r[1].duration).ljust(3)}"

        if (r[2] != 0) or substitution(r[0], r[1]) != 0:
            color = bcolors.FAIL
        else:
            color = bcolors.OKGREEN
        print(f"{color}{r0.ljust(8)}\t{r1.ljust(8)}{bcolors.ENDC}")


def try_to_move_sounds(sounds, coef):
    sound1 = []
    for s in sounds:
        if int(s.duration*coef) not in constants.LEGAL_DURATION_VALUES:
            return None
        sound1.append(
            music.Sound(note=s.note, duration=int(s.duration*coef))
        )
    return sound1


def main(args, rec_meth):
    tests = test_data.get_perfect_test_models()

    print("-----------SOUNDS TEST-----------------")
    print(f"Testing beat recognition {rec_meth}")
    match_factor_sum = 0
    for test in tests:
        sounds = sounds_generation.get_sounds_from_file(test.file_path)
        meter, beats = meter_recognition.get_meter(test.file_path, sounds)
        if rec_meth == "fit_to_bar":
            meter_recognition.update_sounds_with_rhythmic_values_fit_to_bar(
                meter, beats, sounds
            )
        sounds = list(reversed(sounds))
        test.sounds = list(reversed(test.sounds))
        match_factor = -1000
        d_list = None
        test_sounds = None
        for i in [4, 2, 1, 1/2, 1/4]:
            test_sounds_1 = try_to_move_sounds(test.sounds, i)
            if test_sounds_1 is None:
                continue
            match_factor_1, d_list_1 = match_sounds(sounds, test_sounds_1)
            if match_factor_1 > match_factor:
                match_factor = match_factor_1
                d_list = d_list_1
                test_sounds = test_sounds_1

        print(
            f"{test.file_path}: {round(match_factor*100, 3)}")
        match_factor_sum += match_factor
        if args.verbose:
            visualize_d(d_list, sounds, test_sounds)
    print(
        f"Average match factor for beat recognition {rec_meth}: "
        f"{match_factor_sum/len(tests)}")


def run_tests():
    args = parse_args()
    rec_meths = []
    rec_meths.append("fit_to_bar")
    for rec_meth in rec_meths:
        main(args, rec_meth)
