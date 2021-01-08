from ..utils import constants


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

    if id==len(beats)-1:
        b2 = beats[id]
        b1 = beats[id-1]
    else:
        b1 = beats[id]
        b2 = beats[id+1]
    local_duration_of_16s = (b2-b1)/4
    no_16s_in_sound = round(sound.duration_ms/local_duration_of_16s)

    # Build result note from higher level notes (max one of each type)
    duration_components = []
    for num in [32, 16, 8, 4, 2, 1]:
        if no_16s_in_sound >= num:
            duration_components.append(num*2)
            no_16s_in_sound -= num
    return duration_components


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
        duration_components = simple_sound_beat_dur(beats, s)
        if (len(duration_components) >= 3) and \
            (duration_components[0] == duration_components[1]*2) and \
                (duration_components[1] == duration_components[2]*2):
            s.duration = duration_components[0]*2
        elif (len(duration_components) >= 2) and \
                (duration_components[0] == duration_components[1]*2):
            s.duration = duration_components[0] + duration_components[0]//2
        else:
            s.duration = duration_components[0]

    bar = 4*8  # number of 32s in bar
    act_bar = 0
    bar_start = 0
    i = -1
    while i < len(sounds) - 1:
        i += 1
        s = sounds[i]
        act_bar += s.duration
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
            if s.note is None and s.duration <= diff:
                diff -= s.duration
                sounds.pop(j)
                i -= 1
                j -= 1
            if s.duration in constants.LEGAL_DOTTED_DURATION_VALUES and \
                    s.duration // 3 <= diff:
                diff -= s.duration // 3
                s.duration = (s.duration // 3) * 2

    # fix when part of note is silent sometimes
    i = -1
    while i < len(sounds) - 2:
        i += 1
        s0 = sounds[i]
        s1 = sounds[i+1]
        if (s1.note is None) and \
            s0.duration in constants.LEGAL_DOTTED_DURATION_VALUES and \
           (s1.duration*3 <= s0.duration):
            s0.duration = (s0.duration//3)*4
            sounds.pop(i+1)
            i -= 1
