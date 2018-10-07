'''
General utilities to help with stuff, not related to pitch
'''
GAIN_TO_CUT_IN_HALF = -6  # gain used to halve amplitude


def sum_stereo_to_mono(left, right):
    '''
    take two waveforms and sum them together, accounting for duplication of center panned audio
    todo: make a genric form that takes an arbitrary number of channels
    :param left: left channel waveform
    :param right: right channel waveform
    :return: merged waveform
    '''

    # invert the right channel
    right_inverted = -1 * right

    # combine right and left, to eliminate center
    all_but_center = (left + right) * 0.5

    # halve the waveform of right and left channels to offset gain doubling of this algorithm
    left_gain = left * 0.5
    right_gain = right * 0.5

    # combine with original right and left channels
    # this will double everything but the center, to offset the center being doubled by the L+R sum
    # general volume should be twice the original volume
    return left_gain + right_gain + all_but_center
