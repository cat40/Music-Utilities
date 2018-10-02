from pydub import AudioSegment

audiofile = '.\\tests\\Brothers Unite.mp3'
stereo_wave = AudioSegment.from_file(audiofile, format='mp3')
left, right = stereo_wave.split_to_mono()

# invert the right channel
right_inverted = right.invert_phase()

# combine right and left, to eliminat center
all_but_center = left.overlay(right_inverted)

# combine with original right and left channels
# this will double everything but the center, to offset the center being doubled by the L+R sum
# general volume should be twice the original volume
result = left.overlay(right).overlay(all_but_center)

#Export merged audio file
result.export('.\\tests\\results\\stereo_to_mono.wav', format='wav')
