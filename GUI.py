'''
File for the GUI of the program


plan:
Allow dynamic changing of the sliders while the song is playing to account for things like changing tempo and key
Boxes for instruments, with some way to change the number (slider
    Should have user savable presets

Song parameters:
    tempo
    key (should be a slicder with the circle of fifths, and a checkbox for minor (or a menu for mode)
    time signature

instrument parameters
    range (adustable during song to get better results)
    how to get onsets (percussive/harmonic, what octaves to look in, etc)

todo:
fixed values should grey out once the start button is pressed
create a data structure to store the value of each button and the time it changed (or just the value of the buttons)
    for every n frames of the audio
make a class for instruments
'''
import time
import tkinter as tk
from pygame import mixer

MAXFPS = 60
PERIOD = 1/MAXFPS

window = tk.Tk()
window.protocol('WM_DELETE_WINDOW', window.destroy)  # doesn't seem to work at the moment


def newScale(init=0, **kwargs):
    scale = tk.Scale(window, **kwargs)
    scale.set(init)
    scale.pack()
    return scale


def start():
    # window.mainloop()
    prevt = time.clock()
    while True:
        if time.clock() - prevt < PERIOD:
            continue
        window.update()
        print(numInstruments.get())
        prevt = time.clock()


def play():
    prevPauseState = False
    fname = fileBox.get()
    music = mixer.Sound(fname)
    music.play()
    while True:
        window.update()
        # todo get values form all the buttons and thingies
        if not mixer.get_busy():  # music is done playing
            return  # todo put stuff into the data structure here
        if prevPauseState != isPaused:
            if isPaused:
                mixer.pause()
            else:
                mixer.unpause()
        prevPauseState = isPaused


isPaused = False
def pause():
    global isPaused
    isPaused = not isPaused


def savePreset():
    pass

def loadPreset():
    pass

def openMusicFile():
    pass


mixer.init()

mainmenu = tk.Menu(window)
filemenu = tk.Menu(mainmenu, tearoff=0)
filemenu.add_command(label='Save Preset')
filemenu.add_command(label='Open Preset')
filemenu.add_command(label='Open Music File')
mainmenu.add_cascade(label='File', menu=filemenu)

window.config(menu=mainmenu)


# static values
numInstruments = newScale(init=1, orient=tk.HORIZONTAL, from_=1, to=15)  # cannot be changed during execution

startButton = tk.Button(window, text='Start', command=start)
playButton = tk.Button(window, text='Play Music', command=play)
pauseButton = tk.Button(window, text='Pause/Play Music', command=pause)
startButton.pack()
playButton.pack()
pauseButton.pack()

# dynamic values
# global
tempo = newScale(60, orient=tk.HORIZONTAL, from_=0, to=300, label='Tempo')
key = tk.Spinbox(window, values=('C', 'D', 'E', 'F', 'G', 'A', 'B'), wrap=True)
key.pack()


while True:
    window.update()

'''
references:
Scale.get() -> get value
Scale.set() -> set value

possible scale variables:
IntVar, DoubleVar, StringVar
'''