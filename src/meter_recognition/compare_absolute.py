from math import log2
from utils import constants

# is added to all dotted notes scores in recognition process,
# so when it is not clear which duration the note should have,
# the algorithm will weight towards not-dotted notes
DOTTED_NOTES_DISCRIMINATOR = 0.0  # 0.0 - no discrimination, 1.0 - no dotted notes

def update_sounds_with_rhythmic_values_compare_absolute(sounds, meter):
    beat_duration = 8
    allowed_fractions = [float(d)/beat_duration for d in constants.LEGAL_DURATION_VALUES]
    allowed_fractions_log = [log2(ar) for ar in allowed_fractions]
    beat_fractions = []
    for i in range(0, len(sounds)):
        relation = sounds[i].duration_ms / meter
        relation_log = log2(relation)
        minimized_values = [abs(arl-relation_log)
                            for arl in allowed_fractions_log]
        for dotted_note_index in range(1, len(minimized_values), 2):
            minimized_values[dotted_note_index] += DOTTED_NOTES_DISCRIMINATOR
        best_match_index = min(range(len(allowed_fractions_log)),
                               key=minimized_values.__getitem__)
        beat_fractions.append(allowed_fractions[best_match_index])
    sound_durations = [round(bf*beat_duration) for bf in beat_fractions]
    for sound, sound_duration in zip(sounds, sound_durations):
        sound.duration = sound_duration
