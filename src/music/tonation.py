from . import chord
import copy


class Tonation(chord.Chord):
    def __init__(self, note, timestamp, duration, kind):
        super().__init__(note, timestamp, duration, kind)
        self.tonic = chord.Chord(note, timestamp, duration, kind)
        self.dominant = copy.deepcopy(self.tonic)
        self.dominant.note += 7
        self.dominant.kind = "major7"
        self.subdominant = copy.deepcopy(self.tonic)
        self.subdominant.note += 5

    def __str__(self):
        return f"{self.symbol}-{self.kind}"

    def __eq__(self, other):
        return self.symbol == other.symbol and self.kind == other.kind