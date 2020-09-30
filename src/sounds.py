import parselmouth

import argparse
import pathlib
import math
import os

class Sound:
    def __init__(self, note, timestamp, duration):
        self.note = note
        self.timestamp = timestamp
        self.duration = duration

    @property
    def symbol(self):
        if self.note == None:
            return 'None'
        symbols = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'H']
        return symbols[self.note]  

    def __str__(self):
        return f"{round(self.timestamp, 3)}: {self.symbol}\n"

    def __eq__(self, other):
        return self.note == other.note

def frequency_to_note(frequency):
    '''
    A4 440 Hz
    '''
    if frequency == 0:
        return None
    return round(12*math.log2(frequency/440.0)+45) % 12


class Sounds:
    def __init__(self, file):
        self._sounds = []
        snd = parselmouth.Sound(file)
        pitch = snd.to_pitch()
        self._get_sounds_from_pitch(pitch)

    def __str__(self):
        output = ""
        for sound in self._sounds:
            output += str(sound)
        return output

    def _get_sounds_from_pitch(self, pitch):
        self._sounds = []
        frequencies = pitch.selected_array['frequency']
        notes = [frequency_to_note(freq) for freq in frequencies]
        lastNote = None
        lastNoteTimestamp = 0.0
        for note, timestamp in zip(notes, pitch.xs()):
            if lastNote != note:
                self._sounds.append(Sound(lastNote, lastNoteTimestamp, timestamp-lastNoteTimestamp))
                lastNote = note
                lastNoteTimestamp = timestamp
        endTime = pitch.xs()[len(pitch.xs())-1]
        self._sounds.append(Sound(lastNote, lastNoteTimestamp, endTime-lastNoteTimestamp))

def parse_args():
    parser = argparse.ArgumentParser(
        description='Tonations Recognition: ...')
    parser.add_argument('--input', '-I',
                        required=True,
                        help='...',
                        type=pathlib.Path)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    dirPath = str(parse_args().input)
    files = [
        os.path.join(dirPath, fileName) for fileName in os.listdir(dirPath) if fileName.endswith(".mp3") or fileName.endswith(".wav")]
    for file in files:
        print(file)
        sounds = Sounds(file)
        print(sounds)
