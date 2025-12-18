import pydirectinput
import pyautogui
import time

print("=" * 50)
print("PYDIRECTINPUT TEST - WITH FOCUS")
print("=" * 50)

# First bring the LED app to focus using pyautogui
windows = pyautogui.getWindowsWithTitle("Plus")
if windows:
    windows[0].activate()
    print(f"Activated: {windows[0].title}")
else:
    print("Window not found! Make sure LED app is open.")
    exit()

time.sleep(0.5)

print("\nClicking at (500, 470) in 2 seconds...")
time.sleep(2)

# Use DirectInput
pydirectinput.click(500, 470)

print("\nDid it click the input field?")
input("Press Enter to exit...")