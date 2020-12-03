from utils import constants


class BaseSound:
    """Base class containing basic sound infromation

    Attributes:
        note (int) : note as number of halftones
            from the nearest C, going down
            (zero for C)
    """
    def __init__(self, note=None, symbol=None):
        self.note = note
        if symbol is not None:
            self.note = constants.REVERSE_SYMBOLS[symbol]

    @property
    def symbol(self):
        """Returns:
        (string) : representation of the note
            in "C", "C#", "D", ... convention
        """
        if self.note is None:
            return 'r'

        return constants.SYMBOLS[self.note]

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, note):
        self._note = note % 12 if note else note

    @property
    def duration(self):
        """(int) : Rhytmic value of the sound
            expressed in numbers of equivalent 32th notes
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        if duration not in constants.LEGAL_DURATION_VALUES:
            raise Exception(
                f"Tried to set duration to an illegal value: {duration}")
        if isinstance(duration, float):
            raise Exception("Tried to set duration to float")
        self._duration = duration

    def __str__(self):
        return self.symbol

    __repr__ = __str__

    def __eq__(self, other):
        return self.note == other.note
