import audioutils
import os
import lyutils # unused at the moment, but here to make sure the import works
from audioutils import VIOLIN, VIOLA, CELLO, PIANO
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
    tracks = [inst.tomiditrack(65) for inst in insts]
    music = midiutils.Music(tracks)
    music.file(os.path.join(RESULTSPATH, fname) + 'midi')

def testmidi():
    from mido import Message, MidiFile, MidiTrack
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=12, time=0))
    track.append(Message('note_on', note=64, velocity=64, time=32))
    track.append(Message('note_off', note=64, velocity=127, time=32))
    mid.save(os.path.join(RESULTSPATH, 'new_song.mid'))

testmidi()

instruments = [VIOLIN, CELLO]
# test('15 Romantic Flight.mp3', instruments, False)
test('26 Battle Cry of Freedom.mp3', [PIANO], True)
# test('cmajor.wav', instruments, True)
