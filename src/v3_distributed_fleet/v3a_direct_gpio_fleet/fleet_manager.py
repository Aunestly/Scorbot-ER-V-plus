# Role: Commander
# fleet_manager.py (on Pi 4)

import serial
import time
import glob

def find_robots():
    # Scans all usb serial ports and asks connected devices for IDs
    # Returns dictionary
    robots = {}
    ports = glob.glob('/dev/ttyACM*')
    print(f"Scanning USB ports: {ports}...")
    
    for port in ports:
        try:
            print(f"Connecting to {port}...", end="")
            s = serial.Serial(port, 115200, timeout=2)
            time.sleep(2) 
            
            s.reset_input_buffer()
            s.write(b"WHO_ARE_YOU\n")
            s.flush()
            
            # --- READ LOOP TO IGNORE ECHO ---
            found_id = None
            for i in range(5):
                line = s.readline().decode('utf-8').strip()
                # Ignore empty lines or the echo of the command itself
                if line == "" or line == "WHO_ARE_YOU":
                    continue
                if "ARM_1" in line:
                    found_id = "ARM_1"
                    break
                elif "ARM_2" in line:
                    found_id = "ARM_2"
                    break
            # -------------------------------

            print(f" Identity: {found_id}")
            
            if found_id == "ARM_1":
                robots['ARM_1'] = s
            elif found_id == "ARM_2":
                robots['ARM_2'] = s
            else:
                print(f"  -> Warning: No valid ID found.")
                s.close()
                
        except Exception as e:
            print(f"\n  -> Error on {port}: {e}")
            
    return robots

#main mission sequence
print(">>>Initializing robot fleet")
fleet = find_robots()

#check if we found both arms
# Check if we found both arms
if 'ARM_1' in fleet and 'ARM_2' in fleet:
    print("\n--- FLEET READY: BOTH ARMS ONLINE ---")
    arm1 = fleet['ARM_1']
    arm2 = fleet['ARM_2']
    
    # --- SKIPPING ARM 1 (Save for later) ---
    print("[Mission] Skipping Arm 1 (Maintenance Mode)...")
    # arm1.write(b"MOVE_BASE_FWD\n") 
    # time.sleep(2.0)
    # arm1.write(b"STOP\n")
    
    # --- MISSION: MOVE ARM 2 ---
    print("\n[Mission] Commanding Arm 2 (Direct GPIO)...")
    
    # 1. Move Base Forward
    print(">>> Arm 2: Moving Base Forward")
    arm2.write(b"MOVE_BASE_FWD\n")
    time.sleep(3.0)
    
    # 2. Stop
    print(">>> Arm 2: Stopping")
    arm2.write(b"STOP\n")
    time.sleep(0.5)
    
    # 3. Move Base Backward
    print(">>> Arm 2: Moving Base Backward")
    arm2.write(b"MOVE_BASE_BACK\n")
    time.sleep(3.0)
    
    # 4. Final Stop
    print(">>> Arm 2: Stopping")
    arm2.write(b"STOP\n")
    
    print("\n>>> Mission Complete.")
    
    # Clean up connections
    arm1.close()
    arm2.close()
    
elif 'ARM_1' in fleet:
    print("\n-- PARTIAL FLEET: ONLY ARM 1 FOUND...")
    fleet['ARM_1'].write(b"BLINK\n")
    fleet['ARM_1'].close()
elif 'ARM_2' in fleet:
    print("\n--- PARTIAL FLEET: ONLY ARM 2 FOUND ---")
    arm2 = fleet['ARM_2']
    
    # --- CONFIGURATION ---
    LOOPS = 4
    BASE_TIME = 2.0
    ARM_TIME = 1.2
    GRIP_TIME = 0.8
    
    print(f"Starting {LOOPS}-Cycle Sequence...")
    time.sleep(2)
    
    for i in range(LOOPS):
        print(f"\n=== CYCLE {i+1} of {LOOPS} ===")
        
        # 1. BASE TURN
        print(">>> 1. Base Turning...")
        arm2.write(b"MOVE_BASE_FWD\n")
        time.sleep(BASE_TIME)
        arm2.write(b"HOLD_BASE\n") 
        time.sleep(0.5)
        
        # 2. EXTEND ARM
        print(">>> 2. Extending Arm...")
        arm2.write(b"EXTEND_ARM\n")
        time.sleep(ARM_TIME)
        arm2.write(b"HOLD_ARM\n")
        time.sleep(0.5)
        
        # 3. GRIP
        print(">>> 3. Closing Gripper...")
        arm2.write(b"GRIPPER_CLOSE\n")
        time.sleep(GRIP_TIME)
        arm2.write(b"HOLD_GRIPPER\n")
        time.sleep(0.5)
        
        # 4. SIMULTANEOUS RETURN
        print(">>> 4. Returning Home (Simultaneous)...")
        arm2.write(b"MOVE_BASE_BACK\n")
        arm2.write(b"RETRACT_ARM\n")
        
        time.sleep(ARM_TIME)
        arm2.write(b"HOLD_ARM\n") 
        
        remaining = BASE_TIME - ARM_TIME
        if remaining > 0:
            time.sleep(remaining)
        
        arm2.write(b"HOLD_BASE\n")
        time.sleep(0.5)
        
        # 5. RELEASE
        print(">>> 5. Releasing...")
        arm2.write(b"GRIPPER_OPEN\n")
        time.sleep(GRIP_TIME)
        arm2.write(b"HOLD_GRIPPER\n")
        time.sleep(1.0) 

    print("\n>>> Sequence Complete. Shutting down.")
    arm2.write(b"STOP_ALL\n") 
    arm2.close()

else:
    print("\n[ERROR] No robots found! Check USB Cables.")

