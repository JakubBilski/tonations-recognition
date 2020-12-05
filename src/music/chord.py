from . import base_sound


class Chord(base_sound.BaseSound):
    """A set of notes, not necessarily played together

    Attributes:
        kind (str) : "minor", "major" or other chord
            type from the music theory
        duration (int) : rhytmic value of the chord
            (if all the notes are played together)
            expressed in numbers of equivalent 32th notes
        all atributes of the base class (BaseSound)
    """
    def __init__(self, note=None, symbol=None, duration=None,
                 kind=None):
        super().__init__(note, symbol)
        if kind is not None:
            self.kind = kind
        if duration is not None:
            self.duration = duration

    def parallel(self):
        """
        Returns:
        (Chord) : chord consisting of the same set of notes,
            but of an opposite kind ("minor" when "major"
            and "major" when "minor")
        """
        if "major" in self.kind:
            return Chord(self.note+9, duration=self.duration,
                         kind=self.kind.replace("major", "minor"))
        else:
            return Chord(self.note+3, duration=self.duration,
                         kind=self.kind.replace("minor", "major"))

    def sounds(self):
        """
        Returns:
        (list[Sound]) : list of Sounds the chord comprises
        """
        if self.kind == "major":
            return [base_sound.BaseSound(self.note),
                    base_sound.BaseSound(self.note+4),
                    base_sound.BaseSound(self.note+7)]
        elif self.kind == "minor":
            return [base_sound.BaseSound(self.note),
                    base_sound.BaseSound(self.note+3),
                    base_sound.BaseSound(self.note+7)]
        elif self.kind == "major7":
            return [base_sound.BaseSound(self.note),
                    base_sound.BaseSound(self.note+4),
                    base_sound.BaseSound(self.note+7),
                    base_sound.BaseSound(self.note+10)]
        elif self.kind == "diminished":
            return [base_sound.BaseSound(self.note),
                    base_sound.BaseSound(self.note+3),
                    base_sound.BaseSound(self.note+6)]
        else:
            raise Exception("Not supported chord kind")

    def __str__(self):
        sounds = ', '.join(map(str, self.sounds()))
        return f"{self.symbol}-{self.kind} [{sounds}]"

    __repr__ = __str__

    def __eq__(self, other):
        return (self.note == other.note) and (self.kind == other.kind)

    @base_sound.BaseSound.duration.setter
    def duration(self, duration):
        if isinstance(duration, float):
            raise Exception("Tried to set duration to float")
        self._duration = duration
