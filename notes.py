

class Note:
    def __init__(self, note, time):
        self._note = note
        self.time = time

    @property
    def note(self):
        '''
        1 -> 'C'
        2 -> 'D'
        '''
        pass


class Notes:
    def __init__(self, file):
        pass

    def __str__(self):
        '''
        some graphic representation
        '''
        pass

    def get_notes(self):
        '''
        [Note('C', 100), Note('D', 300), Note(None, 100), Note('C', 100)]
        '''
        pass
