from math import log2


# is added to all dotted notes scores in recognition process,
# so when it is not clear which duration the note should have,
# the algorithm will weight towards not-dotted notes
DOTTED_NOTES_DISCRIMINATOR = 0.0  # 0.0 - no discrimination, 1.0 - no dotted notes


def transform_beat_fractions_into_rhythmic_values(beat_fractions, meter):
    beat_frac_to_rhythmic_value = {
        8.0: "1.",
        6.0: "1.",
        4.0: "1",
        3.0: "2.",
        2.0: "2",
        1.5: "4.",
        1.0: "4",
        0.75: "8.",
        0.5: "8",
        0.375: "16.",
        0.25: "16",
        0.1875: "32.",
        0.125: "32"
    }
    result = []
    for beat_fraction in beat_fractions:
        if beat_fraction not in beat_frac_to_rhythmic_value.keys():
            if beat_fraction > min(beat_frac_to_rhythmic_value.keys()):
                result.append("1.")
            else:
                result.append("64")
        else:
            result.append(beat_frac_to_rhythmic_value[beat_fraction])
    return result


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


def update_sounds_with_rhythmic_values_compare_adjacent(sounds, meter):
    start_index = min(range(len(sounds)), key=[abs(
        s.duration_ms-meter) for s in sounds].__getitem__)
    if sounds[start_index].duration_ms/meter > 1.5 or sounds[start_index].duration_ms/meter < 0.75:
        raise(
            "There was no note with duration similar to the beat and the algorithm failed")
    beat_fractions = [0.0 for _ in sounds]
    beat_fractions[start_index] = 1.0
    allowed_fractions = [16.0, 12.0, 8.0, 6.0,
                         4.0, 3.0, 2.0, 1.5,
                         1.0, 0.75, 0.5, 0.375, 0.25,
                         0.1875, 0.125,
                         0.09375, 0.0625]
    allowed_fractions_log = [log2(ar) for ar in allowed_fractions]
    for i in range(start_index+1, len(sounds)):
        best_match_index = find_best_fraction_index(
            sounds[i], sounds[i-1], beat_fractions[i-1], allowed_fractions_log)
        beat_fractions[i] = allowed_fractions[best_match_index]
    for i in range(start_index-1, -1, -1):
        best_match_index = find_best_fraction_index(
            sounds[i], sounds[i+1], allowed_fractions_log)
        beat_fractions[i] = allowed_fractions[best_match_index]
    rhythmic_values = transform_beat_fractions_into_rhythmic_values(
        beat_fractions, meter)
    for sound, rhythmic_value in zip(sounds, rhythmic_values):
        sound.rhythmic_value = rhythmic_value
