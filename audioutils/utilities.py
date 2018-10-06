'''
General utilities to help with stuff, not related to pitch
'''
GAIN_TO_CUT_IN_HALF = -6  # gain used to halve amplitude


def sum_stereo_to_mono(left, right):
    '''
    take two waveforms and sum them together, accounting for duplication of center panned audio
    :param left: left channel waveform
    :param right: right channel waveform
    :return: merged waveform
    '''
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
    return left_gain.overlay(right_gain).overlay(all_but_center)
