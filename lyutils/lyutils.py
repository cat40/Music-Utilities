from .lyObjs import *
class lyutils(object):
    '''
    arguments:
    @header is a dictionary of items that belong in the lilypond
    \header{} thing
    @globals is a list of lyObj that go in the global section
    '''
    def __init__(self, header={}, globals=[]):
        self.string = ''
        self.header = header  # consider checking if the keys are valid, but that will be very hard to maintain as lilypond updates
                              # might actaully be able to import lilypond source code and use that to check if the keys are valid
        self.globals = globals


    def __add__(self, other):
        if isinstance(other, lyObj):
