from . import lysrc
import math
import librosa
import itertools

# todo refactor code to avoid using str() to convert to lilypond
class Note(object):
    '''notes:
    currently, a duration must be specified (unlike in lilypond, where a note automatically
    takes the duration of it's predecessor

    attributes:
    pitch:      an integer describing the distance, in semitones, of the note from the c below middle C (unmodified c in lilypond
                absolute mode, tenor c, or c-3)
    duration:   an integer describing the duration of the note, the same way as in lilypond. longas and breves are -1 and -2 respectivly
    accidental: Whether the note is sharp or flat. Will be constants.LYSHARP or constants.LYFLAT

    '''
    def __init__(self, pitches, duration, useRelative=True):
        self.pitches = pitches if isinstance(pitches, (list, tuple)) else [pitches]
        if isinstance(duration, Duration):
            self.duration = duration
        else:
            self.duration = Duration(duration, 0)  # assumes no dots. might add conversion from a different kind of integer later
        self.useRelative = useRelative

    # todo: impliment doublestops
    @classmethod
    def fromAudioutils(cls, tempo, note):
        # notes = tuple(notes)
        duration = Duration.fromtime(note.duration, tempo)
        print(duration)
        pitch = Pitch.fromhz(note.freq)
        return cls(pitch, duration)

    def to_lilypond_string(self):
        if len(self.pitches) > 1:
            string = '<' + ' '.join(map(str, self.pitches)) + '>'
        else:
            string = str(self.pitches[0])
        return string + str(self.duration)

    def __str__(self):
        ''' this has been kept only until code can be refactored to avoid usage of str to convert to lilypond'''
        return self.to_lilypond_string()


'''
These are just wrapper classes for the lilypond source classes to make them a bit easier to work with
Arguments have been explained as I understand them, not nessesarily as implemented in the lilypond source code
'''
class Pitch(lysrc.Pitch):
    def __init__(self, octave, step, alteration):
        super().__init__()
        self.step = step  # step above c in the octave, where c = 0, d = 1, a=5, b=6, etc
        self.octave = octave  # the octave of the note, where c3 is 0 and middle c is 1
        self.alteration = alteration  # number of semitones above or below the step, I think
                                         # (1=sharp, 2=doublesharp, -1=flat, -2=double flat
        self._force_absolute_pitch = True

    @classmethod
    def fromhz(cls, freq):
        return cls.frommidi(int(round(librosa.core.hz_to_midi(cls.normalizenote(freq)), 0)))

    @classmethod
    def frommidi(cls, midi):
        C = librosa.core.note_to_midi('c3')
        midilist = [0, 2, 4, 5, 7, 9, 11]
        mididict = dict(zip(midilist, range(6+1)))
        octave, halfstep = divmod(midi-C, 12)
        octave = int(octave)
        step = min(midilist, key=lambda x : abs(x-halfstep))  # gets the nearest natural note
        alteration = halfstep-step  # the left over accidental
        step = mididict[step]
        return cls(octave, step, alteration)

    @staticmethod
    def normalizenote(freq):
        return librosa.core.note_to_hz(librosa.core.hz_to_note(freq))


class Duration(lysrc.Duration):
    def __init__(self, duration_log, dots, factor=None):
        super().__init__()
        self.duration_log = duration_log  # The duration as a log base 2 (quarter note = 2, whole note = 0, etc)
        self.dots = dots  # number of dots
        if factor is not None:
            self.factor = factor  # todo: figure out what this does

    @classmethod
    def fromtime(cls, duration, tempo):
        '''
        :param duration:
        :param tempo: can be a number or a tuple (bpm, note_base) where note_base is the note that gets the beat
        If tempo is a single number, quarter note base will be assumed
        :return:
        TODO: add support for dotted notes
        '''
        # convert an integer tempo to a tuple tempo (assumes quarter note base
        if isinstance(tempo, (float, int)):
            tempo = tempo, 4
        secondsPerBeat = 60 / tempo[0]
        numBeats = duration / secondsPerBeat
        print(numBeats, duration)
        noteValue = (1 / numBeats) * tempo[1]  # converts to absolute note
        print(noteValue)
        validValues = list(itertools.chain.from_iterable((2**x, 2/3 * 2**x) for x in range(5+1)))
        note = min(validValues, key=lambda x: abs(x - noteValue))
        print(note)
        dot = validValues.index(note) % 2  # if the index is even, no dot. If odd, dot
        return cls(int(math.log(int(note/(2/3)), 2)), dot)
