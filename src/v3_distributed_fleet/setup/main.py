# File: main.py on Pico W
# ROLE: SPINAL CORD (Listener)
# This code must be ran on BOTH ARMS (BOTH PICOS, if your using two) before starting any of the version fleet_manager codes. 
# This code enables the picos to listen to the Pi 4, and take commands from it.
# It should be saved as main.py, but main.py will change once you enable the pico
# to take commands from the pi, by running this code.


from machine import Pin
import time
import sys # Necessary for reading USB commands
import select # Helps check if data is waiting

# --- [INSERT YOUR MOTOR CLASS HERE] ---
# (Paste your existing Motor class and expander setup here)
# ...

# --- Motor Setup ---
base = Motor("Base", 14, 13, 16, 17) 
# (Define your other motors here too: shoulder, elbow, etc.)

# --- Main Listener Loop ---
print("READY_FOR_COMMANDS") # Signal to the Pi 4 that we are alive

while True:
    # Check if data is available on the USB serial port (stdin)
    if select.select([sys.stdin], [], [], 0)[0]:
        # Read the line of text sent by the Pi 4
        command = sys.stdin.readline().strip()
        
        # --- PARSE COMMANDS ---
        if command == "MOVE_BASE_FWD":
            base.forward()
            print("ACK: Base Moving Forward") # Send reply to Pi 4
            
        elif command == "MOVE_BASE_BACK":
            base.backward()
            print("ACK: Base Moving Backward")
            
        elif command == "STOP_ALL":
            base.stop()
            # shoulder.stop()
            # elbow.stop()
            print("ACK: Stopped")
            
        else:
            print(f"ERROR: Unknown command '{command}'")
            
    # Small sleep to prevent CPU hogging
    time.sleep(0.01)
