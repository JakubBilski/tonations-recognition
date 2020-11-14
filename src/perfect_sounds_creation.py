from music import Sound

def get_perfect_sounds(sounds, beat):
    update_beat_fractions_from_rhytmic_values(sounds)
    perfect_sounds = []
    current_end_timestamp = 0.0
    for sound in sounds:
        perfect_sounds.append(Sound(sound.note, current_end_timestamp, sound.beat_fraction*beat))
        current_end_timestamp += sound.beat_fraction*beat
    return perfect_sounds

def update_beat_fractions_from_rhytmic_values(sounds):
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
    reverse_dict = {}
    for key in beat_frac_to_rhytmic_value.keys():
        reverse_dict[beat_frac_to_rhytmic_value[key]] = key
    for sound in sounds:
        sound.beat_fraction = reverse_dict[sound.rhytmic_value]
