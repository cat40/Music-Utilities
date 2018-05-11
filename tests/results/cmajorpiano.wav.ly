\version "2.18.2"
acousticgrandI = \relative c' {
c''4 d''4 e'4 f'4 g''4 a''4 b'4 c''4 b'4 a''4 g''4 f'4 e'4 d''4 c''2 }
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