from os import O_TRUNC
import parselmouth

import argparse
import pathlib
import math


class Sound:
    def __init__(self, note, timestamp, duration):
        self.note = note%12
        self.timestamp = timestamp
        self.duration = duration

    @property
    def symbol(self):
        if self.note == None:
            return 'None'
        #           0    1     2    3     4    5    6     7    8     9    10    11
        symbols = ['C', 'C#', 'D', 'D#', 'E',
                   'F', 'F#', 'G', 'G#', 'A', 'A#', 'H']
        return symbols[self.note]

    def __str__(self):
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


class Sounds:
    def __init__(self):
        self.sounds = []
        self._get_sounds_from_pitch()

    def __str__(self):
        return "".join([str(sound) for sound in self.sounds])

    def _get_sounds_from_pitch(self):
        pitch = [1, 2, 3, 4, 5, 6, 6.5, 7, 9,
                 10, 11, 12, 13, 14, 15, 15.5, 16, 18]
        notes = [7, 4, 4, 5, 2, 2, 0, 4, 7, 7, 4, 4, 5, 2, 2, 0, 4, 0]
        lastNote = None
        lastNoteTimestamp = 0.0
        for note, timestamp in zip(notes, pitch):
            if lastNote != note:
                self.sounds.append(
                    Sound(lastNote, lastNoteTimestamp, timestamp-lastNoteTimestamp))
                lastNote = note
                lastNoteTimestamp = timestamp
        endTime = pitch[-1]
        self.sounds.append(
            Sound(lastNote, lastNoteTimestamp, endTime-lastNoteTimestamp))


class Chord(Sound):
    def __init__(self, note, timestamp, duration, type):
        super().__init__(note, timestamp, duration)
        self.type = type

    def parallel(self):
        if "dur" in self.type:
            return Chord(self.note+9, self.timestamp, self.duration, self.type.replace("dur","mol"))
        else:
            return Chord(self.note+3, self.timestamp, self.duration, self.type.replace("mol","dur"))

    def sounds(self):
        if self.type == "dur":
            return [self.note, (self.note+4)%12, (self.note+7)%12]
        elif self.type == "mol":
            return [self.note, (self.note+3)%12, (self.note+7)%12]
        else:
            raise Exception("Not supported chord type")

    def __str__(self):
        return f"{round(self.timestamp, 3)}: {self.symbol}-{self.type}\n"

    def __eq__(self, other):
        return (self.note == other.note) and (self.type == other.type)


class Chords:
    def __init__(self, sounds, tonation, metrum):
        self.chords = []
        self.sounds = sounds
        self.tonation = tonation
        self.metrum = metrum
        self._get_chords()

    def __str__(self):
        return "".join([str(chord) for chord in self.chords])

    def get_sounds_at_metrum(self, sounds: list(Sound)):
        s = []
        last_sound = sounds[0]
        last_metrum = -self.metrum
        for sound in sounds:
            while sound.timestamp >= last_metrum+self.metrum:
                s.append(sound)
                last_metrum += self.metrum
            last_sound = sound
        return s

    def _get_chords(self):
        sounds_at_metrum = self.get_sounds_at_metrum(self.sounds.sounds)


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
    s = Sounds()
    print(s.sounds)
