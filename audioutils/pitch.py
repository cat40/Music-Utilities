import copy
import math
import sys

import librosa
import numpy
from numpy import pi, polymul
from scipy.signal import bilinear
from scipy import signal

'''
A collection of static methods for dealing with pitch


octave fixing ideas:
use multiple methods and take a vote (possibly weighted by method accuracy?)
todo analyze the spetographs of signals who's octaves are detected correclty and incorrectly and look for differences
    also look for a pattern in the note names
'''


# todo: make a single pitch function with a method argument


def getPitch(y, sr):
    '''
    :param y: the waveform to run pitch detection on
    :param sr: the sampling rate of the waveform
    :return: the estimated frequency of the waveform, in hz
    '''
    autocorr = normalized_autocorrelate(y, sr)
    estimate = pitchFromAC(autocorr, sr, autocorrelated=True)
    # estimate = getPitchCheap(y, sr, depth=1)
    # if the pitch is withing frequency bounds - the interval (20hz, 4000hz)
    if 20 < estimate < 4000:  # todo make min and max frequencies keyword arguments
        return fixOctave4(autocorr, estimate, sr)
        # return fixOctave3(y, sr, estimate)
        # return fixOctave2(autocorr, estimate, sr, log)
    return 0


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
    This is an increadibly terrible method
    '''
    y = copy.deepcopy(y)
    # filt = cls.helper_butter(sr, fmin, fmax) # todo make this work (has a nyqulist error)
    # y = signal.sosfiltfilt(filt, y)
    for _ in range(depth):
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        i = numpy.unravel_index(magnitudes.argmax(),
                                magnitudes.shape)  # unravel_index transforms the bizzare integer returned by argmax into a tuple index
        pitch = pitches[i]
        # break out of function before applying filters for no reason
        if _ == depth - 1:
            return pitch
        # now look just at the waveform in the section of the predicted pitch and looks for the pitch again to refine the guess
        radius = .25
        fmax = pitch * (1 + radius)
        fmin = pitch * (1 - radius)
        filt = helper_butter(sr, fmin, fmax)
        y = signal.sosfiltfilt(filt, y)


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
    # remove the components of the autocorrelation outside of min and max frequencies
    autocorrelation[:int(imin)] = 0
    autocorrelation[int(imax):] = 0
    timeShift = autocorrelation.argmax()  # find the maximum of the autocorrelation
    print('timeshift', timeShift)
    if not timeShift:
        return 0
    return sr / timeShift  # converts the period to a frequenct (timeShift is the number of samples,
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
    period = 1 / note * sr  # converts the note back in the period (in samples)
    minperiod = sr // maxfreq
    autocorrArgMax = autocorr.argmax()  # this is the same as the period found above
    print('note', note, 'period', period, 'argmax', autocorrArgMax)
    print(minperiod)
    maxMultiplier = int(round(period // minperiod, 0))
    print('maxmul', maxMultiplier)
    for multiplier in range(maxMultiplier, 1 - 1, -1):
        for mul in range(1, multiplier):
            tempPeriod = int(round(mul * period / multiplier, 0))
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
    period = 1 / note * sr  # converts the note back in the period (in samples)
    minperiod = sr // maxfreq
    autocorrArgMax = autocorr.argmax()  # this is the same as the period found above
    maxMultiplier = int(round(period // minperiod, 0))
    for multiplier in range(maxMultiplier, 1 - 1, -1):
        for mul in range(1, multiplier):
            tempPeriod = int(round(mul * period / multiplier, 0))
            if autocorr[tempPeriod] < thresholdF(note, sr / tempPeriod) * autocorr[autocorrArgMax]:
                break
        else:  # for loop was not broken
            return note * multiplier
    raise Exception('no note was found')  # something went wrong


def fixOctave3(y, sr, guess, threshold=0.2):
    '''
    Octave correction using HPS, as described here:
        http://musicweb.ucsd.edu/~trsmyth/analysis/Harmonic_Product_Spectrum.html
    For the moment, only works with a guess from getPitchCheap() due to array indexing problems (the estimate must be in the pitch array from librosa.piptrack())

    process:
        Get 2nd harmonic of guess (possibly the -2nd harmonic, half the frequnecy)
        if the amplitude of the 2nd harmonic is about half the amplitude of the chosen pitch, and the ratio is above
        and arbitray threshold (0.2?), choose the lower octave
        May have issues since most octave errors result in the octave being too low...
    TODO: make the index checking find the closest value, not just an exact match
    :param y: the waveform to determine the pitch over
    :param sr: sampling rate of the waveform
    :param guess: Initial guess at pitch
    :return: a modified guess with the octave (hopefully) corrected, in hertz
    '''
    # To correct, apply this rule: if the second peak amplitude below initially chosent pitch is approximately 1/2 of
    # the chosen pitch AND the ratio of amplitudes is above a threshold (e.g., 0.2 for 5 harmonics),
    # THEN select the lower octave peak as the pitch for the current frame.
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    print('pitches.py.fixOctave3: guess =', guess)
    print('pitches.py.fixOctave3: pitches =', numpy.any(numpy.count_nonzero(pitches, )))
    indexOfGuess = get_index_of_closest_value(pitches, guess)
    print('pitches.py.fixOctave3: pitch =', pitches[indexOfGuess])
    print('pitches.py.fixOctave3: index of guess =', indexOfGuess)
    magnitudeOfGuess = magnitudes[indexOfGuess]
    indexOfGuess2ndHarmonic = get_index_of_closest_value(pitches, guess/2)  # get the index of half the frequency of the guess
    magnitudeOfSecondHarmonic = magnitudes[indexOfGuess2ndHarmonic]
    print('pitches.py.fixOctave3: magnitude of guess =', magnitudeOfGuess)
    if abs(magnitudeOfGuess - magnitudeOfSecondHarmonic*2) >= 5 and magnitudeOfGuess/magnitudeOfSecondHarmonic > threshold:
        return guess/2
    return guess


def fixOctave4(autocorr, estimate, sr, minfreq = 20, maxfreq = 4000):
    '''
    A fairly simple algorithm written by Gerald Beauregard, converted to python from
    https://gerrybeauregard.wordpress.com/2013/07/15/high-accuracy-monophonic-pitch-estimation-using-normalized-autocorrelation/
    Licensed under MIT License:
    Copyright (c) 2009 Gerald T Beauregard
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
    documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
    THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    --------------------------------------------------------------------------------------------------------------------
    :param autocorr:
    :param estimate:
    :param sr:
    :param minfreq:
    :param maxfreq:
    :return:
    '''
    minimumPeriod = int(sr // (maxfreq - 1))
    maximumPeriod = int(sr // (minfreq + 1))
    estimatePeriod = int(sr // estimate)  # todo this won't work, need to convert frequency back to period first...
    subMultipleThreshold = 0.9  # if the strength at all submultiples of the peak position, assume the submultiple is the actual period
    maximumMultiple = int(estimatePeriod // minimumPeriod)
    estimatePeriod = estimatePeriod
    print(maximumMultiple)
    for submultiple in range(maximumMultiple, 0, -1):
        submultiplesAreStrong = True
        for subsubmultiple in range(1, submultiple):
            subsubmultiple_period = int(subsubmultiple * estimatePeriod // submultiple + 0.5)
            if autocorr[subsubmultiple_period] < subMultipleThreshold * autocorr[estimatePeriod]:
                submultiplesAreStrong = False
                break
        if submultiplesAreStrong:
            estimatePeriod = estimatePeriod // submultiple
            break
    return sr / estimatePeriod


def get_index_of_closest_value(array : numpy.ndarray, value):
    '''
    finds the closest value to a specified target in an array
    Mostly from https://stackoverflow.com/a/2566508
    :param array: The array to be searched
    :param value: The value to be searched for
    :return: The index of the closest value that exists in the array
    '''
    indexOfClosestValue = (numpy.abs(array - value)).argmin()
    return indexOfClosestValue


def get_closest_value(array : numpy.ndarray, value):
    '''
    finds the closest value to a specified target in an array
    Mostly from https://stackoverflow.com/a/2566508
    :param array: The array to be searched
    :param value: The value to be searched for
    :return: The closest value that exists in the array
    '''
    return array[get_index_of_closest_value(array, value)]


def autocorrelate(y, n=2):
    '''
    :param y: waveform to be autocorrelated (numpy array)
    :param n: the number of times to perform an autocorrelation. Higher value deals with noise better
    :return: the nth autocorrelation of y (numpy array)
    adapted from https://dsp.stackexchange.com/a/388
    '''
    prevAutocorr = numpy.fft.rfft(y)
    for _ in range(n):
        prevAutocorr = prevAutocorr * numpy.conj(prevAutocorr)
    return numpy.fft.irfft(prevAutocorr)


def normalized_autocorrelate(y, sr):
    '''
    The normalized autocorrellation of a signal. Adapted from code presented in
    https://gerrybeauregard.wordpress.com/2013/07/15/high-accuracy-monophonic-pitch-estimation-using-normalized-autocorrelation/
    Licensed under MIT License
    :param y: waveform to be autocorrelated
    :param sr: sampling rate of waveform to be autocorrelated
    :return: The normalized autocorrelation of the waveform (numpy array)
    '''
    minimumPeriod = sr // 4000
    maximumPeriod = sr // 20
    nac = numpy.zeros(y.shape)
    for period in range(minimumPeriod-1, maximumPeriod+2):
        autocorrAtPeriod = 0
        sumOfSquaresBeginning = 0
        sumOfSquaresEnd = 0
        for i in range(len(y) - period):
            autocorrAtPeriod += y[i]*y[i+period]
            sumOfSquaresBeginning += y[i]**2
            sumOfSquaresEnd += y[i+period]**2
        nac[period] = autocorrAtPeriod / math.sqrt(sumOfSquaresEnd * sumOfSquaresBeginning)
    return nac


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
    distance = guess - note
    scale = 350
    return 1 - 1 / ((abs(distance) - scale) / scale)


def fancy(note, guess):
    mults = {2, .95,  # major second
             7, .75,  # perfect fifth
             5, .20}  # perfect second
    distance = abs(librosa.core.hz_to_midi(guess) - librosa.core.hz_to_midi(note))


def exp(note, guess):
    '''
    :return: multiplier [0, 1)
    '''
    return 1 - 2 ** (-.005 * guess)


def log(note, guess):
    '''
    this one seems to work best at the moment
    sometimes goes a bit too low
    :return: multiplier (0, oo)
    '''
    a = 30
    return math.log((guess + a) / a, 10)


def SPA(autocorr, note, sr, ):
    '''
    :param autocorr:
    :param note:
    :param sr:
    :return:
    An implementation of Spectrum Peak Analysis as described in High Accuracy and Octave Error Immune Pitch
    Detection Algorithms by M. Dziubinski and B. Kostek

    todo: adjust M so that M*d <= Ha
    '''
    M = 20  # the harmonic number of the original signal the note is assumed to be at
    fundamentals = [note / i for i in range(1, M + 1)]
    K = sr // M
    fundamentalMatrix = [[f * j for j in range(1, K + 1)] for f in fundamentals]
    pass  # not finished yet