import collections
import math
from librosa import note_to_hz
from .. import lyutils

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
        self.minnote = minnote if isinstance(minnote, (int, float)) else note_to_hz(minnote)
        self.maxnote = maxnote if isinstance(maxnote, (int, float)) else note_to_hz(maxnote)
        self.name = name
        self.notes = [] if notes is None else notes

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name not in lyutils.MIDINAMES:
            raise ValueError('%s is not a valid lilypond midi name' % name)  # todo: find a better way of validating name without lyutils
        self._name = name

    '''
    converts to an lyutils instrument object
    Base is a tuple (note duration (fraction), note duration (seconds))
    For example, for a 1 second eigth note, this would be (8, 1)
    support for notes longer than a whole note is not present yet
    '''
    def convert(self, base):
        if isinstance(base, int):
            # might want to do this part before separating into instruments
            base = (base, sum(note.duration for note in self.notes) / len(self.notes))
        wholenote = base[0] * base[1]
        sequence = self.alignnotes(wholenote) # todo: determine time, tempo, and key changes and add to the sequence
        return lyutils.Instrument(self.name, sequence)



    '''
    aligns notes by onset and offest (to see which should be double stops
    will probably end up in instrument instead of here

    conditions:
    starts within tol of each other
    stops within tol of each other
    make : a dictionary
        keys are tuples (start, stop)
        values are a list of notes
    for each note, check all dictionary keys
        if none match, make a new key
    problems:
        if the first found note is on the edge and tolerance is too small to catch all other notes
        possibly somewhat mitigate by modifiying the dicionary key each time something is added to 
        average the values, but still won't help if the first note is on one end and the second is on the other
    a better way to do the dicionarys might be to use unique id's of lists as the keys, so that
    all values can be stored in the list and an average taken
    '''

    def alignnotes(self, wholenote, tol=.5):
        notesdict = {}
        newnotes = []
        for note in self.notes:
            for (start, end, i), notes in notesdict.items():
                if start - tol <= note.start <= start + tol and end - tol <= note.end <= end + tol:
                    notesdict[(start, end, i)].append(note)
                    notesdict[
                        ((start * i + note.start) / (i + 1), (end * i + note.end) / (i + 1), i + 1)] = notesdict.pop(
                        (start, end, i))
                else:
                    notesdict[(note.start, note.end, 1)] = [note]
        ordernotes = collections.OrderedDict(sorted(notesdict.items(), key=lambda x : x[0][0]))
        for (start, end, _), notes in ordernotes.items():
            newnotes.append(self.convertnote(notes, wholenote))
        return newnotes

    @classmethod
    def convertnote(cls, notes, wholenote):
        accidentals = {'#': 1, 'b': -1}
        steps = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}
        duration = sum(note.duration for note in notes) / len(notes)
        duration = lyutils.Duration(*cls.tonearest(duration / wholenote))
        pitches = []
        for note in notes:
            step = steps[note.name[0]]
            accidental = accidentals[note.name[1]] if note.name[1] in accidentals.keys() else 0
            octave = int(note.name[-1])  # - 3?
            pitches.append(lyutils.Pitch(octave, step, accidental))
        return lyutils.Note(pitches, duration)

    # finds the nearest power of 2 to the number i
    @staticmethod
    def tonearest(i, tol=.25):
        log = math.log(i, 2)
        nearest = 2**(round(log, 0))
        if nearest-tol < log < nearest+tol:
            return nearest, 1
        return nearest, 0  # todo: add support for double dotted notes


# presets:
# pitches are the sounded pitch, not the written pitch
VIOLIN = Instrument('g3', 'a7', 'violin')
VIOLA = Instrument('c3', 'e6', 'viola')
CELLO = Instrument('c2', 'c6', 'cello')
BASS = Instrument('e1', 'c4', 'bass')