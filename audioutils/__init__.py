from .LibrosaObject import LibrosaObject
from .Note import Note
from .MusicObject import MusicObject
from .exceptions import *


#run tests
if __name__ == '__main__':
##    from time import clock
##    #test = LibrosaObject('..\\tests\\Kongo Themes.mp3', cachePath='K:\\cache')
##    start = clock()
    #test = LibrosaObject('..\\tests\\15 Romantic Flight.mp3')#, cachePath='K\\cache')
    #test = LibrosaObject('..\\tests\\220sine.wav')
    #test = LibrosaObject('..\\tests\\egmont.mp3')
    #curve = test.pitchCurve()
    #test.writeNotes()
    #test = LibrosaObject('..\\tests\\26 Battle Cry of Freedom.mp3')
    test = LibrosaObject('..\\tests\\Homeward Bound cello.mp3')
    test.getNotes()
    test.outputNotes()

    #test.testInvert()
    
##   test = LibrosaObject('..\\tests\\Liberty and Justice for All.mp3')
##    start2 = clock()
##    #test = librosaObject('tests\\Nearer My God to Thee - Cello solo with piano and orchestra.mp3')
##    #test.getOnsets3()
##    #test.getOnsets4()
##    test.getNotes()
##    print 'getting notes finished'
##    t = clock()
##    print t-start
##    print t-start2
##    test.outputNotes()
##    print 'outputting notes finished'
##    t = clock()5
##    print t-start
##    print t-start2
    #test.getNotes()
#1760.17387859
#1754.19061712
