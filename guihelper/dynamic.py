'''
Module for handling the dynamic variables
'''
import time

class Dynamic(object):
    def __init__(self, variable):
        self.variable = variable
        self.pairs = []
        self.init = time.clock()

    def update(self):
        self.pairs.append((time.clock() - self.init, self.variable.get()))

    @property
    def values(self):
        return [value for _, value in self.pairs]

    @property
    def times(self):
        return[t for t, _ in self.pairs]
