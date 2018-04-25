from .constants import VALIDNOTENAMESNOACCIDENTALS, VALIDNOTEDURATIONS, SHARP, FLAT, LYSHARP, LYFLAT

ACCIDENTALS = {SHARP : LYSHARP,
               FLAT : LYFLAT,
               LYSHARP : LYSHARP,
               LYFLAT : LYFLAT}
'''
notes:
currently, a duration must be specified (unlike in lilypond, where a note automatically
takes the duration of it's predecessor
'''
class lyNote(object):
    def __init__(self, string):
        self.note = string[0]
        if


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
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if value not in VALIDNOTEDURATIONS:
            raise ValueError('%s is not a valid not duration' % value)
        self._length = value

    @property
    def octave(self):
        return self._octave

    @octave.setter
    def octave(self, value):
        if not (len(value) == 0 or value == len(value) * "'" or value == len(value) * ","):
            raise ValueError('%s is not a valid octave' % value)
        self._octave = value
