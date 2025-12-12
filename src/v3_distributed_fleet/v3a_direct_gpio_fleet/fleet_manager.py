# File: fleet_manager.py (Phase 3A - Dual Direct Drive)
# Orchestrates two Picos (ARM_1 and ARM_2) simultaneously.
import serial
import time
import glob

def find_fleet():
    """Scans USB ports to find both ARM_1 and ARM_2"""
    fleet = {}
    ports = glob.glob('/dev/ttyACM*')
    print(f"Scanning USB ports: {ports}")
    
    for port in ports:
        try:
            s = serial.Serial(port, 115200, timeout=2)
            time.sleep(2) # Wait for Pico reboot
            s.reset_input_buffer()
            
            # Handshake
            s.write(b"WHO_ARE_YOU\n")
            s.flush()
            response = s.readline().decode().strip()
            
            if "ARM_1" in response:
                print(f"Found ARM_1 at {port}")
                fleet['ARM_1'] = s
            elif "ARM_2" in response:
                print(f"Found ARM_2 at {port}")
                fleet['ARM_2'] = s
            else:
                s.close()
        except:
            pass
    return fleet

# --- MAIN MISSION ---
print(">>> LAUNCHING PHASE 3A: DUAL ARM DIRECT DRIVE <<<")
robots = find_fleet()

if 'ARM_1' in robots and 'ARM_2' in robots:
    arm1 = robots['ARM_1']
    arm2 = robots['ARM_2']
    print("\n[SUCCESS] Both Arms Online. Starting Synchronized Test.")
    time.sleep(1)

    # Sequence: Move Arm 1, then Arm 2, then Both
    print("1. Moving Arm 1 Base...")
    arm1.write(b"MOVE_BASE_FWD\n")
    time.sleep(1.0)
    arm1.write(b"STOP\n")

    print("2. Moving Arm 2 Base...")
    arm2.write(b"MOVE_BASE_BACK\n")
    time.sleep(1.0)
    arm2.write(b"STOP\n")
    
    print("3. Moving BOTH (Multitasking)...")
    arm1.write(b"MOVE_SHOULDER_FWD\n")
    arm2.write(b"MOVE_SHOULDER_FWD\n")
    time.sleep(1.0)
    
    print("4. Stopping Fleet.")
    arm1.write(b"STOP\n")
    arm2.write(b"STOP\n")
    
    arm1.close()
    arm2.close()
    print("Mission Complete.")

else:
    print(f"[FAIL] Incomplete Fleet. Found: {list(robots.keys())}")
