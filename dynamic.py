'''
Module for handling the dynamic variables
'''


class Dynamic(object):
    def __init__(self, variable):
        self.variable = variable
        self.values = [variable.get()]

    def update(self):
        self.values.append(self.variable.get())
