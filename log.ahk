; Script to monitor Alt+R and Alt+Z keypresses

; Monitor all other keypresses
~*PrintScreen::  ; Example to capture PrintScreen
key := "PrintScreen"
LogKey(key)
return

LogKey(key) {
    FormatTime, time,, yyyy-MM-dd HH:mm:ss
    FileAppend, %time% - %key% pressed`n, C:\keylog.txt
}

; Log Alt+R and Alt+Z attempts
~!r::
LogKey("Alt + R")
return

~!z::
LogKey("Alt + Z")
return
