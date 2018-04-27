from .constants import VALIDNOTENAMESNOACCIDENTALS, VALIDNOTEDURATIONS, SHARP, FLAT, LYSHARP, LYFLAT
from .lysrc import Pitch

ACCIDENTALS = {SHARP : LYSHARP,
               FLAT : LYFLAT,
               LYSHARP : LYSHARP,
               LYFLAT : LYFLAT}

previous_pitch = None
'''
notes:
currently, a duration must be specified (unlike in lilypond, where a note automatically
takes the duration of it's predecessor

attributes:
pitch:      an integer describing the distance, in semitones, of the note from the c below middle C (unmodified c in lilypond 
            absolute mode, tenor c, or c-3)
duration:   an integer describing the duration of the note, the same way as in lilypond. longas and breves are -1 and -2 respectivly
accidental: Whether the note is sharp or flat. Will be constants.LYSHARP or constants.LYFLAT

'''
class lyNote(object):
    def __init__(self, string):
        self.note = string[0]
        if len(string) == 2:
            self.duration = string[1]
        if SHARP in string or LYSHARP in string:
            self.accidental = LYSHARP
        elif FLAT in string or LYFLAT in string:
            self.accidental = LYFLAT
        if "'" in string:
            self.octave = "'" * string.count("'")
        elif ',' in string:
            self.octave = ',' * string.count(',')
        else:
            self.octave = ''



    @classmethod
    def fromparts(cls, name, accidental, octave, length):
        cls(name+ACCIDENTALS[accidental]+octave+length)
        # self._name = name
        # self._accidental = accidental
        # self._length = length
        # self._octave = octave


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value not in VALIDNOTENAMESNOACCIDENTALS:
            raise ValueError('%s is not a valid note name')
        self._name = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if value not in VALIDNOTEDURATIONS:
            raise ValueError('%s is not a valid not duration' % value)
        self._duration = value

    @property
    def octave(self):
        return self._octave

    @octave.setter
    def octave(self, value):
        if not (len(value) == 0 or value == len(value) * "'" or value == len(value) * ","):
            raise ValueError('%s is not a valid octave' % value)
        self._octave = value

    @property
    def accidental(self):
        return self._accidental

    @accidental.setter
    def accidental(self, value):
        if value not in (LYFLAT, LYSHARP):
            raise ValueError('%s is not a valid accidental' % value)
        self._accidental = value


'''
From LilyPond 2.18.2 source code
lilypond.org
'''
class Pitch:
    def __init__ (self):
        self.alteration = 0
        self.step = 0
        self.octave = 0
        self._force_absolute_pitch = False

    def __repr__(self):
        return self.ly_expression()

    def transposed (self, interval):
        c = self.copy ()
        c.alteration  += interval.alteration
        c.step += interval.step
        c.octave += interval.octave
        c.normalize ()

        target_st = self.semitones()  + interval.semitones()
        c.alteration += target_st - c.semitones()
        return c

    def normalize (c):
        while c.step < 0:
            c.step += 7
            c.octave -= 1
        c.octave += c.step / 7
        c.step = c.step  % 7

    def lisp_expression (self):
        return '(ly:make-pitch %d %d %d)' % (self.octave,
                                             self.step,
                                             self.alteration)

    def copy (self):
        p = Pitch ()
        p.alteration = self.alteration
        p.step = self.step
        p.octave = self.octave
        return p

    def steps (self):
        return self.step + self.octave*7

    def semitones (self):
        return self.octave * 12 + [0,2,4,5,7,9,11][self.step] + self.alteration

    def ly_step_expression (self):
        return pitch_generating_function (self)

    def absolute_pitch (self):
        if self.octave >= 0:
            return "'" * (self.octave + 1)
        elif self.octave < -1:
            return "," * (-self.octave - 1)
        else:
            return ''

    def relative_pitch (self):
        global previous_pitch
        if not previous_pitch:
            previous_pitch = self
            return self.absolute_pitch ()
        previous_pitch_steps = previous_pitch.octave * 7 + previous_pitch.step
        this_pitch_steps = self.octave * 7 + self.step
        pitch_diff = (this_pitch_steps - previous_pitch_steps)
        previous_pitch = self
        if pitch_diff > 3:
            return "'" * ((pitch_diff + 3) // 7)
        elif pitch_diff < -3:
            return "," * ((-pitch_diff + 3) // 7)
        else:
            return ""

    def ly_expression (self, relative_pitches=True):
        string = self.ly_step_expression()
        if relative_pitches and not self._force_absolute_pitch:
            string += self.relative_pitch()
        else:
            string += self.absolute_pitch()

        return string

    def print_ly (self, outputter):
        outputter (self.ly_expression())