from . import lysrc
import math
import librosa


'''notes:
currently, a duration must be specified (unlike in lilypond, where a note automatically
takes the duration of it's predecessor

attributes:
pitch:      an integer describing the distance, in semitones, of the note from the c below middle C (unmodified c in lilypond 
            absolute mode, tenor c, or c-3)
duration:   an integer describing the duration of the note, the same way as in lilypond. longas and breves are -1 and -2 respectivly
accidental: Whether the note is sharp or flat. Will be constants.LYSHARP or constants.LYFLAT

'''
class Note(object):
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
        duration = note.toInt(tempo)
        duration = Duration(math.log(duration, 2), 0)
        pitch = Pitch.fromhz(note.freq)
        return cls(pitch, duration)

    def __str__(self):
        if len(self.pitches) > 1:
            string = '<' + ' '.join(map(str, self.pitches)) + '>'
        else:
            string = str(self.pitches[0])
        return string + str(self.duration)


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

    @classmethod
    def fromhz(cls, freq):
        return cls.frommidi(int(round(librosa.core.hz_to_midi(cls.normalizenote(freq)), 0)))

    @classmethod
    def frommidi(cls, midi):
        print(midi)
        C = librosa.core.note_to_midi('c3')
        midilist = [0, 2, 4, 5, 7, 9, 11]
        mididict = dict(zip(midilist, range(6+1)))
        octave, halfstep = divmod(midi-C, 12)
        octave = int(octave)
        # todo change step to be the lilypond step number, not the midi number (probably use a dictionary)
        step = min(midilist, key=lambda x : abs(x-halfstep))  # gets the nearest natural note
        alteration = halfstep-step  # the left over accidental
        step = mididict[step]
        print(octave, step, alteration)
        return cls(octave, step, alteration)

    def __str__(self):
        return repr(self)

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

    def __str__(self):
        return repr(self)
