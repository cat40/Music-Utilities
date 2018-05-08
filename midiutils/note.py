import mido

class Note(object):
    def __init__(self, note, start, end):
        self.note = int(note)
        self.start = start
        self.end = end

    def message(self, resolution, tempo):
        start = int(mido.second2tick(self.start, resolution, tempo))
        end = int(mido.second2tick(self.end, resolution, tempo))
        print(start, end, self.start-self.end)
        return (mido.Message('note_on', note=self.note, time=start),
                mido.Message('note_off', note=self.note, time=end))
