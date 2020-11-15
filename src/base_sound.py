from utils import constants


class BaseSound:
    def __init__(self, note=None, symbol=None):
        self.note = note
        if symbol is not None:
            self.note = constants.REVERSE_SYMBOLS[symbol]

    @property
    def symbol(self):
        if self.note is None:
            return 'r'

        return constants.SYMBOLS[self.note]

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, note):
        self._note = note % 12 if note else note

    def __str__(self):
        return self.symbol

    __repr__ = __str__

    def __eq__(self, other):
        return self.note == other.note
