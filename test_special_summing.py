from pydub import AudioSegment

GAIN_TO_CUT_IN_HALF = -6  # gain used to halve amplitude

audiofile = '.\\tests\\Brothers Unite.mp3'
stereo_wave = AudioSegment.from_file(audiofile, format='mp3')
left, right = stereo_wave.split_to_mono()

# invert the right channel
right_inverted = right.invert_phase()

# combine right and left, to eliminat center
all_but_center = left.overlay(right_inverted).apply_gain(GAIN_TO_CUT_IN_HALF)

# halve the waveform of right and left channels to offset gain doubling of this algorithm
left_gain = left.apply_gain(GAIN_TO_CUT_IN_HALF)
right_gain = right.apply_gain(GAIN_TO_CUT_IN_HALF)

# combine with original right and left channels
# this will double everything but the center, to offset the center being doubled by the L+R sum
# general volume should be twice the original volume
result = left_gain.overlay(right_gain).overlay(all_but_center)

# Export merged audio file
result.export('.\\tests\\results\\stereo_to_mono.wav', format='wav')
