from os import O_TRUNC
import parselmouth
import math


class Sound:
    def __init__(self, note, timestamp=0, duration=0):
        self.note = note
        self.timestamp = timestamp
        self.duration = duration

    @property
    def symbol(self):
        if self.note == None:
            return 'None'
        #           0    1     2    3     4
        symbols = ['C', 'C#', 'D', 'D#', 'E',
                   # 5   6     7    8     9    10    11
                   'F', 'F#', 'G', 'G#', 'A', 'A#', 'H']
        return symbols[self.note]

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, note):
        self._note = note % 12 if note else note

    def __str__(self):
        return f"{self.timestamp}: {self.symbol}"

    def __eq__(self, other):
        return self.note == other.note

    __repr__ = __str__


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
            return Chord(self.note+9, self.timestamp, self.duration, self.type.replace("dur", "mol"))
        else:
            return Chord(self.note+3, self.timestamp, self.duration, self.type.replace("mol", "dur"))

    def sounds(self):
        if self.type == "dur":
            return [Sound(self.note), Sound(self.note+4), Sound(self.note+7)]
        elif self.type == "mol":
            return [Sound(self.note), Sound(self.note+3), Sound(self.note+7)]
        elif self.type == "dur7":
            return [Sound(self.note), Sound(self.note+4), Sound(self.note+7), Sound(self.note+10)]
        else:
            raise Exception("Not supported chord type")

    def __str__(self):
        sounds = ', '.join(map(str, self.sounds()))
        return f"{self.symbol}-{self.type} [{sounds}]"

    __repr__ = __str__

    def __eq__(self, other):
        return (self.note == other.note) and (self.type == other.type)
