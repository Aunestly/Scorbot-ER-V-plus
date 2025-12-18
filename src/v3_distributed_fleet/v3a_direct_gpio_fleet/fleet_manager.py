# File: fleet_manager.py (Run on Raspberry Pi 4)
import serial
import time
import glob

def find_robots():
    robots = {}
    ports = glob.glob('/dev/ttyACM*')
    print(f"Scanning USB ports: {ports}...")
    
    for port in ports:
        try:
            s = serial.Serial(port, 115200, timeout=2)
            time.sleep(2) 
            s.reset_input_buffer()
            
            # --- THE CORRECT HANDSHAKE YOU WANTED ---
            s.write(b"WHO_ARE_YOU\n")
            s.flush()
            
            # Read multiple lines to skip boot messages
            for i in range(5): 
                line = s.readline().decode('utf-8').strip()
                if "ARM_1" in line: 
                    robots['ARM_1'] = s
                    print(f" -> Found ARM_1 on {port}")
                    break
                elif "ARM_2" in line: 
                    robots['ARM_2'] = s
                    print(f" -> Found ARM_2 on {port}")
                    break
        except: 
            pass
    return robots

print(">>> INITIALIZING FLEET <<<")
fleet = find_robots()

if 'ARM_1' in fleet and 'ARM_2' in fleet:
    print("\n--- FLEET READY ---")
    arm1 = fleet['ARM_1']
    arm2 = fleet['ARM_2']
    
    # ==========================================
    # MISSION 1: ARM 1 BASE TEST (2 Cycles)
    # ==========================================
    print("\n[MISSION 1] Testing Arm 1 Base (2 Cycles)...")
    for i in range(2):
        print(f" > Cycle {i+1}: Forward")
        arm1.write(b"MOVE_BASE_FWD\n")
        time.sleep(2.0)
        arm1.write(b"STOP\n")
        time.sleep(0.5)
        
        print(f" > Cycle {i+1}: Backward")
        arm1.write(b"MOVE_BASE_BACK\n")
        time.sleep(2.0)
        arm1.write(b"STOP\n")
        time.sleep(0.5)
    
    print("[MISSION 1] Complete.")
    time.sleep(1.0)

    # ==========================================
    # MISSION 2: ARM 2 COMPLEX SEQUENCE
    # ==========================================
    print("\n[MISSION 2] Starting Arm 2 Task...")
    
    # 1. Base Forward + Hold
    print(" > Moving Base...")
    arm2.write(b"MOVE_BASE_FWD\n")
    time.sleep(2.0)
    arm2.write(b"HOLD_BASE\n")
    time.sleep(0.5)
    
    # 2. Extend Arm
    print(" > Extending...")
    arm2.write(b"EXTEND_ARM\n")
    time.sleep(1.5)
    arm2.write(b"HOLD_ARM\n")
    time.sleep(0.5)
    
    # 3. Grip
    print(" > Gripping...")
    arm2.write(b"GRIPPER_CLOSE\n")
    time.sleep(1.0)
    arm2.write(b"HOLD_GRIPPER\n")
    time.sleep(0.5)
    
    # 4. Return (Simultaneous)
    print(" > Returning...")
    arm2.write(b"MOVE_BASE_BACK\n")
    arm2.write(b"RETRACT_ARM\n")
    time.sleep(1.5) # Arm travel time
    arm2.write(b"HOLD_ARM\n")
    time.sleep(0.5) # Remaining base travel
    arm2.write(b"HOLD_BASE\n")
    
    # 5. Release
    print(" > Releasing...")
    arm2.write(b"GRIPPER_OPEN\n")
    time.sleep(1.0)
    arm2.write(b"HOLD_GRIPPER\n")

    print("\n>>> ALL MISSIONS COMPLETE.")
    arm1.write(b"STOP\n")
    arm2.write(b"STOP_ALL\n")
    arm1.close()
    arm2.close()

else:
    print("ERROR: Did not find both arms. Check USB cables.")
