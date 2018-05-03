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
class Note(object):
    def __init__(self, pitches, duration, useRelative=True):
        self.pitches = pitches if isinstance(pitches, list) else list(pitches)
        if isinstance(duration, Duration):
            self.duration = duration
        else:
            self.duration = Duration(duration)
        self.useRelative = useRelative

    def __str__(self):
        if len(self.pitches) > 1:
            string = '<' + ' '.join(map(str, self.pitches)) + '>'
        else:
            string = str(self.pitches)
        return string + str(self.duration)


'''
These are just wrapper classes for the lilypond source classes to make them a bit easier to work with
Arguments have been explained as I understand them, not nessesarily as implemented in the lilypond source code
'''

class Pitch(lysrc.Pitch):
    def __init__(self, octave, step, alteration):
        super().__init__()
        self.step = step  # step above c in the octave, where c = 0, d = 1, a=5, b=6, etc
        self.octave = octave  # the octave of the note, where c3 is 0 and middle c is 1
        self.alteration = alteration  # number of semitones above or below the step, I think
                                         # (1=sharp, 2=doublesharp, -1=flat, -2=double flat

    def __str__(self):
        return repr(self)  # todo this might need to be super instead of self, see how it works


class Duration(lysrc.Duration):
    def __init__(self, duration_log, dots, factor=None):
        super().__init__()
        self.duration_log = duration_log  # The duration as a log base 2 (quarter note = 2, whole note = 0, etc)
        self.dots = dots  # number of dots
        if factor is not None:
            self.factor = factor  # todo: figure out what this does

    def __str__(self):
        return repr(self)
