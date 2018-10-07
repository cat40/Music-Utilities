'''
miscellaneous functions to help with manual testing
'''
import matplotlib.pyplot as plot
from scipy.io import wavfile

from audioutils import sum_stereo_to_mono


def plot_spectogram_from_file(fname):
    '''
    takes a wave file and displays it's spectogram
    :param fname: path to the wave file
    :return: None, display spectogram
    '''
    samplingrate, signal = wavfile.read(fname)
    # check for a stereo file and convert to mono
    assert len(signal.shape) <= 2  # if not, something really weird happened
    if len(signal.shape) == 2:
        signal = sum_stereo_to_mono(signal[:,0], signal[:,1])
    print(signal)
    plot_spectogram(signal, samplingrate)


def plot_wavform(waveform):
    '''
    plot the waveform of a signal
    :param waveform: numpy array of the signal
    :return: None, display waveform plot
    '''
    plot.title('Waveform')
    plot.plot(waveform)
    plot.xlabel('Sample')
    plot.ylabel('Amplitude')


def plot_spectogram(waveform, samplingrate):
    '''
    make and display a spectogram of a signal
    :param waveform: numpy array of the signal
    :param samplingrate: sampling rate of the signal
    :return:
    '''
    plot.title('Spectogram')
    plot.specgram(waveform, Fs=samplingrate)
    plot.xlabel('Time')
    plot.ylabel('Frequency')
    plot.show()


# run the tests
if __name__ == '__main__':
    plot_spectogram_from_file('.\\testsp\\Isle-of-Innisfree.wav')
