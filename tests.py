import librosa
import audioutils
import os
import lyutils # unused at the moment, but here to make sure the import works
from audioutils import VIOLIN, VIOLA, CELLO, PIANO, Instrument
import midiutils
import warnings

# todo reorganize audioutils into seperate files for pitch and onset detection stuff
# todo try making a stream type music object where it is read in order through a while loop and can have attributes like current_key and current_tempo



TESTPATH = '.\\tests\\'
RESULTSPATH = '.\\tests\\results\\'

'''
TODO: add presets for each instrument to determine how onsets should be detected and what pitches to convert to notes
Possible key detection: run a pitch analysis of the whole track (can skip octave correction part) to determine dominant pitch
    Possibly try to compress track down to one octave first? (transpose all notes outside of that octave into it)
    Could also take the weighted average of all found notes, after removing octave component
'''


def test(fname, instruments, output=True):
    a = audioutils.LibrosaObject(os.path.join(TESTPATH, fname))
    a.getNotes()
    if output:
        a.outputNotes()
    insts = a.splittoinstruments(instruments)
    tracks = [inst.tomiditrack() for inst in insts]
    music = midiutils.Music(tracks)
    music.file(os.path.join(RESULTSPATH, fname) + '.mid')


def testmidi():
    # directly copied from mido docs # todo add link
    from mido import Message, MidiFile, MidiTrack
    mid = MidiFile(type=1)
    track = MidiTrack()
    track.append(Message('program_change', program=12, time=0))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    mid.tracks.append(track)
    mid.save(os.path.join(RESULTSPATH, 'new_song.mid'))


def testly(fname, instruments, tempo, output=True, prop=False):
    print(fname)
    testpath = '.\\testsp\\' if prop else TESTPATH
    resultspath = '.\\testsp\\results' if prop else RESULTSPATH
    if prop and not (os.path.exists(testpath) and os.path.exists(resultspath)):
        warnings.warn('Proprietary test or result path not found. Skipping this test')
        return
    a = audioutils.LibrosaObject(os.path.join(testpath, fname))
    a.getNotes()
    if output:
        a.outputNotes()
    insts = a.splittoinstruments(instruments)
    music = lyutils.Music(tempo, insts)
    music.write(os.path.join(resultspath, fname+'.ly'))


def testInternals(fname):
    y, sr = librosa.load(os.path.join(TESTPATH, fname))
    audioutils.pitchfs.autocorrelate(y)

testmidi()

instruments = [VIOLIN, CELLO]
# test('15 Romantic Flight.mp3', instruments, False)
# testly('26 Battle Cry of Freedom.mp3', [Instrument(65, preset=PIANO)], True, prop=True)
# test('cmajor.wav', instruments, True)
testly('cmajorpiano.wav', [Instrument(60, preset=PIANO)], 60, True)  # todo figure out why tempo is in both audioutils.Instrument and lyutils.music
# testly('4 strings pizz.wav', [Instrument(80, preset=VIOLA)], 80, True)
# testInternals('cmajorpiano.wav')
# testly('Battle-Cry-of-Freedom.wav', [Instrument(60, preset=PIANO)], 60, True, prop=True)
testly('Isle-of-Innisfree.wav', [Instrument(60, preset=PIANO)], 60, True, prop=True)
# testly('Lovely Piano Song.mp3', [Instrument(105, preset=PIANO)], 105, True)
