import serial
import time

# Replace COM3 with your actual port
PORT = "COM3"  # <-- CHANGE THIS

print(f"Connecting to Pico on {PORT}...")

try:
    pico = serial.Serial(PORT, 115200, timeout=2)
    time.sleep(2)  # Wait for connection
    print("Connected!")
    
    # Test ping
    print("\nTesting PING...")
    pico.write(b"PING\n")
    response = pico.readline().decode().strip()
    print(f"Response: {response}")
    
    if response == "PONG":
        print("✅ Pico is responding!")
        
        # Move to corner first (calibration)
        print("\nCalibrating - moving to corner...")
        pico.write(b"CORNER\n")
        print(pico.readline().decode().strip())
        time.sleep(1)
        
        # Move to a position
        print("\nMoving mouse to (500, 400)...")
        pico.write(b"MOVETO,500,400\n")
        print(pico.readline().decode().strip())
        
        print("\n✅ Test complete! Did your mouse move?")
    else:
        print("❌ Unexpected response")
        
    pico.close()
    
except serial.SerialException as e:
    print(f"❌ Error: {e}")
    print("\nMake sure:")
    print("1. The Pico is plugged in")
    print("2. You're using the correct COM port")
    print("3. No other program is using the port")