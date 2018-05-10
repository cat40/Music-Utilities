import librosa


class Note(object):
    def __init__(self, freq, start, end, volume, perc=False):
        if not perc:
            self.name = librosa.core.hz_to_note(freq)
            self.freq = freq
        self.start = start
        self.end = end
        self.duration = abs(end-start)
        self.volume = volume
        self.isPercussion = perc

    # can also use __cmp__ (returns - if less than, + if greater than, 0 if equal
    def __lt__(self, other):
        return self.freq < other.freq

    def __le__(self, other):
        return self.freq <= other.freq

    def __eq__(self, other):
        return self.freq == other.freq and self.duration == other.duration

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.freq > self.other

    def __ge__(self, other):
        return self.freq >= self.other

    def __str__(self):
        return str(self.name) + ' ' + str(self.duration)

    def __repr__(self):
        return ' '.join(map(str, (self.freq, self.name, self.duration)))

    '''
    parameters:
    tempo can be a number or a tuple (bpm, note_base) where note_base is the note that gets the beat
    If tempo is a single number, quarter note base will be assumed
    TODO: add support for dotted notes
    this might end up as a class method of Duration in lyutils later
    '''
    def toInt(self, tempo):
        # convert an integer tempo to a tuple tempo (assumes quarter note base
        if isinstance(tempo, (float, int)):
            tempo = tempo, 4
        secondsPerBeat = 60/tempo[0]
        numBeats = self.duration / secondsPerBeat
        return int((1/numBeats) * tempo[1])
