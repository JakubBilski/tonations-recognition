from . import chord
from . import base_sound


class Tonation(base_sound.BaseSound):
    """A sound of one pitch present in a music piece

    Attributes:
        kind (str) : "minor" or "major"
        tonic (Chord) : Set of sounds composing the
            tonic of this key expressed in a form of Chord
        subdominant (Chord) : Set of sounds composing the
            subdominant of this key expressed in a form of Chord
        dominant (Chord) : Set of sounds composing the
            dominant of this key expressed in a form of Chord
        all atributes of the base class (BaseSound)
    """
    def __init__(self, note=None, symbol=None,
                 kind=None):
        super().__init__(note, symbol)
        self.kind = kind
        self.tonic = chord.Chord(self.note, kind=kind)
        self.dominant = chord.Chord(self.note+7, kind="major7")
        self.subdominant = chord.Chord(self.note+5, kind=kind)

    def __str__(self):
        return f"{self.symbol}-{self.kind}"
