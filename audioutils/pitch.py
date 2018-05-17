import copy
import math

import librosa
import numpy
from numpy import pi, polymul
from scipy.signal import bilinear
from scipy import signal

'''
A collection of static methods for dealing with pitch
'''
# todo: make a single pitch function with a method argument

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


def getPitchCheap(y, sr, depth=1, fmin=16, fmax=4000):
    '''
    Another pitch getting method. precision on a pure sine wav seems to be about +- 0.5 to 1
    how it works:
    librosa.piptrack returns paralell arrays of pitches and magnitudes for each bin. Pitch at the max magnidute is the dominent pitch.
    '''
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


def getPitch(y, sr):
    '''
    :param y: the waveform to run pitch detection on
    :param sr: the sampling rate of the waveform
    :return: the estimated frequency of the waveform, in hz
    '''
    autocorr = autocorrelate(y)
    estimate = pitchFromAC(autocorr, sr, autocorrelated=True)
    if 20 < estimate < 4000:  # todo make min and max frequencies keyword arguments
        return fixOctave2(autocorr, estimate, sr, log)
    return 0


def pitchFromAC(y, sr, autocorrelated=False):
    '''
    :param y: waveform to run analysis on
    :param sr: sampling rate of the waveform
    :param autocorrelated: whether or not y is an autocorrelation of the actual waveform
    :return: a frequency estimate, in hz
    todo make fmin and fmax keyword arguments
    '''
    fmin = 27.5
    fmax = 4000
    imin = sr // fmax
    imax = sr // fmin
    autocorrelation = y if autocorrelated else autocorrelate(y)
    autocorrelation[:int(imin)] = 0
    autocorrelation[int(imax):] = 0
    timeShift = autocorrelation.argmax()  # find the maximum of the autocorrelation
    print('timeshift', timeShift)
    if not timeShift:
        return 0
    return sr/timeShift # converts the period to a frequenct (timeShift is the number of samples,
    # so divide by sampling rate to get time in seconds and then invert)


def fixOctave(autocorr, note, sr, threshold=.9, maxfreq=4000):
    '''
    :param autocorr: autocorrelation of waveform to get pitch over
    :param note: the frequency of the detected pitch
    :param threshold: The multiple of the highest peak the new peak must be greater than.
    :param maxfreq: the maximum frequency detectable, in hz
    :return: the corrected pitch, in hz

    Adapted from https://github.com/ad1269/Monophonic-Pitch-Detection
    '''
    period = 1/note * sr  # converts the note back in the period (in samples)
    minperiod = sr // maxfreq
    autocorrArgMax = autocorr.argmax()  # this is the same as the period found above
    print('note', note, 'period', period, 'argmax', autocorrArgMax)
    print(minperiod)
    maxMultiplier = int(round(period // minperiod, 0))
    print('maxmul', maxMultiplier)
    for multiplier in range(maxMultiplier, 1-1, -1):
        for mul in range(1, multiplier):
            tempPeriod = int(round(mul * period/multiplier, 0))
            print(multiplier, mul, tempPeriod)
            if autocorr[tempPeriod] < threshold * autocorr[autocorrArgMax]:
                break
        else:  # for loop was not broken
            return note * multiplier
    raise Exception('no note was found')  # something went wrong


def fixOctave2(autocorr, note, sr, thresholdF, maxfreq=4000):
    '''
    :param autocorr: Autocorrelation of the waveform to detect pitch over
    :param note: The previously estimated pitch, in hz
    :param sr: Sampling rate of the waveform, in hz
    :param thresholdF: A function that will yeild a threshold(see previous) given a distance in hz between the
    note (param note) estimate and the current guess. Threshold should probably be >= 0 unless you want some
    really strange stuff to happen
    :param maxfreq: The maximum frequency detectable
    :return: An octave corrected pitch

    Adapted from https://github.com/ad1269/Monophonic-Pitch-Detection, with the exception of the threshold function
    '''
    period = 1/note * sr  # converts the note back in the period (in samples)
    minperiod = sr // maxfreq
    autocorrArgMax = autocorr.argmax()  # this is the same as the period found above
    maxMultiplier = int(round(period // minperiod, 0))
    for multiplier in range(maxMultiplier, 1-1, -1):
        for mul in range(1, multiplier):
            tempPeriod = int(round(mul * period/multiplier, 0))
            if autocorr[tempPeriod] < thresholdF(note, sr/tempPeriod) * autocorr[autocorrArgMax]:
                break
        else:  # for loop was not broken
            return note * multiplier
    raise Exception('no note was found')  # something went wrong

def autocorrelate(y, n=2):
    '''
    :param y: waveform to be autocorrelated (numpy array)
    :param n: the number of times to perform an autocorrelation. Higher value deals with noise better
    :return: the nth autocorrelation of y (numpy array)
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


'''
Some sample threshold functions to be used for fix octave 2

For all functions below:
:param note: origonal estimated note
:param guess: current guess
:return: a multiplier

ideas to implement:
something based on pachelbel's canon chord progression
a sine wave (ineffective, but amusing)
use a log scale for threshold, so lower frequencies require less energy
'''


def simpleinverse(note, guess):
    '''
    :return: multiplier (0, 1)
    '''
    distance = guess-note
    scale = 350
    return 1 - 1 / ((abs(distance)-scale)/scale)


def fancy(note, guess):
    mults = {2, .95,  # major second
             7, .75,  # perfect fifth
             5, .20}  # perfect second
    distance = abs(librosa.core.hz_to_midi(guess) - librosa.core.hz_to_midi(note))


def exp(note, guess):
    '''
    :return: multiplier [0, 1)
    '''
    return 1 - 2**(-.005 * guess)


def log(note, guess):
    '''
    this one seems to work best at the moment
    :return: multiplier (0, oo)
    '''
    a = 30
    return math.log((guess+a)/a, 10)
