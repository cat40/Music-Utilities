class lyObj(object):
    def __init__(self, hasbrackets, base, *entries):
        self.hasbrackets = hasbrackets
        self.base = base  # might not need this if child attributes are visible to the parent class
        self.entries = entries

    def __str__(self):
        product = self.base
        if self.hasbrackets: product += '\n{'
        else: product += ' '
        product += ' '.join(entries)
        if self.hasbrackets: product += '\n}'
        return product

    def __add__(self, other):
        if isinstance(other, str):
            self.entries.append(other)
        else:
            self.entries += other


class Key(lyObj):
    modes = {'major' : '\\major', 'minor' : '\\minor'}
    def __init__(self, note, mode):
        super().__init__(False, r'\key')
        super().entries += [note, self.modes[mode]]


class Time(lyObj):
    def __init__(self, n, d):
        super().__init__(False, r'\time')
        super().entries.append('%s/%s' % (n, d))


class Clef(lyObj):
    def __init__(self, clef):
        super().__init__(False, r'\clef')
        super().entries.append('\\'+clef)

'''
class lyObj(object):
    def __init__(self):
        raise IdiotError "abstract class, you idiot!"
        assert 2+2==5

    def combine(self):
        return self.base + self.data

class IdiotError(ZeroDivisionError):
    pass
'''
