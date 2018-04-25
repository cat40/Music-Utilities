import warnings
import os
class MusicObject(object):
    '''
    notes is a list of Note objects
    keys is a list of keys (note letter and mode) and time the key began, as in (key, beginTime)
    tempos is a list of tempos and the time that tempo began, as in (tempo, beginTime)
    baseNote is the length of the longest note, as an inverse fraction (8th note -> 8, etc)
    
    
    it is not reccomended to call __init__ directly, instead use fromNotes and fromFile
    use librosaObject to detect tempo
    transforming note durations into factional notes (whole, half, quarter notes, etc) is not yet implimented. DO THIS LATER
    '''
    def __init__(self, notes, keys, tempos, baseNote=2):
        self.notes = notes
        self.keys = keys
        self.tempos = tempos
        self.baseNote = baseNote

    @classmethod
    def fromNotes(cls, notes, tempos):
        keys = getKeys(notes)
        return cls(notes, keys, tempos)

    @classmethod
    def fromFile(cls, fname):
        with open(fname, 'r') as f:
            pass

    def writeToFile(self, fname, overwrite=True):
        if os.path.exists(fname):
            if overwrite:
                warnings.warn(fname+' already exists and will be overwritten')
            else:
                raise OSError('File %s already exists.' % fname)
        with open(fname, 'w') as f:
            pass


    @staticmethod
    def closeTo(a, b, tol=.05):
        return a >= b-.05 and a <= b+.05
        

'''
ideas to get key:
find the most common note, and hope the second and third most common notes are harmonics (possibly check, and if not, try something else)
    Then find the most common form of each note letter (sharp, flat, natural) and determine key signature for that (use a dictionary of dictionarys of the form:
    {'Bb Major : {'a':'natural', 'b':'flat'}}...
might put this in the class later
'''
def getKeys(notes):
    pass
