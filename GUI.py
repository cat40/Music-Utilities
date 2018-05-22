'''
File for the GUI of the program
'''
import time
import tkinter as tk

window = tk.Tk()

scaleVariable = tk.IntVar()
scale = tk.Scale(window,
                 orient=tk.HORIZONTAL)
scale.set(50)
scale.pack()

window.mainloop()

'''
references:
Scale.get() -> get value
Scale.set() -> set value

possible scale variables:
IntVar, DoubleVar, StringVar
'''