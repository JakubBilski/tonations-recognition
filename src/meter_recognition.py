import librosa
from math import log2

from music import Sound

DOTTED_NOTES_DISCRIMINATOR = 0.0 #0.0 - no discrimination, 1.0 - no dotted notes (not linear!)
RECOGNITION_METHOD = "compare_adjacent"
# RECOGNITION_METHOD = "compare_absolute"

def get_meter(file_path, sounds):
    y, sr = librosa.load(file_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
    return 60.0/tempo, beats

def find_best_fraction_index(sound1, sound2, allowed_fractions_log):
    local_beat = sound2.duration / sound2.beat_fraction
    relation = sound1.duration / local_beat
    relation_log = log2(relation)
    minimized_values = [abs(arl-relation_log) for arl in allowed_fractions_log]
    # print(minimized_values)
    for dotted_note_index in range(1, len(minimized_values), 2):
        minimized_values[dotted_note_index] += DOTTED_NOTES_DISCRIMINATOR
    return min(range(len(allowed_fractions_log)),
                            key=minimized_values.__getitem__)

def update_sounds_with_beat_fractions_compare_adjacent(sounds, meter):
    start_index = min(range(len(sounds)), key=[abs(s.duration-meter) for s in sounds].__getitem__)
    if sounds[start_index].duration/meter > 1.5 or sounds[start_index].duration/meter < 0.75:
        raise("Wow, there was no note with duration similar to the beat")
    sounds[start_index].beat_fraction = 1.0
    allowed_fractions = [16.0, 12.0, 8.0, 6.0, 4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 0.375, 0.25, 0.1875, 0.125, 0.09375, 0.0625]
    allowed_fractions_log = [log2(ar) for ar in allowed_fractions]
    for i in range(start_index+1, len(sounds)):
        best_match_index = find_best_fraction_index(sounds[i], sounds[i-1], allowed_fractions_log)
        sounds[i].beat_fraction = allowed_fractions[best_match_index]
    for i in range(start_index-1, -1, -1):
        best_match_index = find_best_fraction_index(sounds[i], sounds[i+1], allowed_fractions_log)
        sounds[i].beat_fraction = allowed_fractions[best_match_index]
    return transform_beat_fractions_into_duration_signatures(sounds, meter)

def update_sounds_with_beat_fractions_compare_absolute(sounds, meter):
    allowed_fractions = [16.0, 12.0, 8.0, 6.0, 4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 0.375, 0.25, 0.1875, 0.125, 0.09375, 0.0625]
    allowed_fractions_log = [log2(ar) for ar in allowed_fractions]
    for i in range(0, len(sounds)):
        relation = sounds[i].duration / meter
        relation_log = log2(relation)
        minimized_values = [abs(arl-relation_log) for arl in allowed_fractions_log]
        for dotted_note_index in range(1, len(minimized_values), 2):
            minimized_values[dotted_note_index] += DOTTED_NOTES_DISCRIMINATOR
        best_match_index =  min(range(len(allowed_fractions_log)),
                                key=minimized_values.__getitem__)
        sounds[i].beat_fraction = allowed_fractions[best_match_index]
    return transform_beat_fractions_into_duration_signatures(sounds, meter)

def transform_beat_fractions_into_duration_signatures(sounds, meter):

    multiplier = 1.0
    # if abs(meter-0.5108390022675736)<0.0001:
    #     multiplier = 2.0
    # if (abs(meter-0.4411791383219954)<0.0001):
    #     multiplier = 0.5
    beat_frac_to_duration_sign = {
        8.0 : "1.",
        6.0 : "1.",
        4.0 : "1",
        3.0 : "2.",
        2.0 : "2",
        1.5 : "4.",
        1.0 : "4",
        0.75 : "8.",
        0.5 : "8",
        0.375 : "16.",
        0.25 : "16",
        0.1875 : "32.",
        0.125 : "32"
    } 
    for sound in sounds:
        if multiplier*sound.beat_fraction not in beat_frac_to_duration_sign.keys():
            if multiplier*sound.beat_fraction > min(beat_frac_to_duration_sign.keys()):
                sound.duration_signature = "1."
            else:
                sound.duration_signature = "64"
        else:
            sound.duration_signature = beat_frac_to_duration_sign[multiplier*sound.beat_fraction]

def update_sounds1(meter, beats, sounds):
    if RECOGNITION_METHOD == "compare_adjacent":
        update_sounds_with_beat_fractions_compare_adjacent(sounds, meter)
    elif RECOGNITION_METHOD == "compare_absolute":
        update_sounds_with_beat_fractions_compare_absolute(sounds, meter)
    elif  RECOGNITION_METHOD == "brojaczj_algorithm":
        update_sounds_brojaczj_algorithm(meter, beats, sounds)
    transform_beat_fractions_into_duration_signatures(sounds, meter)
    return sounds


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
    sixteenth = (b2-b1)/4
    return round(sound.duration/sixteenth)
    # if abs(sound.timestamp-b1) < 0.05:
    #     # super


def tim_to_duration(tim):
    result = []
    for num in [32, 16, 8, 4, 2, 1]:
        if tim >= num:
            result.append(16//num)
            tim -= num

    # result1 = []
    # for i in range(len(result)-1):
    #     result1.append(str(result[i])+'~')
    # result1.append(result[-1])
    return result


# def symbol_to_lilypond(symbol):
#     s = symbol.lower().replace("#", "is")


def update_sounds_brojaczj_algorithm(tempo, beats, sounds):
    beats = list(beats)
    while beats[0] > 0:
        beats.insert(0, beats[0]-tempo)
    while beats[-1] < sounds[-1].timestamp+sounds[-1].duration:
        beats.append(beats[-1]+tempo)

    dur = {}
    for s in sounds:
        id = f'{s.duration:.3f}'
        dur[id] = dur.get(id, 0) + 1

    for i in range(len(sounds)):
        sounds[i].beat_id = beat_id_closest_to_timestamp(
            beats, sounds[i].timestamp)

    sounds1 = []
    print()
    print('Sounds with beats:')
    for s in sounds:
        duration = tim_to_duration(simple_sound_beat_dur(beats, s))
        if (len(duration) >= 3) and \
            (duration[1] == duration[0]*2) and \
                (duration[2] == duration[1]*2):
            sounds1.append(Sound(
                note=s.note,
                duration_signature=str(duration[0]//2)+'.'
            ))
        elif (len(duration) >= 2) and (duration[1] == duration[0]*2):
            sounds1.append(Sound(
                note=s.note,
                duration_signature=str(duration[0])+'.'
            ))
        else:
            sounds1.append(Sound(
                note=s.note,
                duration_signature=str(duration[0])
            ))

    return sounds1
