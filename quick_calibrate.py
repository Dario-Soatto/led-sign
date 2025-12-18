import serial
import time

PORT = "COM3"

pico = serial.Serial(PORT, 115200, timeout=2)
time.sleep(2)

print("Moving to corner...")
pico.write(b"CORNER\n")
pico.readline()
time.sleep(1)
print("Cursor should be at top-left")

input("Press Enter to move 100 pixels right...")

# Move right 100 pixels (the version that worked)
for i in range(100):
    pico.write(f"MOVETO,{i+1},0\n".encode())
    pico.readline()
    time.sleep(0.01)

print("Done! Clicking...")
pico.write(b"CLICK\n")
print(pico.readline().decode().strip())

print("\n✅ Did mouse move and click?")

pico.close()