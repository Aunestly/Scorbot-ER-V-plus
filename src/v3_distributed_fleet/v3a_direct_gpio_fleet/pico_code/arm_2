# File: main.py (Save to ARM 2 Pico)
# ROLE: DIRECT SPINAL CORD (Granular Control)

import sys
import select
import time
from machine import Pin

ROBOT_ID = "ARM_2" 

class Motor:
    def __init__(self, name, rpwm_pin, lpwm_pin, r_en_pin, l_en_pin):
        self.name = name
        self.rpwm = Pin(rpwm_pin, Pin.OUT)
        self.lpwm = Pin(lpwm_pin, Pin.OUT)
        self.r_en = Pin(r_en_pin, Pin.OUT)
        self.l_en = Pin(l_en_pin, Pin.OUT)
        self.stop()

    def forward(self):
        # Logic swapped per previous setup
        self.r_en.value(1); self.l_en.value(1)
        self.rpwm.value(0); self.lpwm.value(1)

    def backward(self):
        # Logic swapped per previous setup
        self.r_en.value(1); self.l_en.value(1)
        self.rpwm.value(1); self.lpwm.value(0)

    def hold(self):
        self.r_en.value(1); self.l_en.value(1)
        self.rpwm.value(0); self.lpwm.value(0)

    def stop(self):
        self.r_en.value(0); self.l_en.value(0)
        self.rpwm.value(0); self.lpwm.value(0)

# --- MOTOR DEFINITIONS ---
# Verify these pins match your physical wiring!
base = Motor("Base", 14, 13, 16, 17)
shoulder = Motor("Shoulder", 18, 19, 20, 21)
elbow = Motor("Elbow", 6, 7, 8, 9)
gripper = Motor("Gripper", 10, 11, 12, 15)

print(f"{ROBOT_ID}_READY")

while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        cmd = sys.stdin.readline().strip()
        
        if cmd == "WHO_ARE_YOU":
            print(ROBOT_ID)

        # --- MOVEMENT GROUPS ---
        elif cmd == "MOVE_BASE_FWD":   base.forward()
        elif cmd == "MOVE_BASE_BACK":  base.backward()
        elif cmd == "HOLD_BASE":       base.hold() # Stops just the base
        
        elif cmd == "EXTEND_ARM":      shoulder.forward(); elbow.forward()
        elif cmd == "RETRACT_ARM":     shoulder.backward(); elbow.backward()
        elif cmd == "HOLD_ARM":        shoulder.hold(); elbow.hold() # Stops just the arm
        
        elif cmd == "GRIPPER_CLOSE":   gripper.backward() # Check your specific polarity
        elif cmd == "GRIPPER_OPEN":    gripper.forward()
        elif cmd == "HOLD_GRIPPER":    gripper.hold()

        # --- SAFETY ---
        elif cmd == "STOP_ALL":
            base.stop(); shoulder.stop(); elbow.stop(); gripper.stop()
            
    time.sleep(0.01)
