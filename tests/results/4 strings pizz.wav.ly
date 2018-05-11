\version "2.18.2"
violaII = \relative c' {
cis'''64 c''1 g''1 d''1 a''1 f'2 }
violaIIPart = \new Staff \with {
instrumentName = "viola2"
midiInstrument = "viola"
}\violaII

\score {
<<
\violaIIPart
>>
\layout {}
\midi {}
}