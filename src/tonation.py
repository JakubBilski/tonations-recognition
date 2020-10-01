import chords
import copy


class Tonation(chords.Chord):
    def __init__(self, note, timestamp, duration, type):
        super().__init__(note, timestamp, duration, type)
        self.tonic = chords.Chord(note, timestamp, duration, type)
        self.dominant = copy.deepcopy(self.tonic)
        self.dominant.note += 7
        self.dominant.type = "dur"
        self.subdominant = copy.deepcopy(self.tonic)
        self.subdominant.note += 5

    def __str__(self):
        return f"{round(self.timestamp, 3)}: {self.symbol}-{self.type}\n"\
            f"tonic: {self.tonic.symbol}-{self.tonic.type}\n"\
            f"dominant: {self.dominant.symbol}-{self.dominant.type}\n"\
            f"subdominant: {self.subdominant.symbol}-{self.subdominant.type}"




class Tonations(chords.Chord):
    def __init__(self, *args):
        pass

    def __str__(self):
        '''
        some graphic representation
        '''
        pass

    def get_tonations(self):
        '''
        [Note('C', 100), Note('D', 300), Note(None, 100), Note('C', 100)]
        '''
        pass
