from .instrument import Instrument
class Music(object):
    '''
    arguments:
    @header is a dictionary of items that belong in the lilypond
    \header{} thing
    @globals is a list of lyObj that go in the global section
    '''
    def __init__(self, instruments, header=None, globalparts=None, midi=True, basenote=4):
        self.string = ''
        self.header = header if header is not None else {} # consider checking if the keys are valid, but that will be very hard to maintain as lilypond updates
                              # might actaully be able to import lilypond source code and use that to check if the keys are valid
        self.globalparts = globalparts if globalparts is not None else []
        # if a global base is better than local ones, impliment it here
        self.instruments = instruments if isinstance(instruments[0], Instrument) else [instrument.convert(basenote) for instrument in instruments]

    def __repr__(self):
        return 'Instrument object with %s instruments' % len(self.instruments) # todo: make this more descriptive

    def __str__(self):
        string = '\\version "2.18.2"\n'
        # header
        if self.header:
            string += 'header {\n'
            string += '\n'.join(key + ' = ' + '"'+value+'"' for key, value in self.header.items())
            string += '\n}'
        # globals
        if self.globalparts:
            string += 'global = {\n'
            string += '\n'.join(map(str, self.globalparts))
            string += '\n}'
        # instruments
        string += '\n\n'.join(map(str, self.instruments)) + '\n'
        # instrument staff blocks
        string += '\n\n'.join(instrument.staffblock() for instrument in self.instruments)
        # score block
        string += '\n\n\\score {\n<<\n'
        for instrument in self.instruments:
            string += '\\'+instrument.name+'\n'
        string += '>>\n\\layout {}\n\\midi {}\n}'
        return string

    def write(self, fname, mode='w'):
        with open(fname, mode) as f:
            f.write(str(self))
