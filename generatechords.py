import mingus
import lyutils
import librosa
'''
This file will generate chords, randomly or based on a specified progression
'''

def genhelper(n, key, progression):
    '''
    :param n: Number of chords to generate. Need not be a multiple of the progression length
    :param key: The key the chords should be in
    :param progression:
    :return: yields n Mingus chords
    '''
    for i in range(n):
        if callable(progression):
            yield progression(i, key)
        else:
            yield progression[len(progression) % i]


def toPitch(name, octave):
    '''
    :param name: note name (c, d, e) etc
    :param octave: note octave, integer
    :return: an lyutils Pitch
    '''
    return lyutils.Pitch.frommidi(librosa.core.note_to_midi(name+'0') + 12*octave)

