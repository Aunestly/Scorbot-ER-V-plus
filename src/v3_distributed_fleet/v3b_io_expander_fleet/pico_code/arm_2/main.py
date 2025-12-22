# File: main.py (For ARM 2 ONLY)
# Hardware: 2 Expanders (0x20, 0x21) connected to GP16/GP17
# Movement: Base turn Extend Identrical Movement for Arm 2 Connections
# Fix: Added WHO_ARE_YOU response so Fleet Manager can find it.

import sys
import select
import time
import machine
from mcp23017 import MCP23017

ROBOT_ID = "ARM_2"

# --- 1. I2C SETUP (SoftI2C for stability) ---
sda = machine.Pin(16)
scl = machine.Pin(17)
i2c = machine.SoftI2C(sda=sda, scl=scl, freq=100000)

print(f"{ROBOT_ID}: Booting up...")

# --- 2. CONNECTION RETRY LOOP ---
connected = False
while not connected:
    try:
        devices = i2c.scan()
        if 32 in devices and 33 in devices:
            exp1 = MCP23017(i2c, 0x20) # Main Arm
            exp2 = MCP23017(i2c, 0x21) # Wrist & Relay
            connected = True
            print("SUCCESS: Connection Established!")
        else:
            print(f" > Bus Scan Failed. Found: {devices}")
            time.sleep(2)
    except Exception as e:
        print(f" > Error: {e}")
        time.sleep(2)

# --- 3. MOTOR CLASS ---
class Motor:
    def __init__(self, name, expander, pins):
        self.name = name
        self.exp = expander
        self.pins = pins 
        for p in self.pins:
            self.exp.pin(p, mode=0, value=0)

    def forward(self):
        self.exp.pin(self.pins[2], value=1) # R_EN
        self.exp.pin(self.pins[3], value=1) # L_EN
        self.exp.pin(self.pins[0], value=0) # RPWM
        self.exp.pin(self.pins[1], value=1) # LPWM

    def backward(self):
        self.exp.pin(self.pins[2], value=1)
        self.exp.pin(self.pins[3], value=1)
        self.exp.pin(self.pins[0], value=1)
        self.exp.pin(self.pins[1], value=0)

    def hold(self):
        self.exp.pin(self.pins[2], value=1)
        self.exp.pin(self.pins[3], value=1)
        self.exp.pin(self.pins[0], value=0)
        self.exp.pin(self.pins[1], value=0)

    def stop(self):
        self.exp.pin(self.pins[2], value=0)
        self.exp.pin(self.pins[3], value=0)
        self.exp.pin(self.pins[0], value=0)
        self.exp.pin(self.pins[1], value=0)

# --- 4. HARDWARE DEFINITIONS ---
# Expander 1 (0x20)
base     = Motor("Base",     exp1, [0, 1, 2, 3])
shoulder = Motor("Shoulder", exp1, [4, 5, 6, 7])
elbow    = Motor("Elbow",    exp1, [8, 9, 10, 11])
gripper  = Motor("Gripper",  exp1, [12, 13, 14, 15])

# Expander 2 (0x21)
pitch    = Motor("Pitch",    exp2, [0, 1, 2, 3])
roll     = Motor("Roll",     exp2, [4, 5, 6, 7])
exp2.pin(8, mode=0, value=0) # Relay
exp2.pin(9, mode=0, value=0)

# --- 5. COMMAND LISTENER ---
print(f"{ROBOT_ID}_READY")

def handle_command(cmd):
    cmd = cmd.strip().upper()
    
    # --- IDENTITY CHECK (CRITICAL FOR FLEET MANAGER) ---
    if cmd == "WHO_ARE_YOU":
        print(ROBOT_ID)
        return
    # ---------------------------------------------------

    # RELAYS
    if cmd == "RELAY_1_ON":     exp2.pin(8, value=1)
    elif cmd == "RELAY_1_OFF":  exp2.pin(8, value=0)

    # BASE
    elif cmd == "MOVE_BASE_FWD":  base.forward()
    elif cmd == "MOVE_BASE_BACK": base.backward()
    elif cmd == "HOLD_BASE":      base.hold()

    # ARM
    elif cmd == "EXTEND_ARM":     
        shoulder.forward()
        elbow.forward()
    elif cmd == "RETRACT_ARM":    
        shoulder.backward()
        elbow.backward()
    elif cmd == "HOLD_ARM":       
        shoulder.hold()
        elbow.hold()

    # GRIPPER
    elif cmd == "GRIPPER_CLOSE":  gripper.forward()
    elif cmd == "GRIPPER_OPEN":   gripper.backward()
    elif cmd == "HOLD_GRIPPER":   gripper.hold()

    # WRISTS
    elif cmd == "PITCH_UP":       pitch.forward()
    elif cmd == "PITCH_DOWN":     pitch.backward()

    # STOP
    elif cmd == "STOP" or cmd == "STOP_ALL": 
        base.stop()
        shoulder.stop()
        elbow.stop()
        gripper.stop()
        pitch.stop()
        roll.stop()
        exp2.pin(8, value=0)

# --- MAIN LOOP ---
while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if line:
            handle_command(line)
