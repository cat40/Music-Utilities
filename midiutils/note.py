import mido

class Note(object):
    def __init__(self, note, start, end):
        self.note = int(note)
        self.start = start
        self.end = end

    def message(self, resolution, tempo):
        return (mido.Message('note_on', note=self.note, time=int(mido.second2tick(self.start, resolution, tempo))),
                mido.Message('note_off', note=self.note, time=int(mido.second2tick(self.end, resolution, tempo))))
