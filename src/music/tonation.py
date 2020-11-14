from . import chord
import copy


class Tonation(chord.Chord):
    def __init__(self, note=None, timestamp=None, duration_ms=None, symbol=None,
                 kind=None):
        super().__init__(note, timestamp, duration_ms, symbol, kind)
        self.tonic = chord.Chord(note, timestamp, duration_ms, symbol, kind)
        self.dominant = copy.deepcopy(self.tonic)
        self.dominant.note += 7
        self.dominant.kind = "major7"
        self.subdominant = copy.deepcopy(self.tonic)
        self.subdominant.note += 5

    def __str__(self):
        return f"{self.symbol}-{self.kind}"
