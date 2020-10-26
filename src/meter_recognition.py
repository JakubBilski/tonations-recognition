import librosa
from math import log2

from music import sound

DOTTED_NOTES_DISCRIMINATOR = 0.2 #0.0 - no discrimination, 1.0 - no dotted notes (not linear!)

def get_beat_from_file(file_path):
    y, sr = librosa.load(file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr, units="time")
    return 60.0/tempo

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

def update_sounds_with_beat_fractions_compare_adjacent(sounds, beat):
    start_index = min(range(len(sounds)), key=[abs(s.duration-beat) for s in sounds].__getitem__)
    if sounds[start_index].duration/beat > 1.5 or sounds[start_index].duration/beat < 0.75:
        raise("Wow, there was no note with duration similar to the beat")
    sounds[start_index].beat_fraction = 1
    allowed_fractions = [16, 12, 8, 6, 4, 3, 2, 1.5, 1, 0.75, 0.5, 0.375, 0.25, 0.1875, 0.125, 0.09375, 0.0625]
    allowed_fractions_log = [log2(ar) for ar in allowed_fractions]
    for i in range(start_index+1, len(sounds)):
        best_match_index = find_best_fraction_index(sounds[i], sounds[i-1], allowed_fractions_log)
        sounds[i].beat_fraction = allowed_fractions[best_match_index]
    for i in range(start_index-1, -1, -1):
        best_match_index = find_best_fraction_index(sounds[i], sounds[i+1], allowed_fractions_log)
        sounds[i].beat_fraction = allowed_fractions[best_match_index]

def update_sounds_with_beat_fractions_compare_absolute(sounds, beat):
    allowed_fractions = [16, 12, 8, 6, 4, 3, 2, 1.5, 1, 0.75, 0.5, 0.375, 0.25, 0.1875, 0.125, 0.09375, 0.0625]
    allowed_fractions_log = [log2(ar) for ar in allowed_fractions]
    for i in range(0, len(sounds)):
        relation = sounds[i].duration / beat
        relation_log = log2(relation)
        minimized_values = [abs(arl-relation_log) for arl in allowed_fractions_log]
        for dotted_note_index in range(1, len(minimized_values), 2):
            minimized_values[dotted_note_index] += DOTTED_NOTES_DISCRIMINATOR
        best_match_index =  min(range(len(allowed_fractions_log)),
                                key=minimized_values.__getitem__)
        sounds[i].beat_fraction = allowed_fractions[best_match_index]