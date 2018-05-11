import audioutils
import os
import lyutils # unused at the moment, but here to make sure the import works
from audioutils import VIOLIN, VIOLA, CELLO, PIANO, Instrument
import midiutils

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

def testly(fname, instruments, tempo, output=True):
    a = audioutils.LibrosaObject(os.path.join(TESTPATH, fname))
    a.getNotes()
    if output:
        a.outputNotes()
    insts = a.splittoinstruments(instruments)
    music = lyutils.Music(tempo, insts)
    music.write(os.path.join(RESULTSPATH, fname+'.ly'))

testmidi()

instruments = [VIOLIN, CELLO]
# test('15 Romantic Flight.mp3', instruments, False)
# test('26 Battle Cry of Freedom.mp3', [Instrument(65, preset=PIANO)], True)
# test('cmajor.wav', instruments, True)
testly('cmajorpiano.wav', [Instrument(60, preset=PIANO)], 60, True)  # todo figure out why tempo is in both audioutils.Instrument and lyutils.music
testly('4 strings pizz.wav', [Instrument(80, preset=VIOLA)], 80, True)
