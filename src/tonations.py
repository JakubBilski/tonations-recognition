from . import chord
from . import base_sound


class Tonation(base_sound.BaseSound):
    def __init__(self, note=None, symbol=None,
                 kind=None):
        super().__init__(note, symbol)
        self.kind = kind
        self.tonic = chord.Chord(self.note, kind=kind)
        self.dominant = chord.Chord(self.note+7, kind="major7")
        self.subdominant = chord.Chord(self.note+5, kind=kind)

    def __str__(self):
        return f"{self.symbol}-{self.kind}"
