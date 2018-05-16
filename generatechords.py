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
        chords.append(Progressions.to_chords(genhelper(n, key, prog)))
    return chords

def toPitch(name, octave):
    '''
    :param name: note name (c, d, e) etc
    :param octave: note octave, integer
    :return: an lyutils Pitch
    '''
    return lyutils.Pitch.frommidi(librosa.core.note_to_midi(name+'0') + 12*octave)


def random(_, key):
    '''
    :param _: garbage can for the index argument supplied in genhelper
    :param key: the key the chord is in
    :return: a random chord in the specified key
    '''
    pass


def randomsimple(_, key):
    '''
    :param _: garbage can for the index argument supplied in genhelper
    :param key: the key the chord is in
    :return: a random chord in the specified key, using only the natural diatonic triads
    '''
    return lyutils.roman
