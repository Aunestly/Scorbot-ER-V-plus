# File: main.py (Phase 3A - Direct GPIO Listener)
# LOAD ON BOTH PICOS (Change ROBOT_ID for the second one)
# or see other main.py code in this file.
import sys
import select
from machine import Pin

# !!! CHANGE THIS TO "ARM_2" FOR THE SECOND ROBOT !!!
ROBOT_ID = "ARM_1" 

# --- HARDWARE SETUP (Direct Drive) ---
# Note: R_EN and L_EN are wired to 3.3V (Physical Pin 36)
base_rpwm     = Pin(0, Pin.OUT)
base_lpwm     = Pin(1, Pin.OUT)
shoulder_rpwm = Pin(2, Pin.OUT)
shoulder_lpwm = Pin(3, Pin.OUT)
elbow_rpwm    = Pin(4, Pin.OUT)
elbow_lpwm    = Pin(5, Pin.OUT)
gripper_rpwm  = Pin(6, Pin.OUT)
gripper_lpwm  = Pin(7, Pin.OUT)

def stop_all():
    base_rpwm.value(0);     base_lpwm.value(0)
    shoulder_rpwm.value(0); shoulder_lpwm.value(0)
    elbow_rpwm.value(0);    elbow_lpwm.value(0)
    gripper_rpwm.value(0);  gripper_lpwm.value(0)

# --- COMMAND HANDLERS ---
def move_base(dir):
    stop_all()
    if dir == "FWD": base_lpwm.value(1)
    else: base_rpwm.value(1)

def move_shoulder(dir):
    stop_all()
    if dir == "FWD": shoulder_lpwm.value(1)
    else: shoulder_rpwm.value(1)

# --- LISTENER LOOP ---
print(f"{ROBOT_ID}_READY_PHASE_3A")
stop_all()

while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline().strip()
        
        if line == "WHO_ARE_YOU":
            print(ROBOT_ID)
            
        elif line == "MOVE_BASE_FWD":     move_base("FWD")
        elif line == "MOVE_BASE_BACK":    move_base("BACK")
        elif line == "MOVE_SHOULDER_FWD": move_shoulder("FWD")
        elif line == "MOVE_SHOULDER_BACK":move_shoulder("BACK")
        
        elif line == "STOP":
            stop_all()
