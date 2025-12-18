import serial
import time

PORT = "COM3"

# ============================================
# COORDINATES - Adjust these by trial and error
# ============================================

# Input field (from corner: move right, move down)
INPUT_RIGHT = 220   # pixels right from corner
INPUT_DOWN = 220    # pixels down from corner

# Send button (from corner: move right, move down)
SEND_RIGHT = 70    # pixels right from corner
SEND_DOWN = 100    # pixels down from corner

# OK button (from corner: move right, move down)
OK_RIGHT = 50      # pixels right from corner
OK_DOWN = 70       # pixels down from corner

# ============================================

def move_incremental(pico, dx, dy, step=10):
    """Move in increments of 'step' pixels."""
    x, y = 0, 0
    
    target_x = dx
    while x != target_x:
        if x < target_x:
            x = min(x + step, target_x)
        else:
            x = max(x - step, target_x)
        pico.write(f"MOVETO,{x},{y}\n".encode())
        pico.readline()
    
    target_y = dy
    while y != target_y:
        if y < target_y:
            y = min(y + step, target_y)
        else:
            y = max(y - step, target_y)
        pico.write(f"MOVETO,{x},{y}\n".encode())
        pico.readline()


def send_to_led(message):
    """Send a message to the LED sign."""
    
    pico = serial.Serial(PORT, 115200, timeout=2)
    time.sleep(2)
    
    print(f"\n📺 Sending: {message}\n")
    
    # 1. Go to corner
    print("STEP 1: Moving to corner...")
    pico.write(b"CORNER\n")
    pico.readline()
    input("  ✓ At corner. Press Enter to continue...")
    
    # 2. Move to input field
    print(f"\nSTEP 2: Moving to input field ({INPUT_RIGHT}, {INPUT_DOWN})...")
    move_incremental(pico, INPUT_RIGHT, INPUT_DOWN)
    input("  ✓ At input field. Press Enter to click, select all, and type...")
    
    # 3. Click input field
    print("\nSTEP 3: Clicking input field...")
    pico.write(b"CLICK\n")
    pico.readline()
    time.sleep(0.3)
    
    # 4. Select all
    print("STEP 4: Selecting all (Ctrl+A)...")
    pico.write(b"HOTKEY,CTRL,A\n")
    pico.readline()
    time.sleep(0.2)
    
    # 5. Type message
    print(f"STEP 5: Typing: {message}")
    pico.write(f"TYPE,{message}\n".encode())
    pico.readline()
    time.sleep(0.3)
    input("  ✓ Typed. Press Enter to move to send button...")
    
    # 6. Move to send button
    print(f"\nSTEP 6: Moving to corner, then to send button ({SEND_RIGHT}, {SEND_DOWN})...")
    pico.write(b"CORNER\n")
    pico.readline()
    move_incremental(pico, SEND_RIGHT, SEND_DOWN)
    input("  ✓ At send button. Press Enter to click...")
    
    # 7. Click send button
    print("\nSTEP 7: Clicking send button...")
    pico.write(b"CLICK\n")
    pico.readline()
    input("  ✓ Clicked. Press Enter to move to OK button...")
    
    # 8. Move to OK button
    print(f"\nSTEP 8: Moving to corner, then to OK button ({OK_RIGHT}, {OK_DOWN})...")
    pico.write(b"CORNER\n")
    pico.readline()
    move_incremental(pico, OK_RIGHT, OK_DOWN)
    input("  ✓ At OK button. Press Enter to click...")
    
    # 9. Click OK button
    print("\nSTEP 9: Clicking OK button...")
    pico.write(b"CLICK\n")
    pico.readline()
    
    print("\n  ✅ Done!")
    
    pico.close()


if __name__ == "__main__":
    print("=" * 50)
    print("LED SIGN CONTROLLER - STEP BY STEP")
    print("=" * 50)
    print("\n⚠️  Make sure LED app is OPEN and VISIBLE!")
    input("Press Enter when ready...")
    
    send_to_led("Test Message")
    
    print("\n✅ Check the LED sign!")