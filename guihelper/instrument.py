'''
module for instrument-specific data

instrument parameters
    range (adustable during song to get better results)
    how to get onsets (percussive/harmonic, what octaves to look in, etc)
todo impliment soft and hard range bounds (right now all are hard)
todo make the note interface more friendly for use without familiarity with midi notes
todo put the ranges on one scale instead of one for each bound
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
        self.useOctaves = tk.BooleanVar()
        self.useOctavesButton = tk.Checkbutton(self.window, text="Use Octave-splitting onset detection",
                                               variable=self.useOctaves, onvalue=True, offvalue=False)
        self.useOctavesButton.select()
        self.octaveUpperBound = tk.IntVar()
        self.octaveUpperBoundSlider = tk.Scale(self.window, orient=tk.HORIZONTAL, from_=0, to=8,
                                               label='Upper Octave Bound', length=250, variable=self.octaveUpperBound)
        self.octaveUpperBoundBox = tk.Spinbox(self.window, variable=self.octaveUpperBound)
        self.octaveLowerBound = tk.IntVar()
        self.octaveLowerBoundSlider = tk.Scale(self.window, orient=tk.HORIZONTAL, from_=0, to=8,
                                               label='Lower Octave Bound', length=250, variable=self.octaveLowerBound)
        self.octaveLowerBoundBox = tk.Spinbox(self.window, variable=self.octaveLowerBound)
        self.staticVariables = [self.usePercussive, self.useHarmonic, self.useOctaves,
                        self.octaveUpperBound, self.octaveLowerBound]
        self.staticInputs = [self.usePercussiveButton, self.useOctavesButton, self.useHarmonicButton,
                             self.octaveUpperBoundSlider, self.octaveUpperBoundBox,
                             self.octaveLowerBoundSlider, self.octaveLowerBoundBox]
        # dynamic variables
        self.lowerRangeBound = tk.IntVar()  # midi number
        self.lowerRangeSlider = tk.Scale(self.window, orient=tk.HORIZONTAL, from_=0, to=127,
                                         label='Lower range bound', length=250, variable=self.lowerRangeBound)
        self.lowerRangeBox = tk.Spinbox(self.window, variable=self.lowerRangeBound)
        self.upperRangeBound = tk.IntVar()  # midi number
        self.upperRangeSlider = tk.Scale(self.window, orient=tk.HORIZONTAL, from_=0, to=127,
                                         label='Lower range bound', length=250, variable=self.upperRangeBound)
        self.upperRangeBox = tk.Spinbox(self.window, variable=self.upperRangeBound)
        self.dynamicVariables = [self.lowerRangeBound, self.upperRangeBound]
        self.dynamicInputs = [self.lowerRangeBox, self.lowerRangeSlider, self.upperRangeSlider, self.upperRangeBox]

    def displayInputs(self):
        # static variables
        self.useHarmonicButton.pack()
        self.usePercussiveButton.pack()
        self.useOctavesButton.pack()
        self.octaveLowerBoundBox.pack()
        self.octaveLowerBoundSlider.pack()
        self.octaveUpperBoundBox.pack()
        self.octaveUpperBoundSlider.pack()
        # dynamic variables
        self.lowerRangeSlider.pack()
        self.lowerRangeBox.pack()
        self.upperRangeBox.pack()
        self.upperRangeSlider.pack()

    def readDynamicValues(self):
        pass

    def readStaticValues(self):
        '''
        reads the static values
        Inputs are disabled once read
        :return: None
        '''
        self.disableStaticVariables()

    def disableStaticVariables(self):
        for inpt in self.staticInputs:
            inpt.config(state='disabled')

    def enableStaticVariables(self):
        for inpt in self.staticInputs:
            inpt.config(state='enabled')
