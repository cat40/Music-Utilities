from .lyObjs import Clef
# These might end up in constants later
BASS = Clef('bass')
ALTO = Clef('alto')
TREBLE = Clef('treble')

# expand this later, for now it's just string instruments
clefs = {'bass' : BASS,
         'violincello' : BASS,
         'viola' : ALTO,
         'violin' : TREBLE}


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
        self.notes = []                 # list of just the notes (might not be nessesary)
        self.sequence = []              # list of notes, lyObjs, and everything else in between the \relative{} braces

    def __str__(self):
        string = '%s = ' % self.name
        if self.useRelative:
            string += '\\relative '
            string += self.relative if any(s in self.relative for s in 'abcdefg') else 'c'+self.relative
        string += '{\n'
        for thing in self.sequence:
            string += str(thing)
        string += '}'

