import parselmouth

import argparse
import pathlib
import math


class Sound:
    def __init__(self, note, timestamp=None, duration=None):
        self.note = note
        self.timestamp = timestamp
        self.duration = duration

    @property
    def symbol(self):
        if self.note == None:
            return 'None'
        symbols = ['C', 'C#', 'D', 'D#', 'E',
                   'F', 'F#', 'G', 'G#', 'A', 'A#', 'H']
        return symbols[self.note]

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, note):
        self._note = note % 12 if note else note

    def __str__(self):
        if self.timestamp is None:
            return self.symbol
        return f"{round(self.timestamp, 3)}: {self.symbol}"

    def __eq__(self, other):
        return self.note == other.note


def frequency_to_note(frequency):
    '''
    A4 440 Hz
    '''
    if frequency == 0:
        return None
    return round(12*math.log2(frequency/440.0)+45) % 12


def get_sounds_from_file(file):
    sounds = []
    snd = parselmouth.Sound(str(file))
    pitch = snd.to_pitch()
    frequencies = pitch.selected_array['frequency']
    notes = [frequency_to_note(freq) for freq in frequencies]
    last_note = None
    last_note_timestamp = 0.0
    for note, timestamp in zip(notes, pitch.xs()):
        if last_note != note:
            sounds.append(Sound(last_note, last_note_timestamp,
                                timestamp-last_note_timestamp))
            last_note = note
            last_note_timestamp = timestamp
    end_time = pitch.xs()[-1]
    sounds.append(Sound(last_note, last_note_timestamp,
                        end_time-last_note_timestamp))
    return sounds


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert auio file to notes with time of occurrence')
    parser.add_argument('--input', '-I',
                        required=True,
                        help='Audio file. Formats: [.mp3, .wav]',
                        type=pathlib.Path)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    dir_path = parse_args().input
    files = [
        file_name for file_name in dir_path.iterdir() if file_name.suffix in [".mp3", ".wav"]]
    for file in files:
        print(file)
        sounds = get_sounds_from_file(file)
        print("\n".join([str(sound) for sound in sounds]))
