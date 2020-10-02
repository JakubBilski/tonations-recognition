import chords
import copy


class Tonation(chords.Chord):
    def __init__(self, note, timestamp, duration, type):
        super().__init__(note, timestamp, duration, type)
        self.tonic = chords.Chord(note, timestamp, duration, type)
        self.dominant = copy.deepcopy(self.tonic)
        self.dominant.note += 7
        self.dominant.type = "dur7"
        self.subdominant = copy.deepcopy(self.tonic)
        self.subdominant.note += 5

    def __str__(self):
        return f"Tonation {self.symbol}-{self.type}\n"\
            f"tonic: {self.tonic}\n"\
            f"dominant: {self.dominant}\n"\
            f"subdominant: {self.subdominant}"
