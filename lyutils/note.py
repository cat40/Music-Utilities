from .constants import VALIDNOTEDURATIONS, STRNOTEDURATIONS
from . import lysrc


'''notes:
currently, a duration must be specified (unlike in lilypond, where a note automatically
takes the duration of it's predecessor

attributes:
pitch:      an integer describing the distance, in semitones, of the note from the c below middle C (unmodified c in lilypond 
            absolute mode, tenor c, or c-3)
duration:   an integer describing the duration of the note, the same way as in lilypond. longas and breves are -1 and -2 respectivly
accidental: Whether the note is sharp or flat. Will be constants.LYSHARP or constants.LYFLAT

'''
class lyNote(object):
    def __init__(self, dur, useRelative=True):
        self.pitches = []
        if isinstance(dur, Duration):
            self.duration = dur
        else:
            self.duration = Duration(dur)
        self.useRelative = useRelative

    def __str__(self):
        if len(self.pitches) > 1:
            string = '<' + ' '.join(self.pitches) + '>'
        else:
            string = str(self.pitches)
        return string + str(self.duration)


class Duration(object):  # a class to hold duration, and convert the weird ones like breve and longa to ints
    def __init__(self, duration):
        if duration not in VALIDNOTEDURATIONS:
            raise ValueError('%s is not a valid not duration' % duration)
        self.duration = duration

    def __int__(self):
        if self.duration in STRNOTEDURATIONS:
            return STRNOTEDURATIONS[self.duration]
        else:
            return int(self.duration)

    def __str__(self):
        return self.duration


class Pitch(lysrc.Pitch):
    def __str__(self):
        return repr(self)
