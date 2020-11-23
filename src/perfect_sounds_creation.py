from music import Sound

def get_perfect_sounds(sounds, beat_duration, beat_duration_ms):
    perfect_sounds = []
    current_end_timestamp = 0.0
    for sound in sounds:
        sound_perfect_duration_ms = sounds.duration * beat_duration_ms / beat_duration
        perfect_sounds.append(Sound(sound.note, current_end_timestamp, sound_perfect_duration_ms))
        current_end_timestamp += sound_perfect_duration_ms
    return perfect_sounds
