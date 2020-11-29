from . import base_sound


class Sound(base_sound.BaseSound):
    def __init__(self, note=None, timestamp=None, duration_ms=None,
                 duration=None, symbol=None):
        super().__init__(note, symbol)
        if timestamp is not None:
            self.timestamp = timestamp
        if duration_ms is not None:
            self.duration_ms = duration_ms
        if duration is not None:
            self.duration = duration

    @property
    def end_timestamp(self):
        return self.timestamp + self.duration_ms

    def __str__(self):
        if self.duration is not None:
            return f"{self.symbol}\t({self.duration})"
        if self.timestamp is not None:
            return f"{round(self.timestamp, 3)}: {self.symbol}"
        return super().__str__()

    __repr__ = __str__
