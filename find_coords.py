import pyautogui
import time

print("=" * 50)
print("COORDINATE TRACKER")
print("=" * 50)
print("Move your mouse around to see coordinates.")
print("Press Ctrl+C in this terminal to stop.")
print("=" * 50)
print()

try:
    while True:
        x, y = pyautogui.position()
        print(f"\rX: {x:4d}  Y: {y:4d}  ", end="", flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\nStopped!")