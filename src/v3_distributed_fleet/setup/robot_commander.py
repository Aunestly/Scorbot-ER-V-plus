# File: robot_commander.py (Save on Raspberry Pi 4)
# ROLE: BRAIN (Commander)
# SAVE THIS CODE ON YOUR PI 4, under LOCAL Python 3
# run this code so that the Pi 4 can now command the pico's to listen.

import serial
import time

# --- Setup Serial Connection ---
# '/dev/ttyACM0' is the standard address for a Pico plugged into a Pi
try:
    pico = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    time.sleep(2) # Wait for connection to settle
    print("Connected to Pico!")
except:
    print("Could not connect. Check USB cable.")
    exit()

def send_command(cmd):
    # Add a newline character (\n) so the Pico knows the command is finished
    command_string = cmd + "\n"
    pico.write(command_string.encode('utf-8')) # Send binary data
    
    # Listen for the Pico's reply
    response = pico.readline().decode('utf-8').strip()
    print(f"Pico replied: {response}")

# --- Mission Sequence ---
try:
    print(">>> Mission Start: Moving Base")
    
    # 1. Tell Pico to move base
    send_command("MOVE_BASE_FWD")
    
    # 2. The BRAIN decides how long to wait (Time control is now here!)
    time.sleep(2.0) 
    
    # 3. Tell Pico to stop
    send_command("STOP_ALL")
    
    print(">>> Mission Complete")

finally:
    # Always ensure we stop
    send_command("STOP_ALL")
    pico.close()
