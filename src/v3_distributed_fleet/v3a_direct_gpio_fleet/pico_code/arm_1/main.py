# File: main.py (Save to ARM 1 Pico)
# ROLE: DIRECT SPINAL CORD (Base Control Only)

import sys
import select
import time
from machine import Pin

# --- IDENTITY ---
ROBOT_ID = "ARM_1"  # <--- IDENTIFIES THIS AS THE LEFT ROBOT

class Motor:
    def __init__(self, name, rpwm_pin, lpwm_pin, r_en_pin, l_en_pin):
        self.name = name
        self.rpwm = Pin(rpwm_pin, Pin.OUT)
        self.lpwm = Pin(lpwm_pin, Pin.OUT)
        self.r_en = Pin(r_en_pin, Pin.OUT)
        self.l_en = Pin(l_en_pin, Pin.OUT)
        self.stop()

    def forward(self):
        # Logic swapped per your setup
        self.r_en.value(1); self.l_en.value(1)
        self.rpwm.value(0); self.lpwm.value(1)

    def backward(self):
        self.r_en.value(1); self.l_en.value(1)
        self.rpwm.value(1); self.lpwm.value(0)

    def stop(self):
        self.r_en.value(0); self.l_en.value(0)
        self.rpwm.value(0); self.lpwm.value(0)

# --- MOTOR DEFINITIONS ---
# Base pins for Arm 1 (Verify these match your wiring!)
base = Motor("Base", 14, 13, 16, 17)

print(f"{ROBOT_ID}_READY")

while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        cmd = sys.stdin.readline().strip()
        
        if cmd == "WHO_ARE_YOU":
            print(ROBOT_ID)

        # --- BASE COMMANDS ---
        elif cmd == "MOVE_BASE_FWD":
            base.forward()
        elif cmd == "MOVE_BASE_BACK":
            base.backward()
        
        # --- SAFETY ---
        elif cmd == "STOP":
            base.stop()
            
    time.sleep(0.01)

        elif line == "MOVE_SHOULDER_FWD": move_shoulder("FWD")
        elif line == "MOVE_SHOULDER_BACK":move_shoulder("BACK")
        
        elif line == "STOP":
            stop_all()
