# File: fleet_manager.py (Run on Raspberry Pi 4)
# Mission: Arm 1 Base Warmup -> Arm 2 Complex Task

import serial
import time
import glob

def find_robots():
    """ Scans ports and identifies robots by ID """
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
            
            # Read loop to ignore echo
            found_id = None
            for i in range(5):
                line = s.readline().decode('utf-8').strip()
                if line == "" or line == "WHO_ARE_YOU": continue
                if "ARM_1" in line: found_id = "ARM_1"; break
                elif "ARM_2" in line: found_id = "ARM_2"; break

            print(f" Identity: {found_id}")
            
            if found_id:
                robots[found_id] = s
            else:
                s.close()
        except Exception as e:
            print(f" Error: {e}")
            
    return robots

# --- MAIN MISSION ---
print(">>> INITIALIZING FLEET <<<")
fleet = find_robots()

if 'ARM_1' in fleet and 'ARM_2' in fleet:
    print("\n--- FLEET READY ---")
    arm1 = fleet['ARM_1']
    arm2 = fleet['ARM_2']
    
    # ==================================================
    # PHASE 1: ARM 1 (Base Cycles)
    # ==================================================
    print("\n[PHASE 1] Starting Arm 1 Base Cycles...")
    
    # Loop 2 times as requested
    for i in range(2):
        print(f"   >>> Arm 1 Cycle {i+1}/2")
        
        # Move Forward
        arm1.write(b"MOVE_BASE_FWD\n")
        time.sleep(2.0)
        
        # Stop briefly
        arm1.write(b"STOP\n")
        time.sleep(0.5)
        
        # Move Backward
        arm1.write(b"MOVE_BASE_BACK\n")
        time.sleep(2.0)
        
        # Stop
        arm1.write(b"STOP\n")
        time.sleep(0.5)
        
    print("[PHASE 1] Arm 1 Complete. Switching to Arm 2...")
    time.sleep(1.0)

    # ==================================================
    # PHASE 2: ARM 2 (Complex Sequence)
    # ==================================================
    print("\n[PHASE 2] Starting Arm 2 Sequence...")
    
    # Configuration for Arm 2 sequence
    LOOPS = 2
    BASE_TIME = 2.0
    ARM_TIME = 1.2
    GRIP_TIME = 0.8
    
    for i in range(LOOPS):
        print(f"\n   >>> Arm 2 Cycle {i+1}/{LOOPS}")
        
        # 1. Base Forward + Hold
        arm2.write(b"MOVE_BASE_FWD\n")
        time.sleep(BASE_TIME)
        arm2.write(b"HOLD_BASE\n")
        time.sleep(0.5)
        
        # 2. Extend Arm
        arm2.write(b"EXTEND_ARM\n")
        time.sleep(ARM_TIME)
        arm2.write(b"HOLD_ARM\n")
        time.sleep(0.5)
        
        # 3. Grip
        arm2.write(b"GRIPPER_CLOSE\n")
        time.sleep(GRIP_TIME)
        arm2.write(b"HOLD_GRIPPER\n")
        time.sleep(0.5)
        
        # 4. Simultaneous Return (The cool part!)
        print("      (Simultaneous Return...)")
        arm2.write(b"MOVE_BASE_BACK\n")
        arm2.write(b"RETRACT_ARM\n")
        
        # Wait for Arm (shorter) then stop it
        time.sleep(ARM_TIME)
        arm2.write(b"HOLD_ARM\n")
        
        # Wait for Base (longer) then stop it
        remaining = BASE_TIME - ARM_TIME
        if remaining > 0:
            time.sleep(remaining)
        arm2.write(b"HOLD_BASE\n")
        time.sleep(0.5)
        
        # 5. Release
        arm2.write(b"GRIPPER_OPEN\n")
        time.sleep(GRIP_TIME)
        arm2.write(b"HOLD_GRIPPER\n")
        time.sleep(1.0)

    # ==================================================
    # SHUTDOWN
    # ==================================================
    print("\n>>> ALL MISSIONS COMPLETE.")
    arm1.write(b"STOP\n")
    arm2.write(b"STOP_ALL\n") # Ensures Arm 2 cuts brake power
    
    arm1.close()
    arm2.close()

else:
    print("\n[ERROR] Did not find both arms.")
    print(f"Found: {list(fleet.keys())}")

