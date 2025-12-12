# File: fleet_manager.py (Phase 3A - Direct Drive Prototype)
import serial
import time
import glob

def find_robot_port():
    """Scans USB ports to find a Pico responding as ARM_1"""
    ports = glob.glob('/dev/ttyACM*')
    print(f"Scanning ports: {ports}")
    
    for port in ports:
        try:
            s = serial.Serial(port, 115200, timeout=2)
            time.sleep(2) # Wait for Pico to reboot/ready
            s.reset_input_buffer()
            
            # The Handshake
            print(f"Pinging {port}...")
            s.write(b"WHO_ARE_YOU\n")
            s.flush()
            
            response = s.readline().decode().strip()
            print(f"Response: {response}")
            
            if "ARM_1" in response:
                return s
            s.close()
        except Exception as e:
            print(f"Error on {port}: {e}")
    return None

# --- MAIN MISSION ---
print(">>> LAUNCHING PHASE 3A: DIRECT DRIVE FLEET <<<")
robot = find_robot_port()

if robot:
    print("\n[SUCCESS] Connected to ARM_1 via Direct GPIO Mode.")
    time.sleep(1)

    # Test Sequence: Base & Shoulder Only (Due to Pin Limits)
    cmds = [
        ("MOVE_BASE_FWD", 1.0),
        ("STOP", 0.5),
        ("MOVE_BASE_BACK", 1.0),
        ("STOP", 0.5),
        ("MOVE_SHOULDER_FWD", 0.5),
        ("STOP", 0.5)
    ]

    for cmd, duration in cmds:
        print(f"Sending: {cmd} for {duration}s")
        robot.write(f"{cmd}\n".encode())
        time.sleep(duration)
    
    # Final Stop
    robot.write(b"STOP\n")
    robot.close()
    print("Mission Complete.")
else:
    print("[FAIL] No robot found. Is the Pico running the Phase 3A code?")
