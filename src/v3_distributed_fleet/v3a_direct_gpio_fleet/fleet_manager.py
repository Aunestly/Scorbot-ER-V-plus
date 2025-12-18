# fleet_manager.py
# Run this on the Raspberry Pi 4
import serial
import time
import glob

def find_robots():
    robots = {}
    ports = glob.glob('/dev/ttyACM*')
    print(f"Scanning USB ports: {ports}...")
    
    for port in ports:
        try:
            # Connect to port
            s = serial.Serial(port, 115200, timeout=2)
            time.sleep(2) # Wait for Pico to reboot
            s.reset_input_buffer()
            
            # HANDSHAKE (The Standard Command)
            s.write(b"IDENTIFY\n")
            time.sleep(0.1)
            
            # Robust Check (Read 5 lines to skip boot messages)
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
                    
        except Exception as e:
            print(f" -> Error on {port}: {e}")
            
    return robots

# --- MAIN EXECUTION ---
print(">>> INITIALIZING FLEET <<<")
fleet = find_robots()

if 'ARM_1' in fleet and 'ARM_2' in fleet:
    print("\n--- FLEET READY: ALL SYSTEMS GO ---")
    arm1 = fleet['ARM_1']
    arm2 = fleet['ARM_2']
    
    # ==========================================
    # MISSION 1: ARM 1 BASE SHAKE (Validation)
    # ==========================================
    print("\n[MISSION 1] Testing Arm 1 Base...")
    arm1.write(b"MOVE_BASE_FWD\n")
    time.sleep(1.0)
    arm1.write(b"STOP\n")
    time.sleep(0.2)
    
    arm1.write(b"MOVE_BASE_BACK\n")
    time.sleep(1.0)
    arm1.write(b"STOP\n")
    print(" -> Arm 1 Test Complete.")
    
    # ==========================================
    # MISSION 2: ARM 2 COMPLEX 4-CYCLE
    # ==========================================
    print("\n[MISSION 2] Starting Arm 2 Production Cycle...")
    LOOPS = 4
    
    for i in range(LOOPS):
        print(f" -> Cycle {i+1}/{LOOPS}")
        
        # 1. Base Turn
        arm2.write(b"MOVE_BASE_FWD\n")
        time.sleep(2.0)
        arm2.write(b"HOLD_BASE\n") 
        time.sleep(0.5)
        
        # 2. Extend
        arm2.write(b"EXTEND_ARM\n")
        time.sleep(1.5)
        arm2.write(b"HOLD_ARM\n")
        time.sleep(0.5)
        
        # 3. Grip
        arm2.write(b"GRIPPER_CLOSE\n")
        time.sleep(1.0)
        arm2.write(b"HOLD_GRIPPER\n")
        
        # 4. Return Home (Simultaneous)
        arm2.write(b"MOVE_BASE_BACK\n")
        arm2.write(b"RETRACT_ARM\n")
        time.sleep(1.5) # Wait for arm
        arm2.write(b"HOLD_ARM\n")
        time.sleep(0.5) # Wait for base
        arm2.write(b"HOLD_BASE\n")
        
        # 5. Release
        arm2.write(b"GRIPPER_OPEN\n")
        time.sleep(1.0)
        arm2.write(b"HOLD_GRIPPER\n")
        time.sleep(1.0)

    print("\n>>> ALL MISSIONS COMPLETE.")
    arm1.write(b"STOP\n")
    arm2.write(b"STOP_ALL\n")
    arm1.close()
    arm2.close()

else:
    print("\n[ERROR] Fleet Incomplete. Check connections.")
    print(f"Found: {list(fleet.keys())}")
