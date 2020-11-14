from . import sound


class Chord(sound.Sound):
    def __init__(self, note=None, timestamp=None, duration_ms=None, symbol=None,
                 kind=None):
        super().__init__(note, timestamp, duration_ms, None, symbol)
        self.kind = kind

    def parallel(self):
        if "major" in self.kind:
            return Chord(self.note+9, self.timestamp, self.duration_ms,
                         self.kind.replace("major", "minor"))
        else:
            return Chord(self.note+3, self.timestamp, self.duration_ms,
                         self.kind.replace("minor", "major"))

    def sounds(self):
        if self.kind == "major":
            return [sound.Sound(self.note), sound.Sound(self.note+4),
                    sound.Sound(self.note+7)]
        elif self.kind == "minor":
            return [sound.Sound(self.note), sound.Sound(self.note+3),
                    sound.Sound(self.note+7)]
        elif self.kind == "major7":
            return [sound.Sound(self.note), sound.Sound(self.note+4),
                    sound.Sound(self.note+7), sound.Sound(self.note+10)]
        else:
            raise Exception("Not supported chord kind")

    def __str__(self):
        sounds = ', '.join(map(str, self.sounds()))
        return f"{self.symbol}-{self.kind} [{sounds}]"

    __repr__ = __str__

    def __eq__(self, other):
        return (self.note == other.note) and (self.kind == other.kind)
