SYMBOLS = ['C', 'C#', 'D', 'D#', 'E',
           'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
REVERSE_SYMBOLS = {
    s: i for i, s in enumerate(SYMBOLS)
}
REVERSE_SYMBOLS.update(
    {
        s.lower(): i for i, s in enumerate(SYMBOLS)
    }
)
REVERSE_SYMBOLS.update(
    {
        'cis': 1,
        'dis': 3,
        'fis': 6,
        'gis': 8,
        'ais': 10
    }
)


class Sound:
    def __init__(self, note=None, timestamp=None, duration=None,
                 duration_signature=None, symbol=None):
        self.note = note
        if symbol is not None:
            self.note = REVERSE_SYMBOLS[symbol]
        self.timestamp = timestamp
        self.duration = duration
        self.duration_signature = duration_signature
        self.beat_fraction = None

    @property
    def symbol(self):
        if self.note is None:
            return 'None'

        return SYMBOLS[self.note]

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

    def transform_beat_fraction_into_duration_signature(sounds, meter):
        beat_frac_to_duration_sign = {
            8.0 : "1.",
            6.0 : "1.",
            4.0 : "1",
            3.0 : "2.",
            2.0 : "2",
            1.5 : "4.",
            1.0 : "4",
            0.75 : "8.",
            0.5 : "8",
            0.375 : "16.",
            0.25 : "16",
            0.1875 : "32.",
            0.125 : "32"
        } 
        for sound in sounds:
            if sound.beat_fraction not in beat_frac_to_duration_sign.keys():
                if sound.beat_fraction > min(beat_frac_to_duration_sign.keys()):
                    sound.duration_signature = "1."
                else:
                    sound.duration_signature = "64"
            else:
                sound.duration_signature = beat_frac_to_duration_sign[sound.beat_fraction]
