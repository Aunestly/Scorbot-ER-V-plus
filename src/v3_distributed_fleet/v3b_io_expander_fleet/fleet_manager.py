# File: fleet_manager.py (If you want to run this code save this on your Raspberry Pi 4 Desktop)
# ROLE: THE BRAIN (Commander), instead of using a laptop or desktop, if you choose, this code it is only for 
# the Rasberry Pi 4, with two Rasberry Pi Picos connected to the USB.
# remove print messages with debug code if you don't want to see status messages.
# If new picos are being used, they will also need to be programmed to take commands from the Pi 4 in order for
# this code to even run. Make sure to run main.py for both arms before running this code.

import serial
import time
import glob

print(">>> INITIALIZING SCORBOT FLEET <<<")

def find_robots():
    robots = {}
    # Scan for USB devices
    ports = glob.glob('/dev/ttyACM*')
    for port in ports:
        try:
            # Connect
            s = serial.Serial(port, 115200, timeout=2)
            time.sleep(2)
            s.reset_input_buffer()
            
            # Ask identity
            s.write(b"WHO_ARE_YOU\n")
            s.flush()
            
            # Read response
            for i in range(5): 
                line = s.readline().decode('utf-8').strip()
                if "ARM_1" in line: 
                    robots['ARM_1'] = s
                    break
                elif "ARM_2" in line: 
                    robots['ARM_2'] = s
                    break
        except: 
            pass
    return robots

# --- MAIN SEQUENCE ---
fleet = find_robots()

if 'ARM_1' in fleet and 'ARM_2' in fleet:
    print("\nSUCCESS: Both Arms Connected!")
    arm1 = fleet['ARM_1']
    arm2 = fleet['ARM_2']
    
    # --- GENTLE MOVEMENT TEST ---
    print("\n--- STARTING GENTLE TEST ---")
    
    print("1. RELAY CLICK (Arm 2)")
    arm2.write(b"RELAY_1_ON\n"); time.sleep(0.5)
    arm2.write(b"RELAY_1_OFF\n"); time.sleep(0.5)

    print("2. BASE WIGGLE (Both)")
    # Move Base Forward
    arm1.write(b"MOVE_BASE_FWD\n")
    arm2.write(b"MOVE_BASE_BACK\n")
    time.sleep(1.2) 
    arm1.write(b"STOP\n")
    arm2.write(b"STOP\n")
    time.sleep(0.5)
    
    print("3. GENTLE EXTEND (0.6s)")
    # Short burst out
    arm1.write(b"EXTEND_ARM\n")
    arm2.write(b"EXTEND_ARM\n")
    time.sleep(0.8) 
    arm1.write(b"STOP_ALL\n")
    arm2.write(b"STOP_ALL\n")
    time.sleep(0.5)
 

    print("4. RETURN HOME (0.6s)")
    # Bring it back
    arm1.write(b"RETRACT_ARM\n")
    arm2.write(b"RETRACT_ARM\n")
    time.sleep(0.8) 
    
    # IMPORTANT: Stop retracting before moving base!
    arm1.write(b"STOP_ALL\n")
    arm2.write(b"STOP_ALL\n")
    time.sleep(0.5) 
    
    print("5. RETURN BASE")
    # Move Base Back
    arm1.write(b"MOVE_BASE_BACK\n")
    arm2.write(b"MOVE_BASE_FWD\n")
    
    # IMPORTANT: Give it time to actually move!
    time.sleep(1.2) 
    
    arm1.write(b"STOP_ALL\n")
    arm2.write(b"STOP_ALL\n")

    print("\nTEST COMPLETE.")
    arm1.close()
    arm2.close()

else:
    print(f"ERROR: Only found {list(fleet.keys())}. Connect both arms!")
