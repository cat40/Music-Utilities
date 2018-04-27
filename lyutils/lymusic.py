from .lyObjs import *
class lyutils(object):
    '''
    arguments:
    @header is a dictionary of items that belong in the lilypond
    \header{} thing
    @globals is a list of lyObj that go in the global section
    '''
    def __init__(self, instruments, header={}, globals=[], midi=True):
        self.string = ''
        self.header = header  # consider checking if the keys are valid, but that will be very hard to maintain as lilypond updates
                              # might actaully be able to import lilypond source code and use that to check if the keys are valid
        self.globals = globals
        self.instruments = instruments

    def __str__(self):
        string = '\\version "2.18.2"'
        if self.header:
            string += '\\header {\n'
            string += '\n'.join(key + ' = ' + '"'+value+'"' for key, value in self.header.items())
            string += '\n}'
        if self.globals:
            string += '\\global = {\n'
            string += '\n'.join(self.globals)
            string += '\n}'
        string += '\n\n'.join(self.instruments)

        return string
