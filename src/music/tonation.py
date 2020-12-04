from . import chord
from . import base_sound


class Tonation(base_sound.BaseSound):
    """A sound of one pitch present in a music piece

    Attributes:
        kind (str) : "minor" or "major"
        all atributes of the base class (BaseSound)
    """
    def __init__(self, note=None, symbol=None,
                 kind=None):
        super().__init__(note, symbol)
        self.kind = kind

    def __str__(self):
        return f"{self.symbol}-{self.kind}"
