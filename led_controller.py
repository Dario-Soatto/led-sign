import serial
import time

PORT = "COM3"

# ============================================
# COORDINATES
# ============================================

INPUT_RIGHT = 220
INPUT_DOWN = 220

SEND_RIGHT = 330
SEND_DOWN = 380

OK_RIGHT = 220
OK_DOWN = 225

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
    
    print(f"📺 Sending: {message}")
    
    # 1. Go to corner
    pico.write(b"CORNER\n")
    pico.readline()
    time.sleep(0.3)
    
    # 2. Move to input field
    move_incremental(pico, INPUT_RIGHT, INPUT_DOWN)
    time.sleep(0.2)
    
    # 3. Click input field
    pico.write(b"CLICK\n")
    pico.readline()
    time.sleep(0.3)
    
    # 4. Select all (Ctrl+A)
    pico.write(b"HOTKEY,CTRL,A\n")
    pico.readline()
    time.sleep(0.2)
    
    # 5. Type message (escape newlines for Pico)
    escaped_message = message.replace("\n", "{ENTER}")
    pico.write(f"TYPE,{escaped_message}\n".encode())
    pico.readline()
    time.sleep(0.3)
    
    # 6. Move to send button
    pico.write(b"CORNER\n")
    pico.readline()
    move_incremental(pico, SEND_RIGHT, SEND_DOWN)
    time.sleep(0.2)
    
    # 7. Click send button
    pico.write(b"CLICK\n")
    pico.readline()
    time.sleep(0.5)
    
    # 8. Move to OK button
    pico.write(b"CORNER\n")
    pico.readline()
    move_incremental(pico, OK_RIGHT, OK_DOWN)
    time.sleep(0.2)
    
    # 9. Click OK button
    pico.write(b"CLICK\n")
    pico.readline()
    time.sleep(0.3)
    
    print("✅ Sent!")
    
    pico.close()


if __name__ == "__main__":
    send_to_led("Test Message")