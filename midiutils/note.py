import mido

class Note(object):
    def __init__(self, note, start, end):
        self.note = note
        self.start = start
        self.end = end

    def message(self):
        return (mido.Message('note_on', note=self.note, time=self.start), mido.Message('note_off', note=self.note, time=self.end))
