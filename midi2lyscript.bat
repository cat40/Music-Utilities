@echo off
set inname=%1
set outname=%2

"C:\Program Files (x86)\LilyPond\usr\bin\python2.4.exe" "C:\Program Files (x86)\LilyPond\usr\bin\midi2ly.py" %inname% -o %outname%