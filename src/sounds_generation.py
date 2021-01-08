import math

import parselmouth

from . import music


STRENGTH_CHANGE_TO_SEPARATE = 2


def frequency_to_note(frequency):
    '''
    A4 440 Hz
    '''
    if frequency == 0:
        return None
    return round(12*math.log2(frequency/440.0)+45)


def get_sounds_from_file(file):
    """Use audio file to generate Sounds

    Parameters:
    file (str) : Path to the audio file

    Returns:
    (list[Sound]) : List of generated Sounds
    """
    snd = parselmouth.Sound(str(file))
    pitch = snd.to_pitch()
    frequencies = pitch.selected_array['frequency']
    stgt = pitch.selected_array['strength']
    xs = pitch.xs()
    strength_changes = \
        [(stgt[i]-stgt[i-1] > (xs[i]-xs[i-1])*STRENGTH_CHANGE_TO_SEPARATE)
         for i in range(1, len(stgt))]
    strength_changes.insert(0, False)
    notes = [frequency_to_note(freq) for freq in frequencies]
    return get_sounds_from_list(xs, strength_changes, notes)


def get_sounds_from_list(timestamps, stength_changes, notes):
    # for each timeframe recognise note and
    # merge same more notes together
    sounds = []
    last_note = None
    last_note_timestamp = 0.0
    for note, timestamp, a_changes \
            in zip(notes, timestamps, stength_changes):
        if (last_note != note) or a_changes:
            sounds.append(music.Sound(last_note, last_note_timestamp,
                                      timestamp-last_note_timestamp))
            last_note = note
            last_note_timestamp = timestamp
    end_time = timestamps[-1]
    sounds.append(music.Sound(last_note, last_note_timestamp,
                              end_time-last_note_timestamp))

    if sounds[0].note is None:
        sounds = sounds[1:]
    if sounds[-1].note is None:
        sounds = sounds[:-1]

    # remove badly recognised notes (too short)
    sounds_corrected = []
    for s in sounds:
        if s.duration_ms > 0.2 or \
                (s.duration_ms > 0.1 and s.note is not None):
            sounds_corrected.append(s)
        elif any(sounds_corrected):
            sounds_corrected[-1].duration_ms += s.duration_ms

    return sounds_corrected
