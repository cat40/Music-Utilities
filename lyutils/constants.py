LYFLAT = 'is'
LYSHARP = 'es'
SHARP = '#'
FLAT = 'b'
VALIDNOTENAMESNOACCIDENTALS = list('abcdefg')
VALIDNOTENAMES = tuple(' '.join(' '.join([s, s+LYFLAT, s+LYSHARP]) for s in VALIDNOTENAMESNOACCIDENTALS).split())
VALIDNOTEDURATIONS = tuple(' '.join(' '.join([str(s), str(s)+'.', str(s)+'..']) for s in (2**x for x in range(7+1))).split()) + \
                     tuple(' '.join(' '.join([s, s+'.', s+'..']) for s in ('\\longa', '\\breve')).split())
