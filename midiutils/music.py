class Music(object):
    def __init__(self):
        pass

    def messages(self):
        for note in self.notes:
            start, end = note.message
