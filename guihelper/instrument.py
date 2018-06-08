'''
module for instrument-specific data
'''
globalid = 0


class Instrument(object):
    def __init__(self, window, name):
        global globalid
        self.id = globalid
        globalid += 1
        self.window = window
        self.name = name
