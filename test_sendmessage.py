import time
import win32gui
import win32con
import win32api

print("Finding window at screen coordinates...")

# Get window handle at specific screen position
hwnd_at_point = win32gui.WindowFromPoint((500, 470))
print(f"Window at (500, 470): {hwnd_at_point}")
print(f"Title: {win32gui.GetWindowText(hwnd_at_point)}")
print(f"Class: {win32gui.GetClassName(hwnd_at_point)}")

# Get parent window
parent = win32gui.GetParent(hwnd_at_point)
print(f"Parent: {parent} - {win32gui.GetWindowText(parent) if parent else 'None'}")

input("\nPress Enter to send click to this specific window...")

# Send click to the window at that point
lParam = 0  # Click at 0,0 of that control
win32gui.SendMessage(hwnd_at_point, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
time.sleep(0.05)
win32gui.SendMessage(hwnd_at_point, win32con.WM_LBUTTONUP, 0, lParam)

print("Sent! Did it work?")