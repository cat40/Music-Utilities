import audioutils
import os
import lyutils # unused at the moment, but here to make sure the import works
from audioutils import VIOLIN, VIOLA, CELLO

TESTPATH = '.\\tests\\'
RESULTSPATH = '.\\tests\\results\\'

def test(fname, instruments):
    a = audioutils.LibrosaObject(os.path.join(TESTPATH, fname))
    a.getNotes()
    a.outputNotes()
    testmus = a.toMusic(instruments)
    testmus.write(os.path.join(RESULTSPATH, fname+'.ly'))  # todo: remove previous file extension before the .ly
    print(str(testmus))


instruments = [VIOLIN, CELLO]
test('15 Romantic Flight.mp3')
