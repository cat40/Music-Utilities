'''
module for instrument-specific data

instrument parameters
    range (adustable during song to get better results)
    how to get onsets (percussive/harmonic, what octaves to look in, etc)
todo impliment soft and hard range bounds (right now all are hard)
todo make the note interface more friendly for use without familiarity with midi notes
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
        # static variables
        self.usePercussive = tk.BooleanVar()
        self.usePercussiveButton = tk.Checkbutton(self.window, text="Use Percussive Onsets", variable=self.usePercussive,
                                                   onvalue=True, offvalue=False)
        self.usePercussiveButton.select()
        self.useHarmonic = tk.BooleanVar()
        self.useHarmonicButton = tk.Checkbutton(self.window, text="Use Harmonic Onsets", variable=self.useHarmonic,
                                                   onvalue=True, offvalue=False)
        self.useHarmonicButton.select()
        # dynamic variables
        self.lowerRangeBound = tk.IntVar()  # midi number
        self.lowerRangeSlider = tk.Scale(self.window, orient=tk.HORIZONTAL, from_=0, to=127,
                                         label='Lower range bound', length=250, variable=self.lowerRangeBound)
        self.lowerRangeBox = tk.Spinbox(self.window, variable=self.lowerRangeBound)
        self.upperRangeBound = tk.IntVar()  # midi number
        self.upperRangeSlider = tk.Scale(self.window, orient=tk.HORIZONTAL, from_=0, to=127,
                                         label='Lower range bound', length=250, variable=self.upperRangeBound)
        self.upperRangeBox = tk.Spinbox(self.window, variable=self.upperRangeBound)

    def displayInputs(self):
        self.lowerRangeSlider.pack()
        self.lowerRangeBox.pack()
        self.upperRangeBox.pack()
        self.upperRangeSlider.pack()
