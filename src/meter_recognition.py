import librosa
from math import log2


# is added to all dotted notes scores in recognition process,
# so when it is not clear which duration the note should have,
# the algorithm will weight towards not-dotted notes
DOTTED_NOTES_DISCRIMINATOR = 0.0 #0.0 - no discrimination, 1.0 - no dotted notes

def get_meter(file_path, sounds):
    y, sr = librosa.load(file_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
    return 60.0/tempo, beats

def find_best_fraction_index(sound1, sound2, prev_beat_fraction, allowed_fractions_log):
    local_beat = sound2.duration_ms / prev_beat_fraction
    relation = sound1.duration_ms / local_beat
    relation_log = log2(relation)
    minimized_values = [abs(arl-relation_log) for arl in allowed_fractions_log]
    # print(minimized_values)
    for dotted_note_index in range(1, len(minimized_values), 2):
        minimized_values[dotted_note_index] += DOTTED_NOTES_DISCRIMINATOR
    return min(range(len(allowed_fractions_log)),
                            key=minimized_values.__getitem__)


def transform_beat_fractions_into_rhytmic_values(beat_fractions, meter):
    beat_frac_to_rhytmic_value = {
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
    result = []
    for beat_fraction in beat_fractions:
        if beat_fraction not in beat_frac_to_rhytmic_value.keys():
            if beat_fraction > min(beat_frac_to_rhytmic_value.keys()):
                result.append("1.")
            else:
                result.append("64")
        else:
            result.append(beat_frac_to_rhytmic_value[beat_fraction])
    return result


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
    return round(sound.duration_ms/sixteenth)


def tim_to_duration(tim):
    result = []
    for num in [32, 16, 8, 4, 2, 1]:
        if tim >= num:
            result.append(16//num)
            tim -= num
    return result


def update_sounds_with_rhytmic_values_brojaczj_algorithm(tempo, beats, sounds):
    beats = list(beats)
    while beats[0] > 0:
        beats.insert(0, beats[0]-tempo)
    while beats[-1] < sounds[-1].timestamp+sounds[-1].duration_ms:
        beats.append(beats[-1]+tempo)

    dur = {}
    for s in sounds:
        id = f'{s.duration_ms:.3f}'
        dur[id] = dur.get(id, 0) + 1

    for i in range(len(sounds)):
        sounds[i].beat_id = beat_id_closest_to_timestamp(
            beats, sounds[i].timestamp)
            
    for s in sounds:
        duration = tim_to_duration(simple_sound_beat_dur(beats, s))
        if (len(duration) >= 3) and \
            (duration[1] == duration[0]*2) and \
                (duration[2] == duration[1]*2):
                    s.rhytmic_value=str(duration[0]//2)+'.'
            
        elif (len(duration) >= 2) and (duration[1] == duration[0]*2):
            s.rhytmic_value=str(duration[0])+'.'
        else:
            s.rhytmic_value=str(duration[0])


def update_sounds_with_rhytmic_values_compare_adjacent(sounds, meter):
    start_index = min(range(len(sounds)), key=[abs(s.duration_ms-meter) for s in sounds].__getitem__)
    if sounds[start_index].duration_ms/meter > 1.5 or sounds[start_index].duration_ms/meter < 0.75:
        raise("There was no note with duration similar to the beat and the algorithm failed")
    beat_fractions = [0.0 for _ in sounds]
    beat_fractions[start_index] = 1.0
    allowed_fractions = [16.0, 12.0, 8.0, 6.0, 4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 0.375, 0.25, 0.1875, 0.125, 0.09375, 0.0625]
    allowed_fractions_log = [log2(ar) for ar in allowed_fractions]
    for i in range(start_index+1, len(sounds)):
        best_match_index = find_best_fraction_index(sounds[i], sounds[i-1], beat_fractions[i-1], allowed_fractions_log)
        beat_fractions[i] = allowed_fractions[best_match_index]
    for i in range(start_index-1, -1, -1):
        best_match_index = find_best_fraction_index(sounds[i], sounds[i+1], allowed_fractions_log)
        beat_fractions[i] = allowed_fractions[best_match_index]
    rhytmic_values = transform_beat_fractions_into_rhytmic_values(beat_fractions, meter)
    for sound, rhytmic_value in zip(sounds, rhytmic_values):
        sound.rhytmic_value = rhytmic_value


def update_sounds_with_rhytmic_values_compare_absolute(sounds, meter):
    allowed_fractions = [16.0, 12.0, 8.0, 6.0, 4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 0.375, 0.25, 0.1875, 0.125, 0.09375, 0.0625]
    allowed_fractions_log = [log2(ar) for ar in allowed_fractions]
    beat_fractions = []
    for i in range(0, len(sounds)):
        relation = sounds[i].duration_ms / meter
        relation_log = log2(relation)
        minimized_values = [abs(arl-relation_log) for arl in allowed_fractions_log]
        for dotted_note_index in range(1, len(minimized_values), 2):
            minimized_values[dotted_note_index] += DOTTED_NOTES_DISCRIMINATOR
        best_match_index =  min(range(len(allowed_fractions_log)),
                                key=minimized_values.__getitem__)
        beat_fractions.append(allowed_fractions[best_match_index])
    rhytmic_values = transform_beat_fractions_into_rhytmic_values(beat_fractions, meter)
    for sound, rhytmic_value in zip(sounds, rhytmic_values):
        sound.rhytmic_value = rhytmic_value