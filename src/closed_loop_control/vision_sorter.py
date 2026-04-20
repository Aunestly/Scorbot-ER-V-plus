# File: vision_sorter.py
import cv2
import numpy as np
import serial
import time
import glob

# --- 1. ROBOT COMMUNICATION ---
def find_robots():
    robots = {}
    # Added ttyUSB just in case the Pi 4 shifted the port names
    ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')
    print(f"\n>>> Scanning USB ports: {ports}...")
    
    for port in ports:
        try:
            print(f"Attempting to open {port}...")
            s = serial.Serial(port, 115200, timeout=2)
            time.sleep(2) 
            s.reset_input_buffer()
            s.write(b"WHO_ARE_YOU\n")
            s.flush()
            
            for _ in range(5): 
                line = s.readline().decode('utf-8').strip()
                if line:
                    print(f"[{port}] Replied: '{line}'") # Let's see what it actually says
                
                if "ARM_2" in line: 
                    robots['ARM_2'] = s
                    print(f" > SUCCESS: Found ARM_2 on {port}")
                    break
                elif "ARM_1" in line: 
                    robots['ARM_1'] = s
                    print(f" > SUCCESS: Found ARM_1 on {port}")
                    break
                    
        except Exception as e: 
            # NO MORE SILENT FAILURES. THIS TELLS US EXACTLY WHAT IS WRONG.
            print(f"[!] FAILED to connect to {port}: {e}")
            
    return robots

fleet = find_robots()

if 'ARM_2' not in fleet:
    print("\n[WARNING] ARM 2 NOT FOUND! The camera will work, but Arm 2 will NOT move.")
    print("If you see an Errno 16 (Device Busy) above, unplug the Pico and plug it back in!")
    time.sleep(3)
if 'ARM_1' not in fleet:
    print("\n[WARNING] ARM 1 NOT FOUND! (Just a heads up)")
    time.sleep(1)

def trigger_and_wait(robot_name, command):
    if robot_name in fleet:
        robot = fleet[robot_name]
        
        # CLEAR THE BUFFER FIRST
        robot.reset_input_buffer()
        
        print(f"\n>>> Triggering {command}... Arm moving.")
        robot.write(f"{command}\n".encode('utf-8'))
        
        while True:
            # Keep the camera alive while waiting for the arm!
            ret, frame = cap.read()
            if ret:
                cv2.putText(frame, "ARM MOVING - PLEASE WAIT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                cv2.imshow('Conveyor Color Tracker', frame)
                cv2.waitKey(1)
                
            if robot.in_waiting > 0:
                response = robot.readline().decode('utf-8').strip()
                if "DONE" in response:
                    print(f"[{robot_name}] Finished sorting! Camera resuming...\n")
                    robot.reset_input_buffer() 
                    break

# --- 2. CAMERA SETUP ---
cap = cv2.VideoCapture(0)

# Ultra-Strict Orange (Ignores all brown/shadows)
lower_orange = np.array([5, 160, 160]) 
upper_orange = np.array([25, 255, 255])

lower_blue = np.array([100, 100, 100])
upper_blue = np.array([130, 255, 255])

print("\n>>> VISION SYSTEM ACTIVE. Waiting for Orange or Blue item... Press 'q' to quit. <<<")

# --- 3. MAIN DETECTION LOOP ---
while True:
    ret, frame = cap.read()
    if not ret: break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    MIN_AREA = 2000 
    
    # Check for ORANGE
    contours_orange, _ = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours_orange:
        if cv2.contourArea(c) > MIN_AREA:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 165, 255), 2)
            cv2.putText(frame, "ORANGE -> BOX A", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
            
            cv2.imshow('Conveyor Color Tracker', frame)
            cv2.waitKey(1) 
            
            trigger_and_wait('ARM_2', 'RUN_ARM2_ORANGE')
            for _ in range(5): cap.read() 
            break 

    # Check for BLUE
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours_blue:
        if cv2.contourArea(c) > MIN_AREA:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "BLUE -> BOX B", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            
            cv2.imshow('Conveyor Color Tracker', frame)
            cv2.waitKey(1)
            
            trigger_and_wait('ARM_2', 'RUN_ARM2_BLUE')
            for _ in range(5): cap.read() 
            break 

    cv2.imshow('Conveyor Color Tracker', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
for name, robot in fleet.items(): robot.close()







