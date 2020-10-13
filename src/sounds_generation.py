import math

import parselmouth

import music


def frequency_to_note(frequency):
    '''
    A4 440 Hz
    '''
    if frequency == 0:
        return None
    return round(12*math.log2(frequency/440.0)+45) % 12


def note_to_frequency(note):
    if note is None:
        return 0
    return pow(2, (note-9.0)/12.0)*440.0


def get_sounds_from_file(file):
    snd = parselmouth.Sound(str(file))
    pitch = snd.to_pitch()
    frequencies = pitch.selected_array['frequency']
    notes = [frequency_to_note(freq) for freq in frequencies]
    return get_sounds_from_list(pitch.xs(), notes)


def get_sounds_from_list(timestamps, notes):
    # for each timeframe recognise note and
    # merge same notes together
    sounds = []
    last_note = None
    last_note_timestamp = 0.0
    for note, timestamp in zip(notes, timestamps):
        if last_note != note:
            sounds.append(music.Sound(last_note, last_note_timestamp,
                                      timestamp-last_note_timestamp))
            last_note = note
            last_note_timestamp = timestamp
    end_time = timestamps[-1]
    sounds.append(music.Sound(last_note, last_note_timestamp,
                              end_time-last_note_timestamp))

    # remove badly recognised notes (too short)
    sounds_corrected = []
    for s in sounds:
        if s.duration > 0.1:
            sounds_corrected.append(s)
        elif any(sounds_corrected):
            sounds_corrected[-1].duration += s.duration
            
    return sounds_corrected
