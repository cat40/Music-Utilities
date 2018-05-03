# from pygame import mixer  # this is a little slow, see if another dedicated module would be faster
import os
import librosa
from scipy import signal
import numpy
import math

import lyutils
from .Cache import Cache
from .Note import Note
from numpy import pi, polymul
from scipy.signal import bilinear


# use a combination of onset detection and frequency detection to get note times, durations, and frequencies
# try playing with genre recognition after notes are finished
# also look at instrument classification

# just a wrapper class for librosa
class LibrosaObject(object):
    # static attributes here
    keymodes = {1: 'Ionian',  # key is the tonic rleative to major scale
                2: 'Dorian',
                3: 'Phrygian',
                4: 'Lydian',
                5: 'Mixolydian',
                6: 'Aeolian',
                7: 'Locrian'}
    '''
    cachePath sets the base path for the cache
    cachePathOverride sets the full path for the cache
    if cache is used, it assumes that all cached files are the same sample rate as the root file.
    caching also assumes that there are no duplicatly named audio files (find a way to mitigate this later)
    To manage cache size, delete sub objects once the object they are used in the create of has been created and cached. 
    '''

    def __init__(self, fname, usecache=True, cachePath='.\\cache\\',
                 cachePathOverride=None):  # change cache to False once testing is completed
        # consider using trim to remove silence on both ends before processing,
        # but remember to add silence back before exporting information (or just play the trimmed file instead)
        # also find a way to cut applause and other noise. (maybe percussion splitting?)
        self.fname = fname
        # load the file
        self.waveform, self.samplingrate = librosa.load(
            fname)  # , sr=None) #sr=None sets it to the file's sampling rate (probably 44100hz). default is 22050
        self.usecache = usecache
        if self.usecache:
            self._cachePath = os.path.join(cachePath, "'" + os.path.basename(
                self.fname) + "'") if cachePathOverride is None else cachePathOverride
            self.cache = Cache(self._cachePath)
        self.beatframes = self.beattimes = self.tempo = None  # these will be initialized when thier functions are called

    def getTempo(self):
        # probably will not catch tempo changes
        # might need to detect those and split based around them (with tempogram?)
        # or use beat frame
        self.tempo, self.beatframes = librosa.beat.beat_track(y=self.waveform, sr=self.samplingrate)
        # convert beat frames to beat times
        self.beattimes = librosa.frames_to_time(self.beatframes, sr=self.samplingrate)
        return self.tempo

    # frame is the distance in seconds to look on each side of the specified time
    # does not work very well, if at all
    def getTempoAtPoint(self, time, frame=5):
        if self.beatframes is None:  # isinstance(self.beatframes, type(None)):
            self.getTempo()
        # anlyze the nearest times
        averagetime = 0
        # print self.beattimes
        releventTimes = [x for x in list(self.beattimes) if x >= time - frame and x <= time + frame]
        prevt = releventTimes[0]
        for t in releventTimes:
            # print t
            averagetime += t - prevt
            prevt = t
        return 60 / (averagetime / len(releventTimes))

    def plotBeats(self, divs=25):
        # only shows every divsth beat
        if self.beattimes is None:  # isinstance(self.beattimes, type(None)):
            self.getTempo()
        from numpy import zeros_like
        import matplotlib.pyplot as pyplot
        beats = [x for i, x in enumerate(self.beattimes) if not i % divs]
        pyplot.plot(beats, zeros_like(beats), '.')
        pyplot.show()

    def sliceAudio(self, split=10):
        split = librosa.core.time_to_samples(split, sr=self.samplingrate)
        duration = librosa.core.time_to_samples(librosa.core.get_duration(y=self.waveform, sr=self.samplingrate),
                                                sr=self.samplingrate)
        for t in range(0, int(duration + 0.5), split):
            yield self.waveform[t:min(t + split, duration)], librosa.core.samples_to_time(t, sr=self.samplingrate)
            # print librosa.core.frames_to_time(len(self.waveform[t:min(t+split, duration)]), sr=self.samplingrate)
            # librosa.output.write_wav(os.path.splitext(self.fname)[0] + '_%s.wav' % t, self.waveform[t:min(t+split,
            # duration)], self.samplingrate)

    '''todo:
    combine make a way to eliminate onsets within some distance (~1ms?) of each other to avoid duplicates from multiple methods, not needed with current implimentation of notes
    try splitting by silence to help with detection, also play around with the mean levels
    consider also not mixing down to mono when the file is loaded, becuase often there are different parts
    panned differently (perhaps try and detect if staying in stereo is worth it)
    also consider splitting by a much smaller pitch margin (half step or smaller) to get a better output
    from the sine wave generator
    '''

    def getOnsets(self, debug=False):
        if self.usecache:
            try:
                return self.cache.load('onsets')
            except:  # cModule.CacheNotFoundError:
                pass
        onsets = []  # might need to make this a numpy array for better management
        harmonic, percussive = self.splitHarmonicPercussive()  # test this, also seems to take a very long time. Consider making the defenition of a perucssive sound more strict(see librosa docs)
        # split remaining by frequency (make sure the above isn't good enough first
        onsetsP = self.onsets_helper(percussive, self.samplingrate)
        onsets.append((onsetsP, percussive))
        # numpy.concatenate([onsets, (onsetsP, percussive)])
        for i, y in enumerate(self.splitByFifths(y=harmonic)):
            onsets_i = self.onsets_helper(y, self.samplingrate)
            # numpy.concatenate([onsets, (onsets_i, y)])
            onsets.append((onsets_i, y))
            if debug:
                clicks = librosa.core.clicks(frames=librosa.core.samples_to_frames(onsets_i), sr=self.samplingrate,
                                             click_freq=220)
                librosa.output.write_wav(os.path.join('tests\\results',
                                                      os.path.splitext(os.path.basename(self.fname))[
                                                          0] + '_onsets_octave_%s.wav' % i), clicks, self.samplingrate)
        if debug:
            librosa.output.write_wav(os.path.join('tests\\results', os.path.splitext(os.path.basename(self.fname))[
                0] + '_percussive.wav'), percussive, self.samplingrate)
            librosa.output.write_wav(
                os.path.join('tests\\results', os.path.splitext(os.path.basename(self.fname))[0] + '_harmonic.wav'),
                harmonic, self.samplingrate)
            clicks = librosa.core.clicks(frames=librosa.core.samples_to_frames(onsetsP), sr=self.samplingrate,
                                         click_freq=220)
            librosa.output.write_wav(
                os.path.join('tests\\results', os.path.splitext(os.path.basename(self.fname))[0] + '_onsets_p.wav'),
                clicks, self.samplingrate)
        if self.usecache:
            self.cache.write(onsets, 'onsets')
        ##            self.cache.writeBatch((harmonic, 'harmonic'),
        ##                                  (percussive, 'percussive'),
        ##                                  (onsets, 'onsets'))

        return onsets

    def getOnsetsSimple(self, debug=False):
        if self.usecache:
            try:
                return self.cache.load('onsets2')
            except:  # cModule.CacheNotFoundError:
                pass
        return [(self.onsets_helper(self.waveform, self.samplingrate), self.waveform)]

    # @staticmethod
    def getPitch(self, y, i, j, x, fmin=16, fmax=4000):
        # mostly from https://musicinformationretrieval.com/pitch_transcription_exercise.html
        # autocorrelate
        print('autocorrelating')
        cached = False
        if self.usecache:
            try:
                r = self.cache.load('autocorrelation-%s-%s-%s.npy' % (i, j, x))
            except Exception as e:  # cModule.CacheNotFoundError:
                print(e)
            else:
                print('else')
                cached = True
        if not cached:
            print('really autocorrelating')
            r = librosa.autocorrelate(y)
            if self.usecache:
                self.cache.write(r, 'autocorrelation-%s-%s-%s' % (i, j,
                                                                  x))  # this causes the re-use of autocorrelations. need to fix. Perhaps try autocorrelating the whole thing at once
        print('autocorrelated')
        # define limits
        imin = self.samplingrate / fmax  # I don't think these are backwards
        imax = self.samplingrate / fmin
        print(imin, imax)
        r[:int(
            imin)] = 0  # -sys.float_info.max#float('-inf') #apparently numpy supports mass assignement by slice syntax. All indexes in the slice have thier values set to 0
        r[int(imax):] = 0  # -sys.float_info.max#float('-inf')
        # find index of maximum autocorrelation
        print(r)
        index = r.argmax()  # consider caching this too
        print(max(r))
        print(index)
        return self.samplingrate / index  # note frequency

    def getNotes(self):
        self.notes = []
        if self.usecache:
            try:
                self.notes = self.cache.load('notes')
                return self.notes
            except:  # cModule.CacheNotFoundError:
                pass
        for x, (onsets, y) in enumerate(self.getOnsets(debug=True)):
            # go through each onset
            for i, j in zip([0] + list(onsets), list(onsets) + [len(y)]):
                # pitch = self.getPitch(y[i:j], i, j, x)
                pitch = self.getPitchCheap(y[i:j], self.samplingrate)
                # rmse = librosa.feature.rmse(y=y[i:j])
                # print 'have rmse'
                # volume = sum(rmse)/len(rmse) #for some reason, this is still an array
                # volume = abs(librosa.stft(y[i:j])) #seems to be the source of the meonory problem
                # possibly might just be that the array is very large, and adding it to the note objects takes a lot of memoty
                # print volume.shape
                volume = self.rmse(y[i:j])
                # volume = 0
                if volume > 10 ** -5 and pitch > 0:
                    self.notes.append(Note(pitch, librosa.core.samples_to_time(i, sr=self.samplingrate),
                                           librosa.core.samples_to_time(j, sr=self.samplingrate),
                                           volume))
        if self.usecache:
            self.cache.write(self.notes, 'notes')
        return self.notes

    # determine the dominate note (key name), and dominatent key signature (key mode)
    def getKey(self):
        pass

    def outputNotes(self):

        '''
        todo: use smaller bins (with octaive bins, the main part and then fringe harmonies are empahsized, but middle is lost
        de-emphasize higher frequencies
        '''
        waveform = numpy.zeros(self.waveform.shape)
        # print self.notes
        for note in self.notes:  # filter(lambda note : note.volume > 0.01, self.notes):
            start = librosa.core.time_to_samples(note.start, self.samplingrate)
            end = librosa.core.time_to_samples(note.end, self.samplingrate)
            print(start, end)
            print(note.start, note.end)
            print(note.freq)
            # waveform[start:end] += self.genSine(note.freq, 0.5, self.samplingrate, end-start)
            sine = self.genSineFunc(self.normalizeNote(note.freq), note.volume, self.samplingrate)
            for i, x in enumerate(waveform[start:end]):
                print(i, x)
                break
            waveform[start:end] = [(sine(i) + x) for i, x in enumerate(waveform[start:end])]
            # map(lambda x : sine(i) + x, waveform[start:end])
            print('a')
        b, a = self.A_weighting(48000)
        waveform = signal.filtfilt(b, a, waveform)  # perform a-weighting
        librosa.output.write_wav(
            os.path.join('tests\\results', os.path.splitext(os.path.basename(self.fname))[0] + '_notes.wav'),
            waveform, self.samplingrate)

    '''
    not actually an inversion, but can't think of a better name. Inverts the absolute value of the amplitude. 
    '''

    def testInvert(self):
        yInv = numpy.array([(1 - abs(x)) for x in self.waveform])
        # yInv = numpy.array([math.copysign(1-abs(x), x) for x in self.waveform])
        librosa.output.write_wav(
            os.path.join('tests\\results', os.path.splitext(os.path.basename(self.fname))[0] + '_test_invert.wav'),
            yInv, self.samplingrate)

    def pitchCurve(self):
        '''
        instead of swapping axes, could ge thte dominant frequency at each bin and time and use them all
        '''
        ##        #stft = librosa.core.stft(self.waveform)
        ##        freqs, stft = librosa.core.ifgram(self.waveform, sr=self.samplingrate)
        ##        print freqs
        ##        print '\n'*15
        ##        print freqs[1, numpy.argmax(freqs[1])]*self.samplingrate
        print('piptracking')
        p, m = librosa.piptrack(y=self.waveform, sr=self.samplingrate)
        p = numpy.swapaxes(p, 0, 1)
        m = numpy.swapaxes(m, 0, 1)
        print(p)
        # get dominant frequency at each time
        for t, (mag, pitch) in enumerate(
                zip(list(m), list(p))):  # xrange(librosa.core.samples_to_frames(len(self.waveform))):
            i = numpy.argmax(mag)
            yield pitch[i], mag[i]

    def writeNotes(self):
        waveform = numpy.empty((0,))  # numpy.zeros(self.waveform.shape)
        for i, (pitch, mag) in enumerate(self.pitchCurve()):
            start = librosa.core.frames_to_samples(i)
            end = librosa.core.frames_to_samples(i + 1)
            sine = self.genSineFunc(pitch, mag, self.samplingrate)
            # print i, pitch, mag
            waveform = numpy.concatenate([waveform, [sine(x) for x in range(librosa.core.frames_to_samples(1))]])

            # print 'bin done'
        librosa.output.write_wav(
            os.path.join('..\\tests\\results', os.path.splitext(os.path.basename(self.fname))[0] + '_notes2.wav'),
            waveform, self.samplingrate)

    def magCurve(self):
        phrase = librosa.core.frames_to_samples(1, self.samplingrate)
        for t in range(1, librosa.core.samples_to_frames(len(self.waveform))):
            pass

    # apply a butterworth filter to seperate the buttermilk from the butter
    def butter(self, fmin=0, fmax=None, order=6, y=None):
        # assert fmin != 0 or fmax is not None, 'failed to specify a minimum or maximum frequency'
        filterbank = self.helper_butter(self.samplingrate, fmin, fmax, order)
        if y is None: y = self.waveform
        return signal.sosfiltfilt(filterbank, y)  # (*(filterbank+(self.waveform,)))

    def splitInThirds(self):
        # more or less taken from librosa examples
        # make a spectogram
        D = librosa.stft(self.waveform)
        # seperate magnitude and phase
        magnitude, phase = librosa.magphase(D)
        # sepeate components and activations
        components, activations = librosa.decompose.decompose(magnitude, n_components=8, sort=True)
        # do the spltting:
        levels = []
        for k in (0, len(activations) // 2, -1):
            # use outer product of component k and activations to reconstuct spectogram, whatever that means
            spect = numpy.multiply.outer(components[:, k], activations[k])
            # invert put the phase back and invert the result
            levels.append(librosa.istft(spect * phase))
        return levels

    '''
    A generator. Splits the waveform into octaves from c1 to the highest c possible at sampling rate
    not sure of octmax should be 8 or 9 (8 is too small, 9 is too large, so going with too many onsets instead of too few for now)
    not sure why it still works on music beow octave 5
    '''

    def splitByOctave(self, octavesPerBin=1, y=None, octmin=6,
                      octmax=9):  # another candiate for caching, would need to be made a non generator object, or something similar (possibly dynamically write a list?)
        # will ignore remander if ocatves%octavesPerBin
        assert octmin >= 1
        assert octmax <= int(math.log(self.samplingrate / (2 * librosa.core.note_to_hz('c0')), 2))
        if y is None: y = self.waveform
        for octave in range(octmin, octmax + 1, octavesPerBin):
            # get frequency bounds
            minfreq = librosa.core.note_to_hz('c' + str(octave - 1))
            maxfreq = librosa.core.note_to_hz('c' + str(octave))
            # apply a butterworth filter
            yield self.butter(fmin=minfreq, fmax=maxfreq, y=y)

    def splitByFifths(self, y=None, octmin=1, octmax=9):
        if y is None: y = self.waveform
        minfreq = librosa.core.note_to_hz('c' + str(octmin - 1))
        maxfreq = librosa.core.note_to_hz('c' + str(octmax))
        scale = 3 / 2.
        freq = oldfreq = minfreq
        while freq <= maxfreq:
            freq = self.normalizeNote(freq * scale)
            yield self.butter(fmin=oldfreq, fmax=freq, y=y)
            oldfreq = freq

    '''
    a wrapper function for librosa.effects.hpss that implements file caching
    note: if caching is used, assumes keyword arguments have not changed (use overrideCache to avoid this)
    '''

    def splitHarmonicPercussive(self, overrideCache=False, **kwargs):
        # might make harmonic and perucussive full object attributes, see how much memory that takes
        if self.usecache:
            try:
                harmonic = self.cache.load('harmonic.npy')
                percussive = self.cache.load('percussive.npy')
                return harmonic, percussive
            except:  # cModule.CacheNotFoundError:
                pass
        '''
        >>> # Get a more isolated percussive component by widening its margin
        >>> y_harmonic, y_percussive = librosa.effects.hpss(y, margin=(1.0,5.0))
        '''
        harmonic, percussive = librosa.effects.hpss(self.waveform, **kwargs)
        if self.usecache:
            self.cache.write(harmonic, 'harmonic')
            self.cache.write(percussive, 'percussive')
        return harmonic, percussive

    def splittoinstruments(self, instruments):
        for instrument in instruments:
            instrument.notes = [note for note in self.notes if instrument.minnote <= note.freq <= instrument.maxnote]
        return instruments  # not strictly necessary, as the instruments list will be modified in place
        # to avoid modifying in place, create a new Instrument object with the old instrument as the preset

    def toMusic(self, instruments, base=4):
        instruments = self.splittoinstruments(instruments)
        globalblock = [lyutils.Time(4, 4), lyutils.Key('c', 'major')]
        return lyutils.Music(instruments, globalparts=globalblock, basenote=base)

    # just a wrapper for scipy.signal.butter for readability
    @staticmethod
    def helper_butter(sr, fmin=0, fmax=None, order=6, output='sos'):
        nyquist = sr / 2
        assert fmax < nyquist, 'maximum frequency is above the Nyquist frequency'
        cutofflow = fmin / nyquist
        if fmax is None:
            return signal.butter(order, cutofflow, btype='lowpass', output=output)
        cutoffhigh = fmax / nyquist
        if fmin:
            return signal.butter(order, (cutofflow, cutoffhigh), btype='bandpass', output=output)
        return signal.butter(order, cutoffhigh, btype='highpass', output=output)

    @classmethod
    def condenseOnsets(cls, onsets):
        new = numpy.empty((0,))
        onsets.sort()
        iteronsets = iter(enumerate(onsets))  # willing to guess this is ineffecient
        next(iteronsets)  # skip first value.
        for i, onset in iteronsets:
            if not cls.closeTo(onset, onsets[i - 1]):  # this will remove all onsets that are chained just close enough
                #  to each other, may not be desireable
                numpy.append(new, onset)

    @staticmethod
    def closeTo(a, b, distance=5):
        return not (a <= b - distance or a >= b + distance)

    ##
    @staticmethod
    def genSineFunc(freq, amp, sr):
        return lambda x: amp * math.sin(2 * numpy.pi * freq * x / sr)

    # copied from https://gist.github.com/endolith/148112
    @staticmethod
    def A_weighting(fs):
        """Design of an A-weighting filter.
        b, a = A_weighting(fs) designs a digital A-weighting filter for
        sampling frequency `fs`. Usage: y = scipy.signal.lfilter(b, a, x).
        Warning: `fs` should normally be higher than 20 kHz. For example,
        fs = 48000 yields a class 1-compliant filter.
        References:
           [1] IEC/CD 1672: Electroacoustics-Sound Level Meters, Nov. 1996.
        """
        # Definition of analog A-weighting filter according to IEC/CD 1672.
        f1 = 20.598997
        f2 = 107.65265
        f3 = 737.86223
        f4 = 12194.217
        A1000 = 1.9997

        NUMs = [(2 * pi * f4) ** 2 * (10 ** (A1000 / 20)), 0, 0, 0, 0]
        DENs = polymul([1, 4 * pi * f4, (2 * pi * f4) ** 2],
                       [1, 4 * pi * f1, (2 * pi * f1) ** 2])
        DENs = polymul(polymul(DENs, [1, 2 * pi * f3]),
                       [1, 2 * pi * f2])

        # Use the bilinear transformation to get the digital filter.
        # (Octave, MATLAB, and PyLab disagree about Fs vs 1/Fs)
        return bilinear(NUMs, DENs, fs)

    '''
    Another pitch getting method. precision on a pure sine wav seems to be about +- 0.5 to 1
    how it works:
    librosa.piptrack returns paralell arrays of pitches and magnitudes for each bin. Pitch at the max magnidute is the dominent pitch. 
    '''

    @staticmethod
    def getPitchCheap(y, sr, fmin=16, fmax=4000):
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        i = numpy.unravel_index(magnitudes.argmax(),
                                magnitudes.shape)  # unravel_index transforms the bizzare integer returned by argmax into a tuple index
        return pitches[i]

    @staticmethod
    def rmse(y):
        # return math.sqrt(1/len(y) * sum(n**2 for n in y))
        return numpy.sqrt(numpy.mean(y ** 2))

    '''
    converts a frequency to the nearest note, then back to that note's frequency (fixes pitch getting error)
    '''

    @staticmethod
    def normalizeNote(freq):
        return librosa.core.note_to_hz(librosa.core.hz_to_note(freq))

    @staticmethod
    # a wrapper for librosa.onset.onset_detect
    def onsets_helper(y, sr):
        onsetEnvelopes = librosa.onset.onset_strength(y, sr=sr, hop_length=100)
        return librosa.onset.onset_detect(y=y, sr=sr, hop_length=100, units='samples',
                                          pre_max=20, post_max=20, pre_avg=100, post_avg=100,
                                          delta=sum(onsetEnvelopes) / len(onsetEnvelopes), backtrack=True)

    @staticmethod
    def genSine(freq, amp, sr, duration):
        duration = librosa.core.time_to_samples(duration)
        print(duration)
        period = librosa.core.time_to_samples(1 / freq)
        print(period)
        x = numpy.arange(period)  # numpy.linspace(0, duration, num=duration)
        print(x)
        print(freq)
        print(sr)
        print(amp)
        print(amp * numpy.sin(2 * numpy.pi * freq * x / sr))
        return numpy.tile(amp * numpy.sin(2 * numpy.pi * freq * x / sr), duration / period)


'''
How things work:
onset detection splits it by percussive sounds and octaves. Each is passed with the waveform the onset function was run on to getPitch(), which splits the waveform
at the onsets and detects the dominant pitch, which is combined with the lenth of the interval to produce a note.

notes will assume the note continues until th enext onset. To mitigate, try inverting the waveform (as in 1 - x for x in waveform) and onset detecting to detect silence (also might sound cool)
and pairing onsets

notes:
when interpreting the note frequencies, make sure to use a log base 2 scale, because that's the way musical notes work


can possilby just get the dominant frequency in each octave or bin at each point, and update the program at each point (or some number of points)
'''
