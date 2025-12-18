#Requires AutoHotkey v2.0

MsgBox "Click OK. Will try PostMessage click."

Sleep 1000

; Find the LED window
hwnd := WinExist("Plus")
if (!hwnd) {
    MsgBox "Window not found!"
    ExitApp
}

WinActivate hwnd
Sleep 500

; Get window position
WinGetPos &winX, &winY, &winW, &winH, hwnd

; Calculate click position relative to window
clickX := 500 - winX
clickY := 470 - winY

; Pack coordinates into lParam
lParam := (clickY << 16) | (clickX & 0xFFFF)

; Send mouse messages directly to window
PostMessage 0x201, 0, lParam, , hwnd  ; WM_LBUTTONDOWN
Sleep 50
PostMessage 0x202, 0, lParam, , hwnd  ; WM_LBUTTONUP

MsgBox "PostMessage sent! Check if input field is now focused."