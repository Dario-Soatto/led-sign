import serial
import time

PORT = "COM3"

INPUT_X = 500
INPUT_Y = 470

pico = serial.Serial(PORT, 115200, timeout=2)
time.sleep(2)

print("1. Moving to corner...")
pico.write(b"CORNER\n")
pico.readline()
time.sleep(1)

# Move in increments of 10 pixels for speed, but still incremental
print(f"2. Moving to ({INPUT_X}, {INPUT_Y})...")

# First move X
for x in range(0, INPUT_X + 1, 1):
    pico.write(f"MOVETO,{x},0\n".encode())
    pico.readline()

# Then move Y  
for y in range(0, INPUT_Y + 1, 1):
    pico.write(f"MOVETO,{INPUT_X},{y}\n".encode())
    pico.readline()

time.sleep(0.2)

print("3. Clicking...")
pico.write(b"CLICK\n")
print(pico.readline().decode().strip())

print("\n✅ Did it click the LED app's input field?")

pico.close()