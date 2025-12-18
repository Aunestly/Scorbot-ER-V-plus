# File: main.py (For ARM 1 ONLY)
# Hardware: 1 Expander + Direct Pins for Pitch/Roll
import sys
import select
import time
from machine import Pin, I2C
from mcp23017 import MCP23017

ROBOT_ID = "ARM_1"

# --- I2C SETUP (For Expander 1) ---
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
try:
    exp1 = MCP23017(i2c, 0x20)
except:
    print("EXPANDER ERROR")

# --- MOTOR CLASSES ---

# Class for motors on the Expander (Base, Shoulder, Elbow, Gripper)
class ExpanderMotor:
    def __init__(self, name, expander, pins):
        self.name = name
        self.exp = expander
        self.pins = pins # [rpwm, lpwm, r_en, l_en]
        self.stop()

    def forward(self):
        self.exp.digital_write(self.pins[2], 1) # R_EN
        self.exp.digital_write(self.pins[3], 1) # L_EN
        self.exp.digital_write(self.pins[0], 0) # RPWM
        self.exp.digital_write(self.pins[1], 1) # LPWM

    def backward(self):
        self.exp.digital_write(self.pins[2], 1)
        self.exp.digital_write(self.pins[3], 1)
        self.exp.digital_write(self.pins[0], 1)
        self.exp.digital_write(self.pins[1], 0)

    def stop(self):
        self.exp.digital_write(self.pins[2], 0)
        self.exp.digital_write(self.pins[3], 0)
        self.exp.digital_write(self.pins[0], 0)
        self.exp.digital_write(self.pins[1], 0)

# Class for motors directly on Pico (Pitch, Roll)
class DirectMotor:
    def __init__(self, name, pins):
        self.name = name
        # pins = [rpwm, lpwm, r_en, l_en]
        self.rpwm = Pin(pins[0], Pin.OUT)
        self.lpwm = Pin(pins[1], Pin.OUT)
        self.r_en = Pin(pins[2], Pin.OUT)
        self.l_en = Pin(pins[3], Pin.OUT)
        self.stop()

    def forward(self):
        self.r_en.value(1); self.l_en.value(1)
        self.rpwm.value(0); self.lpwm.value(1)

    def backward(self):
        self.r_en.value(1); self.l_en.value(1)
        self.rpwm.value(1); self.lpwm.value(0)

    def stop(self):
        self.r_en.value(0); self.l_en.value(0)
        self.rpwm.value(0); self.lpwm.value(0)

# --- PIN DEFINITIONS ---
# Expander Motors (Standard Wiring)
base     = ExpanderMotor("Base", exp1, [0, 1, 2, 3])
shoulder = ExpanderMotor("Shoulder", exp1, [4, 5, 6, 7])
elbow    = ExpanderMotor("Elbow", exp1, [8, 9, 10, 11])
gripper  = ExpanderMotor("Gripper", exp1, [12, 13, 14, 15])

# Direct Motors (Using free Pico pins)
pitch    = DirectMotor("Pitch", [0, 1, 2, 3])
roll     = DirectMotor("Roll", [6, 7, 8, 9])

# --- COMMAND LISTENER ---
print(f"{ROBOT_ID}_READY")
while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        cmd = sys.stdin.readline().strip()
        
        if cmd == "WHO_ARE_YOU": print(ROBOT_ID)
        elif cmd == "MOVE_BASE_FWD": base.forward()
        elif cmd == "MOVE_BASE_BACK": base.backward()
        elif cmd == "STOP": 
            base.stop(); shoulder.stop(); elbow.stop()
            pitch.stop(); roll.stop(); gripper.stop()
    time.sleep(0.01)
