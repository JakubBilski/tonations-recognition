from librosa import util
from utils import constants


def beat_id_closest_to_timestamp(beats, timestamp):
    clos = 1000
    res = -1
    for i in range(len(beats)):
        if abs(beats[i]-timestamp) < clos:
            clos = abs(beats[i]-timestamp)
            res = i

    return res


def simple_sound_beat_dur(beats, sound):
    id = sound.beat_id
    b1 = beats[id]
    b2 = beats[id+1]
    local_duration_of_16s = (b2-b1)/4
    # TODO check changing to 32 in some situations?
    no_16s_in_note = round(sound.duration_ms/local_duration_of_16s)

    # Build result note from higher level notes (max one of each type)
    result_note = []
    for num in [32, 16, 8, 4, 2, 1]:
        if no_16s_in_note >= num:
            result_note.append(16//num)
            no_16s_in_note -= num
    return result_note


def no_32nd(sound):
    # number of equivalent 32nd notes
    return int(sound.rhythmic_value_time /
               constants.RHYTHMIC_VALUE_TO_TIME["32"])


def update_sounds_with_rhythmic_values_fit_to_bar(tempo, beats, sounds):
    # lets assume it is 4/4 meter
    # and that min note is thirty two

    beats = list(beats)
    while beats[0] > 0:
        beats.insert(0, beats[0]-tempo)
    while beats[-1] < sounds[-1].end_timestamp:
        beats.append(beats[-1]+tempo)

    for i in range(len(sounds)):
        sounds[i].beat_id = beat_id_closest_to_timestamp(
            beats, sounds[i].timestamp)

    for s in sounds:
        duration = simple_sound_beat_dur(beats, s)
        if (len(duration) >= 3) and \
            (duration[1] == duration[0]*2) and \
                (duration[2] == duration[1]*2):
            s.rhythmic_value = str(duration[0]//2)

        elif (len(duration) >= 2) and (duration[1] == duration[0]*2):
            s.rhythmic_value = str(duration[0])+'.'
        else:
            s.rhythmic_value = str(duration[0])

    bar = 4*8  # number of 32s in bar
    act_bar = 0
    bar_start = 0
    i = -1
    while i < len(sounds) - 1:
        i += 1
        s = sounds[i]
        act_bar += no_32nd(s)
        if act_bar == bar:
            # super
            bar_start = i+1
            act_bar = 0
        if act_bar < bar:
            # ok
            continue
        # act_bar > bar
        # bad
        diff = act_bar - bar
        if diff > 4:
            # too big mistake
            # it can propagate forward, so dont even try
            break
        # go through all notes in bar
        j = bar_start-1
        while j < i:
            j += 1
            s = sounds[j]
            if s.note is None and no_32nd(s) <= diff:
                diff -= no_32nd(s)
                sounds.pop(j)
                i -= 1
                j -= 1
            if s.rhythmic_value.endswith('.') and no_32nd(s) / 3 <= diff:
                diff -= int(no_32nd(s) / 3)
                s.rhythmic_value = s.rhythmic_value[:-1]

    # fix when part of note is silent sometimes
    i = -1
    while i < len(sounds) - 2:
        i += 1
        s0 = sounds[i]
        s1 = sounds[i+1]
        if (s1.note is None) and \
            s0.rhythmic_value.endswith('.') and \
           (no_32nd(s1)*3 <= no_32nd(s0)):
            s0.rhythmic_value = str(int(s0.rhythmic_value[:-1])//2)
            sounds.pop(i+1)
            i -= 1

