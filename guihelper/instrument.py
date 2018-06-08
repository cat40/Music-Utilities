'''
module for instrument-specific data

instrument parameters
    range (adustable during song to get better results)
    how to get onsets (percussive/harmonic, what octaves to look in, etc)
todo impliment soft and hard range bounds (right now all are hard)
'''
import tkinter as tk

globalid = 0


class Instrument(object):
    def __init__(self, window, name):
        global globalid
        self.id = globalid
        globalid += 1
        self.window = window
        self.name = name
        self.lowerRangeBound = tk.IntVar()  # midi number
        self.lowerRangeSlider = tk.Scale(self.window, orient=tk.HORIZONTAL, from_=0, to=10,
                                         label='Lower range bound', length=250, variable=self.lowerRangeBound)
        self.lowerRangeBox = tk.Spinbox(self.window, variable=self.lowerRangeBound)

    def displayInputs(self):
        pass
