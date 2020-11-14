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
    return int((s1.note != s2.note) or (s1.duration_signature != s2.duration_signature))


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
                (d[i-1][j-1][0] + substitution(test_sounds[j-1], sounds[i-1]), 0),
                key=lambda val: val[0]
            )

    return 1-d[-1][-1][0]/len(test_sounds), d


def visualize_d(d, sounds, test_sounds):
    result = []
    m = len(sounds)
    n = len(test_sounds)
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
            r0 = f"{str(r[0].symbol).ljust(5)} {r[0].duration_signature.ljust(3)}"
        if r[1] is None:
            r1 = ""
        else:
            r1 = f"{str(r[1].symbol).ljust(5)} {r[1].duration_signature.ljust(3)}"
        
        if (r[2] != 0) or substitution(r[0], r[1]) != 0:
            color = bcolors.FAIL
        else:
            color = bcolors.OKGREEN
        print(f"{color}{r0.ljust(8)}\t{r1.ljust(8)}{bcolors.ENDC}")


def move_sounds(sounds, coef):
    sound1 = []
    for s in sounds:
        ds = s.duration_signature
        d = False
        if ds.endswith('.'):
            d = True
            ds = ds[:-1]
        try:
            ds = str(int(int(ds)*coef))
        except Exception:
            ds = ""
        if d:
            ds = f"{ds}."
        sound1.append(
            music.Sound(note=s.note, duration_signature=ds)
        )
    return sound1


def main(args, rec_meth):
    tests = test_data.get_all_test_models()

    print("-----------SOUNDS TEST-----------------")
    print(f"Testing beat recognition {rec_meth}")
    match_factor_sum = 0
    for test in tests:
        sounds = sounds_generation.get_sounds_from_file(test.file_path)
        meter, beats = meter_recognition.get_meter(test.file_path, sounds)
        if rec_meth == "compare_adjacent":
            meter_recognition.update_sounds_with_beat_fractions_compare_adjacent(sounds, meter)
        elif rec_meth == "compare_absolute":
            meter_recognition.update_sounds_with_beat_fractions_compare_absolute(sounds, meter)
        elif  rec_meth == "brojaczj_algorithm":
            meter_recognition.update_sounds_brojaczj_algorithm(meter, beats, sounds)
        match_factor = -1000
        d_list = None
        test_sounds = None
        for i in [4, 2, 1, 1/2, 1/4]:
            test_sounds_1 = move_sounds(test.sounds, i)
            match_factor_1, d_list_1 = match_sounds(sounds, test_sounds_1)
            if match_factor_1 > match_factor:
                match_factor = match_factor_1
                d_list = d_list_1
                test_sounds = test_sounds_1

        # match_factor, d_list = match_sounds(sounds, test.sounds)

        print(
            f"{test.file_path}: {round(match_factor*100, 3)}")
        match_factor_sum += match_factor
        visualize_d(d_list, sounds, test_sounds)
    print(f"Average match factor for beat recognition {rec_meth}: {match_factor_sum/len(tests)}")

if __name__ == "__main__":
    args = parse_args()
    rec_meths = []
    rec_meths.append("compare_absolute")
    # rec_meths.append("compare_adjacent")
    rec_meths.append("brojaczj_algorithm")
    for rec_meth in rec_meths:
        main(args, rec_meth)