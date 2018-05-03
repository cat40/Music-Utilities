from .lyObjs import Clef
from . import lysrc
from . import constants
import roman_numerals

# These might end up in constants later
BASS = Clef('bass')
ALTO = Clef('alto')
TREBLE = Clef('treble')

index = 0  # consider making a dictionary for each instrument (make sure to include an other category
# could also define it dynamically so that the dictionary only includes names that have been used

# expand this later, for now it's just string instruments
clefs = {'bass' : BASS,
         'cello' : BASS,
         'viola' : ALTO,
         'violin' : TREBLE}

''' 
A class for putting instruments into lilypond
    TODO: add support for multi-staff insturments, like piano
    TODO: add midi stuff
    TODO: modify lysrc Pitch to better impliment previous pitch being stored in the insturment
    The parameter name must be a valid midi name
'''
class Instrument(object):
    def __init__(self, name, sequence, paramindex=None, midiname=None, clef=None, useGlobal=True, useRelative=True, relative="'"):
        global index
        if name == 'violincello':
            name = 'cello'
        if name not in constants.MIDINAMES:
            raise ValueError('%s is not a valid instrument name (only lilypond midi names are accepted' % name)
        if midiname is None:
            self.midiname = name
        else:
            self.midiname = midiname
        self.insName = name
        self.index = index
        if clef is None:
            clef = clefs[name]
        self.clef = clef
        self.useGlobal = useGlobal
        self.useRelative = useRelative  # wheter or not to include a \relative before the braces
        self.relative = relative        # note the music is relative to. can be a note, or just , and '
        self.sequence = sequence        # list of notes, lyObjs, and everything else in between the \relative{} braces
        index += 1 # might want to do this conditionally on the index being unspecified
        if paramindex is None: self.index = index
        # self.PreviousPitch = None

    @classmethod
    def from_raw_notes(cls, notes, relative):
        pass # todo put stuff from audioutils.convert in here, also solves import problem in audioutils importhing this

    def __str__(self):
        relative = self.relative if any(s in self.relative for s in 'abcdefg') else 'c' + self.relative
        # relPitch = lysrc.Pitch() # todo: un hardcode this (right now it's always relative to c4
        # relPitch.step=0
        # relPitch.octave=1
        # relPitch.alteration=0
        # lysrc.PreviousPitch = relPitch
        lysrc.relative_pitches = self.useRelative # might want to consider setting this back to its previous value after being done with it
        string = '%s = ' % self.name
        if self.useRelative:
            string += '\\relative '
            string += relative # checks if self.relative is a whole note or just a pitch, and adds c if the later
            string += ' '
        string += '{\n'
        for thing in self.sequence:
            if len(string.split('\n')[-1]) > 80:
                string += '\n'
            string += str(thing) + ' '
        string += '}'
        return string

    def staffblock(self):
        string = self.name + 'Part' + ' = \\new Staff \\with {\n'
        string += 'InstrumentName = ' + self.displayname + '\n'
        string += 'midiInstrument = ' + self.midiname + '\n'
        string += '}' + '\\' + self.name
        return string

    @property
    def name(self):
        return self.insName + str(self.index)

    @property
    def displayname(self):
        return self.insName + str(self.index) if self.index else self.insName # roman_numerals.convert_to_numeral(self.index+1) if self.index else self.insName
