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
import sys
import time
import tkinter as tk
import tkinter.filedialog
import vlc

from dynamic import Dynamic

MAXFPS = 60
PERIOD = 1/MAXFPS


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
    music.play()


# isPaused = False
# def pause():
#     global isPaused
#     if isPaused:
#         music.play()
#     else:
#         music.pause()
#     isPaused = not isPaused

def pause():
    music.pause()


def savePreset():
    pass


def loadPreset():
    pass


def openMusicFile():
    global music
    fname = tk.filedialog.askopenfile()
    if fname is not None:  # user did not press the cancel button
        music = vlc.MediaPlayer(fname)


def goByBy():
    window.destroy()
    sys.exit()


window = tk.Tk()
window.protocol('WM_DELETE_WINDOW', goByBy)  # doesn't seem to work at the moment
window.geometry('400x400')

mainmenu = tk.Menu(window)
filemenu = tk.Menu(mainmenu, tearoff=0)
filemenu.add_command(label='Save Preset')
filemenu.add_command(label='Open Preset')
filemenu.add_command(label='Open Music File', command=openMusicFile)
mainmenu.add_cascade(label='File', menu=filemenu)

window.config(menu=mainmenu)


# static values
numInstruments = newScale(init=1, label='Number of Instruments', orient=tk.HORIZONTAL, from_=1, to=15, length=250)  # cannot be changed during execution

startButton = tk.Button(window, text='Start', command=start)
playButton = tk.Button(window, text='Play Music', command=play)
pauseButton = tk.Button(window, text='Pause/Play Music', command=pause)
startButton.pack()
playButton.pack()
pauseButton.pack()

# dynamic values
# global
tempo = tk.IntVar()
tempoSlide = newScale(60, orient=tk.HORIZONTAL, from_=0, to=300, label='Tempo', length=250, variable=tempo)
tempoBox = tk.Spinbox(window, from_=0, to=300, wrap=False, textvariable=tempo)
tempoBox.pack()
key = tk.Spinbox(window, values=('C', 'D', 'E', 'F', 'G', 'A', 'B'), wrap=True)
key.pack()

variables = [Dynamic(tempo), Dynamic(key)]


def updateVariables():
    for var in variables:
        var.update()


while True:
    window.update()

'''
references:
Scale.get() -> get value
Scale.set() -> set value

possible scale variables:
IntVar, DoubleVar, StringVar
'''