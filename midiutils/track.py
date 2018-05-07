import mido

'''
a single midi track. Can be multiple per song
Does not currently have support for time or key changes
'''
globalnum = 0  # this only works if 1 music is open at once
# todo change globalnum to be a music attribute
class Track(object):
    def __init__(self, tempo, notes, time=(4, 4), key='C', resolution=256):
        global globalnum
        self.tempo = mido.bpm2tempo(tempo)
        self.tracknum = globalnum
        globalnum += 1 if globalnum != 9 else 2  # skips 10 (percussion reserved)
        self.timesig = time
        self.key = key
        self._messages = [mido.MetaMessage('set_tempo', time=0, tempo=tempo),
                          mido.MetaMessage('time_signature', time=0, numerator=time[0], denominator=time[1]),
                          mido.MetaMessage('key_signature', time=0, key=key)]
        self.notes = notes
        self.resolution = resolution  # this should probably actually be in music

    @property
    def messages(self):
        messages = self._messages + \
                   [message for note in self.notes for message in note.message(self.resolution, self.tempo)]
        for message in messages:
            if not message.is_meta:
                message.channel = self.tracknum
        return messages

    def miditrack(self):
        track = mido.MidiTrack()
        track.extend(self.messages)
        return track
