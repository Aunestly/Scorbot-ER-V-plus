# File: main.py (Save to ARM 1 Pico)
# ROLE: BASE TURN AND ARM EXTEND CODE
# this is the main file for arm when when running the sequence
# connected directly to pico controls not io expnaders
# Hardware: 2 Expanders (0x20, 0x21) connected to GP16/GP17
# Hardware: Pins 16 (SDA) & 17 (SCL)
# ID: ARM_1

import sys
import select
import time
import machine
from mcp23017 import MCP23017

ROBOT_ID = "ARM_1"

# --- 1. I2C SETUP (SoftI2C on Pins 16/17) ---
sda = machine.Pin(16)
scl = machine.Pin(17)
i2c = machine.SoftI2C(sda=sda, scl=scl, freq=100000)

print(f"{ROBOT_ID}: Booting up...")

# --- 2. CONNECTION LOOP (Only looks for 0x20) ---
exp1 = None
connected = False
while not connected:
    try:
        devices = i2c.scan()
        if 32 in devices: # Found 0x20
            print("SUCCESS: Found Main Expander (0x20)!")
            exp1 = MCP23017(i2c, 0x20) 
            connected = True
        else:
            print(f" > Waiting for Expander... Found: {devices}")
            time.sleep(2)
    except:
        time.sleep(2)

# --- 3. MOTOR CLASSES ---

# Class A: For motors on the Expander Chip
class ExpanderMotor:
    def __init__(self, name, expander, pins):
        self.name = name
        self.exp = expander
        self.pins = pins # [rpwm, lpwm, r_en, l_en]
        for p in self.pins:
            self.exp.pin(p, mode=0, value=0)

    def forward(self):
        self.exp.pin(self.pins[2], value=1)
        self.exp.pin(self.pins[3], value=1)
        self.exp.pin(self.pins[0], value=0)
        self.exp.pin(self.pins[1], value=1)

    def backward(self):
        self.exp.pin(self.pins[2], value=1)
        self.exp.pin(self.pins[3], value=1)
        self.exp.pin(self.pins[0], value=1)
        self.exp.pin(self.pins[1], value=0)

    def stop(self):
        self.exp.pin(self.pins[2], value=0)
        self.exp.pin(self.pins[3], value=0)
        self.exp.pin(self.pins[0], value=0)
        self.exp.pin(self.pins[1], value=0)

# Class B: For motors connected directly to Pico GPIOs
class DirectMotor:
    def __init__(self, name, pins):
        self.name = name
        # pins = [RPWM_GPIO, LPWM_GPIO, R_EN_GPIO, L_EN_GPIO]
        self.rpwm = machine.Pin(pins[0], machine.Pin.OUT)
        self.lpwm = machine.Pin(pins[1], machine.Pin.OUT)
        self.ren  = machine.Pin(pins[2], machine.Pin.OUT)
        self.len  = machine.Pin(pins[3], machine.Pin.OUT)
        self.stop()

    def forward(self):
        self.ren.value(1)
        self.len.value(1)
        self.rpwm.value(0)
        self.lpwm.value(1)

    def backward(self):
        self.ren.value(1)
        self.len.value(1)
        self.rpwm.value(1)
        self.lpwm.value(0)

    def stop(self):
        self.ren.value(0)
        self.len.value(0)
        self.rpwm.value(0)
        self.lpwm.value(0)

# --- 4. MOTOR DEFINITIONS ---

# Group 1: The Main Arm (Uses Expander 1)
# These use the internal 0-15 numbering of the MCP23017
base     = ExpanderMotor("Base",     exp1, [0, 1, 2, 3])
shoulder = ExpanderMotor("Shoulder", exp1, [4, 5, 6, 7])
elbow    = ExpanderMotor("Elbow",    exp1, [8, 9, 10, 11])
gripper  = ExpanderMotor("Gripper",  exp1, [12, 13, 14, 15])

# Group 2: The Wrists (Uses Direct Pico Pins)
# WARNING: YOU MUST ENTER THE CORRECT GPIO NUMBERS HERE
# Example: If Pitch uses GP10, GP11, GP12, GP13 -> [10, 11, 12, 13]
pitch    = DirectMotor("Pitch", [0, 1, 2, 3]) # <--- UPDATE THIS
roll     = DirectMotor("Roll",  [6, 7, 8, 9]) # <--- UPDATE THIS

# --- 5. COMMAND LISTENER ---
print(f"{ROBOT_ID}_READY")

def handle_command(cmd):
    cmd = cmd.strip().upper()
    
    if cmd == "WHO_ARE_YOU":
        print(ROBOT_ID)
        return

    # MOVEMENT COMMANDS
    if cmd == "MOVE_BASE_FWD":    base.forward()
    elif cmd == "MOVE_BASE_BACK": base.backward()
    
    elif cmd == "EXTEND_ARM":     
        shoulder.forward()
        elbow.forward()
    elif cmd == "RETRACT_ARM":    
        shoulder.backward()
        elbow.backward()
        
    elif cmd == "GRIPPER_CLOSE":  gripper.forward()
    elif cmd == "GRIPPER_OPEN":   gripper.backward()
    
    elif cmd == "PITCH_UP":       pitch.forward()
    elif cmd == "PITCH_DOWN":     pitch.backward()
    
    elif cmd == "STOP" or cmd == "STOP_ALL": 
        base.stop(); shoulder.stop(); elbow.stop(); 
        gripper.stop(); pitch.stop(); roll.stop()

while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if line: handle_command(line)
