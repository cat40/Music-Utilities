import mingus.core.chords as Chords
import mingus.core.progressions as Progressions
import lyutils
import librosa
import random
'''
This file will generate chords, randomly or based on a specified progression
'''

def genhelper(n, key, progression):
    '''
    :param n: Number of chords to generate. Need not be a multiple of the progression length
    :param key: The key the chords should be in
    :param progression:
    :return: yields n chord names (I, IV, etc)
    '''
    for i in range(n):
        if callable(progression):
            yield progression(i, key)
        else:
            yield progression[len(progression) % i]

def genChords(progressions):
    '''
    :param progressions: A list of the following strcuture:
    [[chords, key, n=len(chords)]] or [[chordfunction, key, n]]
    :return: All the chords as a list of Mingus chords
    TODO implement octaves
    '''
    chords = []
    for progression in progressions:
        prog, key = progression[0:1+1]
        try: n = progression[2]
        except IndexError:
            if not callable(prog):
                n = len(prog)
            else: raise
        chords.extend(Progressions.to_chords(genhelper(n, key, prog)))
    return chords


def toPitch(name, octave):
    '''
    :param name: note name (c, d, e) etc
    :param octave: note octave, integer
    :return: an lyutils Pitch
    '''
    print(name)
    return lyutils.Pitch.frommidi(librosa.core.note_to_midi(name+'0') + 12*octave)


def toly(chords, duration, instrument, octave):
    '''
    :param chords: a list of Mingus chords, where a chord is a list of note letters (ex. [C, E, G])
    :param duration: an lyutils.Duration to denote the duration of the notes
    :param instrument: An lyutils.Instrument, with everything pre-initalized
    :param octave: octave the notes should be in
    todo: expand octave to allow octave changing
    :return: None. Instrument's sequence has been modified
    '''
    print(chords)
    pitches = [list(map(lambda x: toPitch(x, octave), chord)) for chord in chords]
    print(pitches)
    notes = (lyutils.Note(pitch, duration) for pitch in pitches)
    instrument.sequence.extend(notes)


def randomchord(_, __):
    '''
    :param _: garbage can for the index argument supplied in genhelper
    :param __: garbage can for the key argument supplied in genhelper
    :return: a random chord
    '''
    return random.choice(Chords.chord_shorthand.keys())


def randomchordsimple(_, __):
    '''
    :param _: garbage can for the index argument supplied in genhelper
    :param __: garbage can for the key argument supplied in genhelper
    :return: a random chord in the specified, using only the natural diatonic triads
    '''
    return lyutils.romannumerals(random.randint(1, 7)).upper()

# run tests
if __name__ == '__main__':
    # produce a random chord progression
    progression = []
    for key in 'ABCDEFG':
        progression.append([randomchordsimple, key, 12])
    chords = genChords(progression)
    inst = lyutils.Instrument('cello', [])
    toly(chords, lyutils.Duration(0, 0), inst, 2)
    music = lyutils.Music(80, [inst])
    music.write('.\\tests\\results\\genrandom.ly')
