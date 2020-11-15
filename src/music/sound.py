from utils import constants
from . import base_sound


class Sound(base_sound.BaseSound):
    def __init__(self, note=None, timestamp=None, duration_ms=None,
                 rhytmic_value=None, symbol=None):
        super().__init__(note, symbol)
        self.timestamp = timestamp
        self.duration_ms = duration_ms
        self.rhytmic_value = rhytmic_value

    @property
    def end_timestamp(self):
        return self.timestamp + self.duration_ms

    @property
    def rhytmic_value_time(self):
        return constants.RHYTHMIC_VALUE_TO_TIME[self.rhytmic_value]

    def __str__(self):
        if self.timestamp is None:
            return super().__str__()
        return f"{round(self.timestamp, 3)}: {self.symbol}"

    __repr__ = __str__
