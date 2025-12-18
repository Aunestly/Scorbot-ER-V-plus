# File: fleet_manager.py (If you want to run this code save this on your Raspberry Pi 4 Desktop)
# ROLE: THE BRAIN (Commander), instead of using a laptop or desktop, if you choose, this code it is only for 
# the Rasberry Pi 4, with two Rasberry Pi Picos connected to the USB.
# remove print messages with debug code if you don't want to see status messages.
# If new picos are being used, they will also need to be programmed to take commands from the Pi 4 in order for
# this code to even run. Make sure to run main.py for both arms before running this code.

import serial
import time
import glob

def find_robots():
    """
    Scans all USB serial ports and asks connected devices for their ID.
    Returns a dictionary: {'ARM_1': serial_connection, 'ARM_2': serial_connection}
    """
    robots = {}
    # Find all USB serial devices (usually /dev/ttyACM0, ACM1, etc.)
    ports = glob.glob('/dev/ttyACM*')
    
    print(f"Scanning USB ports: {ports}...")
    
    for port in ports:
        try:
            # Connect to the port
            print(f"Connecting to {port}...", end="")
            s = serial.Serial(port, 115200, timeout=2)
            time.sleep(2) # Wait for the connection to stabilize
            
            # Clear any old data
            s.reset_input_buffer()
            
            # Ask the Pico: "Who are you?"
            s.write(b"WHO_ARE_YOU\n")
            s.flush()
            
            # Listen for the answer (Pico should reply "ARM_1" or "ARM_2")
            response = s.readline().decode('utf-8').strip()
            print(f" Identity: {response}")
            
            if response == "ARM_1":
                robots['ARM_1'] = s
            elif response == "ARM_2":
                robots['ARM_2'] = s
            else:
                print(f"  -> Warning: Unknown device response: '{response}'")
                s.close()
                
        except Exception as e:
            print(f"\n  -> Error on {port}: {e}")
            
    return robots

# --- MAIN MISSION SEQUENCE ---
print(">>> INITIALIZING ROBOT FLEET <<<")
fleet = find_robots()

# Check if we found both arms
if 'ARM_1' in fleet and 'ARM_2' in fleet:
    print("\n--- FLEET READY: BOTH ARMS ONLINE ---")
    arm1 = fleet['ARM_1']
    arm2 = fleet['ARM_2']
    
    # --- MISSION 1: Visual Check ---
    print("\n[Mission 1] Signaling Arm 1 (Bottom Port)...")
    arm1.write(b"BLINK\n")
    time.sleep(1) # Wait for blink to finish
    
    print("[Mission 1] Signaling Arm 2 (Top Port)...")
    arm2.write(b"BLINK\n")
    time.sleep(1)
    
    print("\n>>> Mission Complete. Fleet Standing By.")
    
    # Clean up connections
    arm1.close()
    arm2.close()
    
elif 'ARM_1' in fleet:
    print("\n--- PARTIAL FLEET: ONLY ARM 1 FOUND ---")
    fleet['ARM_1'].write(b"BLINK\n")
    fleet['ARM_1'].close()

elif 'ARM_2' in fleet:
    print("\n--- PARTIAL FLEET: ONLY ARM 2 FOUND ---")
    fleet['ARM_2'].write(b"BLINK\n")
    fleet['ARM_2'].close()

else:
    print("\n[ERROR] No robots found! Check USB cables.")
