from . import sound


class Chord(sound.Sound):
    def __init__(self, note, timestamp, duration, type):
        super().__init__(note, timestamp, duration)
        self.type = type

    def parallel(self):
        if "dur" in self.type:
            return Chord(self.note+9, self.timestamp, self.duration, self.type.replace("dur", "mol"))
        else:
            return Chord(self.note+3, self.timestamp, self.duration, self.type.replace("mol", "dur"))

    def sounds(self):
        if self.type == "dur":
            return [sound.Sound(self.note), sound.Sound(self.note+4), sound.Sound(self.note+7)]
        elif self.type == "mol":
            return [sound.Sound(self.note), sound.Sound(self.note+3), sound.Sound(self.note+7)]
        elif self.type == "dur7":
            return [sound.Sound(self.note), sound.Sound(self.note+4), sound.Sound(self.note+7), sound.Sound(self.note+10)]
        else:
            raise Exception("Not supported chord type")

    def __str__(self):
        sounds = ', '.join(map(str, self.sounds()))
        return f"{self.symbol}-{self.type} [{sounds}]"

    __repr__ = __str__

    def __eq__(self, other):
        return (self.note == other.note) and (self.type == other.type)