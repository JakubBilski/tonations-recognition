import librosa
from math import log2

from music import sound

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
    transform_beat_fractions_into_duration_signatures(sounds, meter)
    return sounds