\version "2.18.2"
acousticgrandI = \relative c' {
c''4 d''2 e'4 f'2 g''4 a''2 b'4 c''2 b'4 a''2 g''2 f'4 e'4 d''2 c''2 }
acousticgrandIPart = \new Staff \with {
instrumentName = "acoustic grand1"
midiInstrument = "acoustic grand"
}\acousticgrandI

\score {
<<
\acousticgrandIPart
>>
\layout {}
\midi {}
}