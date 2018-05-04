import audioutils
import os
import lyutils # unused at the moment, but here to make sure the import works
from audioutils import VIOLIN, VIOLA, CELLO, PIANO

TESTPATH = '.\\tests\\'
RESULTSPATH = '.\\tests\\results\\'

'''
TODO: add presets for each instrument to determine how onsets should be detected and what pitches to convert to notes
'''

def test(fname, instruments, output=True):
    a = audioutils.LibrosaObject(os.path.join(TESTPATH, fname))
    a.getNotes()
    if output:
        a.outputNotes()
    testmus = a.toMusic(instruments)
    # print(str(testmus))
    testmus.write(os.path.join(RESULTSPATH, fname+'.ly'))  # todo: remove previous file extension before the .ly


instruments = [VIOLIN, CELLO]
# test('15 Romantic Flight.mp3', instruments, False)
test('26 Battle Cry of Freedom.mp3', [PIANO], True)
# test('cmajor.wav', instruments, True)
