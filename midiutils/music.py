import mido


class Music(object):
    def __init__(self, tracks, resolution=256):
        self.tracks = tracks
        self.resolution = resolution
        for track in tracks:
            track.resolution = self.resolution

    def file(self, fname):
        midif = mido.MidiFile(type=1)
        for track in self.tracks:
            midif.tracks.append(track)
        midif.save(fname)

