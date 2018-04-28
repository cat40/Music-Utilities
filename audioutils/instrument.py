import math

from .. import lyutils
# presets:

'''
:parameter
:param
'''
class Instrument(object):
    def __init__(self, minnote=None, maxnote=None, name=None, preset=None, notes: list=None):
        if preset is not None:
            pass # todo: impliment getting stuff from the presets
        elif not(minnote is not None and maxnote is not None and name is not None):
            raise ValueError('Not all parameters were specified')
        self.minnote = minnote
        self.maxnote = maxnote
        self.name = name
        self.notes = [] if notes is None else notes

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name not in lyutils.MIDINAMES:
            raise ValueError('%s is not a valid lilypond midi name' % name) # todo: find a better way of validating name without lyutils
        self._name = name

    '''
    converts to an lyutils instrument object
    Base is a tuple (note duration (fraction), note duration (seconds))
    For example, for a 1 second eigth note, this would be (8, 1)
    support for notes longer than a whole note is not present yet
    '''
    def convert(self, base: tuple):
        newnotes = []
        wholenote = base[1] * base[0]  # duration of a whole note
        for note in self.notes:
            duration = self.tonearest(note.duration/wholenote)
            pitch = self.name

    @staticmethod
    # finds the nearest power of 2 to the number i
    def tonearest(i):
        return 2**(round(math.log(i, 2), 0))
