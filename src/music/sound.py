class Sound:
    def __init__(self, note, timestamp=None, duration=None, beat_fraction=None):
        self.note = note
        self.timestamp = timestamp
        self.duration = duration
        self.beat_fraction = beat_fraction

    @property
    def symbol(self):
        if self.note is None:
            return 'None'
        symbols = ['C', 'C#', 'D', 'D#', 'E',
                   'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return symbols[self.note]

    @property
    def note(self):
        return self._note
    
    @property
    def end_timestamp(self):
        return self.timestamp + self.duration

    @note.setter
    def note(self, note):
        self._note = note % 12 if note else note

    def __str__(self):
        if self.timestamp is None:
            return self.symbol
        return f"{round(self.timestamp, 3)}: {self.symbol}"

    __repr__ = __str__

    def __eq__(self, other):
        return self.note == other.note
