\version "2.18.2"

global = {
  \key c \major
  \time 4/4
}

viola = \relative c {
  \global
  c2 d e f g a b c b a g f e d c
  
}

\score {
  \new Staff \with {
    instrumentName = "Viola"
    midiInstrument = "acoustic grand"
  } { \clef alto \viola }
  \layout { }
  \midi {
    \tempo 2=60
  }
}
