import copy
import librosa
import numpy
from numpy import pi, polymul
from scipy.signal import bilinear
from scipy import signal

'''
A collection of static methods for dealing with pitch
'''


# copied from https://gist.github.com/endolith/148112
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


def getPitchCheap(y, sr, depth=1, fmin=16, fmax=4000):
    y = copy.deepcopy(y)
    # filt = cls.helper_butter(sr, fmin, fmax) # todo make this work (has a nyqulist error)
    # y = signal.sosfiltfilt(filt, y)
    for _ in range(depth):
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        i = numpy.unravel_index(magnitudes.argmax(),
                                magnitudes.shape)  # unravel_index transforms the bizzare integer returned by argmax into a tuple index
        pitch = pitches[i]
        if _ == depth - 1:
            return pitch
        # now look just at the waveform in the section of the predicted pitch
        radius = .25
        fmax = pitch * (1 + radius)
        fmin = pitch * (1 - radius)
        filt = helper_butter(sr, fmin, fmax)
        y = signal.sosfiltfilt(filt, y)

def findOctave(y, sr, note):
    '''
    :param y: waveform to get pitch on
    :param sr: sampling rate of the waveform
    :param note: the frequency of the detected pitch
    :return: the corrected pitch

    Adapted from https://github.com/ad1269/Monophonic-Pitch-Detection
    '''
    threshold = .9
    pass


def autocorrelate(y, n=2):
    '''
    :param y: waveform to be autocorrelated (numpy array)
    :param n: the number of times to perform an autocorrelation
    :return: the nth autocorrelation of y
    adapted from https://dsp.stackexchange.com/a/388
    '''
    prevAutocorr = numpy.fft.rfft(y)
    for _ in range(n):
        prevAutocorr = prevAutocorr*numpy.conj(prevAutocorr)
    return numpy.fft.irfft(prevAutocorr)

# just a wrapper for scipy.signal.butter for readability
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