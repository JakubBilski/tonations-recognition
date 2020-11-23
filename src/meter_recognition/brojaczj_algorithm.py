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
    b1 = beats[sound.beat_id]
    b2 = beats[sound.beat_id+1] 
    local_duration_of_32s = (b2-b1)/8
    no_32s_in_sound = round(sound.duration_ms/local_duration_of_32s)
    duration_components = []
    for num in reversed(constants.LEGAL_NOT_DOTTED_DURATION_VALUES):
        if no_32s_in_sound >= num:
            duration_components.append(num)
            no_32s_in_sound -= num
    return duration_components


def update_sounds_with_rhythmic_values_brojaczj_algorithm(tempo, beats, sounds):
    beats = list(beats)
    while beats[0] > 0:
        beats.insert(0, beats[0]-tempo)
    while beats[-1] < sounds[-1].timestamp+sounds[-1].duration_ms:
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
        elif (len(duration_components) >= 2) and (duration_components[0] == duration_components[1]*2):
            s.duration = duration_components[0]+duration_components[0]//2
        else:
            s.duration = duration_components[0]
