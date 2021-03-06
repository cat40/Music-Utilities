LYFLAT = 'is'
LYSHARP = 'es'
SHARP = '#'
FLAT = 'b'
VALIDACCIDENTALS = (LYFLAT, LYSHARP)
VALIDNOTENAMESNOACCIDENTALS = list('abcdefg')
VALIDNOTENAMES = tuple(' '.join(' '.join([s, s+LYFLAT, s+LYSHARP]) for s in VALIDNOTENAMESNOACCIDENTALS).split())
STRNOTEDURATIONS = {'\\breve' : -1, '\\longa' : -2}
VALIDNOTEDURATIONS = tuple(' '.join(' '.join([str(s), str(s)+'.', str(s)+'..']) for s in (2**x for x in range(7+1))).split()) + \
                     tuple(' '.join(' '.join([s, s+'.', s+'..']) for s in STRNOTEDURATIONS.keys()).split())

# Note: these names are current from the LilyPond 2.19.81 documentation accessed 4/27/2018
MidiNamesRaw = '''acoustic grand            contrabass           lead 7 (fifths)
bright acoustic           tremolo strings      lead 8 (bass+lead)
electric grand            pizzicato strings    pad 1 (new age)
honky-tonk                orchestral harp      pad 2 (warm)
electric piano 1          timpani              pad 3 (polysynth)
electric piano 2          string ensemble 1    pad 4 (choir)
harpsichord               string ensemble 2    pad 5 (bowed)
clav                      synthstrings 1       pad 6 (metallic)
celesta                   synthstrings 2       pad 7 (halo)
glockenspiel              choir aahs           pad 8 (sweep)
music box                 voice oohs           fx 1 (rain)
vibraphone                synth voice          fx 2 (soundtrack)
marimba                   orchestra hit        fx 3 (crystal)
xylophone                 trumpet              fx 4 (atmosphere)
tubular bells             trombone             fx 5 (brightness)
dulcimer                  tuba                 fx 6 (goblins)
drawbar organ             muted trumpet        fx 7 (echoes)
percussive organ          french horn          fx 8 (sci-fi)
rock organ                brass section        sitar
church organ              synthbrass 1         banjo
reed organ                synthbrass 2         shamisen
accordion                 soprano sax          koto
harmonica                 alto sax             kalimba
concertina                tenor sax            bagpipe
acoustic guitar (nylon)   baritone sax         fiddle
acoustic guitar (steel)   oboe                 shanai
electric guitar (jazz)    english horn         tinkle bell
electric guitar (clean)   bassoon              agogo
electric guitar (muted)   clarinet             steel drums
overdriven guitar         piccolo              woodblock
distorted guitar          flute                taiko drum
guitar harmonics          recorder             melodic tom
acoustic bass             pan flute            synth drum
electric bass (finger)    blown bottle         reverse cymbal
electric bass (pick)      shakuhachi           guitar fret noise
fretless bass             whistle              breath noise
slap bass 1               ocarina              seashore
slap bass 2               lead 1 (square)      bird tweet
synth bass 1              lead 2 (sawtooth)    telephone ring
synth bass 2              lead 3 (calliope)    helicopter
violin                    lead 4 (chiff)       applause
viola                     lead 5 (charang)     gunshot
cello                     lead 6 (voice)'''


MIDINAMES = [st for st in (s.rstrip(' ') for s in (line[x:y] for x, y in zip((0, 26, 26+21), (26, 26+21, None))
                                                   for line in MidiNamesRaw.split('\n'))) if st]
MIDINUMBERS = dict(zip(range(1, len(MIDINAMES)+1), MIDINAMES))
