import parselmouth

import sys
import math
import os


def frequency_to_note(frequency):
    '''
    A4 440 Hz
    '''
    if frequency == 0:
        return None
    return round(12*math.log2(frequency/440.0)+45) % 12


def note_to_symbol(note):
    if note == None:
        return 'None'
    symbols = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'H']
    return symbols[note]


class NotesInTime:
    def __init__(self, file):
        snd = parselmouth.Sound(file)
        pitch = snd.to_pitch()
        frequencies = pitch.selected_array['frequency']
        notes = [frequency_to_note(freq) for freq in frequencies]
        self.notesInTime = []
        lastNote = None
        for note, time in zip(notes, pitch.xs()):
            if lastNote != note:
                self.notesInTime.append((note, time))
                lastNote = note

    def __str__(self):
        output = "0.000: None\n"
        for note, time in self.notesInTime:
            output += "{t}: {s}\n".format(t=round(time, 3),
                                          s=note_to_symbol(note))
        return output


if __name__ == "__main__":
    dirPath = sys.argv[1]

    files = [
        dirPath + fileName for fileName in os.listdir(dirPath) if fileName.endswith(".mp3") or fileName.endswith(".wav")]
    for file in files:
        print(file)
        notes = NotesInTime(file)
        print(notes)
