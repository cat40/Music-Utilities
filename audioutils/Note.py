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
        return self.name + ' ' + self.duration

    def __repr__(self):
        return ' '.join((self.freq, self.name, self.duration))
