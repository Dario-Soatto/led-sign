import time
import win32api
import win32con

print("=" * 40)
print("WIN32 API CLICK TEST")
print("=" * 40)
print("\nMake sure the LED app is open (can be in background).")
print("Clicking at (500, 470) in 3 seconds...")
print()

for i in range(3, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

print("\nMoving cursor...")
win32api.SetCursorPos((300, 300))
time.sleep(0.2)

print("Clicking...")
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 500, 470, 0, 0)
time.sleep(0.05)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 500, 470, 0, 0)

print("\nDone! Did the LED app respond?")