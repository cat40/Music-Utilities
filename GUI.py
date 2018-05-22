'''
File for the GUI of the program


plan:
Allow dynamic changing of the sliders while the song is playing to account for things like changing tempo and key
Boxes for instruments, with some way to change the number (slider
    Should have user savable presets

Song parameters:
    tempo
    key
    time signature

instrument parameters
    range (adustable during song to get better results)
    how to get onsets (percussive/harmonic, what octaves to look in, etc)

todo:
fixed values should grey out once the start button is pressed
'''
import time
import tkinter as tk

MAXFPS = 60
PERIOD = 1/MAXFPS

window = tk.Tk()
window.protocol('WM_DELETE_WINDOW', window.destroy)  # doesn't seem to work at the moment


def newScale(init=0, **kwargs):
    scale = tk.Scale(window, **kwargs)
    scale.set(init)
    scale.pack()
    return scale


numInstruments = newScale(init=1, orient=tk.HORIZONTAL, from_=1, to=15)  # cannot be changed during execution

# window.mainloop()
prevt = time.clock()
while True:
    if time.clock() - prevt < PERIOD:
        continue
    window.update()
    print(numInstruments.get())
    prevt = time.clock()


'''
references:
Scale.get() -> get value
Scale.set() -> set value

possible scale variables:
IntVar, DoubleVar, StringVar
'''