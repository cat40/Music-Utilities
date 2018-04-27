from .lyObjs import Clef
from . import lysrc
from .note import lyNote
# These might end up in constants later
BASS = Clef('bass')
ALTO = Clef('alto')
TREBLE = Clef('treble')

# expand this later, for now it's just string instruments
clefs = {'bass' : BASS,
         'violincello' : BASS,
         'viola' : ALTO,
         'violin' : TREBLE}

''' 
A class for putting instruments into lilypond
    TODO: add support for multi-staff insturments, like piano
    TODO: add midi stuff
    TODO: modify lysrc Pitch to better impliment previous pitch being stored in the insturment
'''
class Instrument(object):
    def __init__(self, name, clef=None, useGlobal=True, useRelative=True, relative="'"):
        if name == 'cello':
            name = 'violincello'
        self.name = name
        if clef is None:
            clef = clefs[name]
        self.clef = clef
        self.useGlobal = useGlobal
        self.useRelative = useRelative  # wheter or not to include a \relative before the braces
        self.relative = relative        # note the music is relative to. can be a note, or just , and '
        self.sequence = []              # list of notes, lyObjs, and everything else in between the \relative{} braces
        #self.PreviousPitch = None

    def __str__(self):
        lysrc.PreviousPitch = None
        lysrc.relative_pitches = self.useRelative # might want to consider setting this back to its previous value after being done with it
        string = '%s = ' % self.name
        if self.useRelative:
            string += '\\relative '
            string += self.relative if any(s in self.relative for s in 'abcdefg') else 'c'+self.relative # checks if self.relative is a whole note or just a pitch, and adds c if the later
            string += ' '
        string += '{\n'
        for thing in self.sequence:
            if len(string.split('\n')[-1]) > 80:
                string += '\n'
            string += str(thing) + ' '
        string += '}'
        return string


