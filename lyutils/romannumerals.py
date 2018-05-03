from collections import OrderedDict

numerals = {
    1 : 'I',
    5 : 'V',
    10 : 'X',
    50 : 'L',
    100 : 'C',
    500 : 'D',
    1000 : 'M'
}

numerals = OrderedDict(sorted(numerals.items(), key=lambda x : x[0]))


# todo impliment subtraction rules (9=IX), etc
def romannumerals(i):
    string = ''
    for key, value in reversed(numerals.items()):
        count = i//key
        string += value * count
        i -= key*count
    return string


if __name__ == '__main__':
    for x in range(1500):
        print(x, romannumerals(x))