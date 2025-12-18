# File: main.py (For ARM 2 ONLY)
# Hardware: 2 Expanders (0x20, 0x21)
import sys
import select
import time
from machine import Pin, I2C
from mcp23017 import MCP23017

ROBOT_ID = "ARM_2"

# --- I2C SETUP ---
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
try:
    exp1 = MCP23017(i2c, 0x20) # Main Arm
    exp2 = MCP23017(i2c, 0x21) # Wrist & Relay
except:
    print("EXPANDER ERROR")

# --- MOTOR CLASS ---
class Motor:
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

    def hold(self):
        # Keeps Enables ON, but Speed OFF (Active Brake)
        self.exp.digital_write(self.pins[2], 1)
        self.exp.digital_write(self.pins[3], 1)
        self.exp.digital_write(self.pins[0], 0)
        self.exp.digital_write(self.pins[1], 0)

    def stop(self):
        self.exp.digital_write(self.pins[2], 0)
        self.exp.digital_write(self.pins[3], 0)
        self.exp.digital_write(self.pins[0], 0)
        self.exp.digital_write(self.pins[1], 0)

# --- PIN DEFINITIONS ---
# Expander 1 (0x20)
base     = Motor("Base", exp1, [0, 1, 2, 3])
shoulder = Motor("Shoulder", exp1, [4, 5, 6, 7])
elbow    = Motor("Elbow", exp1, [8, 9, 10, 11])
gripper  = Motor("Gripper", exp1, [12, 13, 14, 15])

# Expander 2 (0x21)
pitch    = Motor("Pitch", exp2, [0, 1, 2, 3])
roll     = Motor("Roll", exp2, [4, 5, 6, 7])
# Relay on GPB0/GPB1 of Expander 2
relay_pin = 8 # GPB0

# --- COMMAND LISTENER ---
print(f"{ROBOT_ID}_READY")
while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        cmd = sys.stdin.readline().strip()
        
        if cmd == "WHO_ARE_YOU": print(ROBOT_ID)
        
        # --- BASE COMMANDS ---
        elif cmd == "MOVE_BASE_FWD": base.forward()
        elif cmd == "MOVE_BASE_BACK": base.backward()
        elif cmd == "HOLD_BASE": base.hold()
        
        # --- ARM COMMANDS ---
        elif cmd == "EXTEND_ARM": 
            shoulder.forward()
            elbow.forward()
        elif cmd == "RETRACT_ARM": 
            shoulder.backward()
            elbow.backward()
        elif cmd == "HOLD_ARM":
            shoulder.hold()
            elbow.hold()
            
        # --- GRIPPER COMMANDS ---
        elif cmd == "GRIPPER_CLOSE": gripper.forward()
        elif cmd == "GRIPPER_OPEN": gripper.backward()
        elif cmd == "HOLD_GRIPPER": gripper.hold()
        
        # --- STOP ---
        elif cmd == "STOP_ALL": 
            base.stop(); shoulder.stop(); elbow.stop(); 
            gripper.stop(); pitch.stop(); roll.stop()
            
    time.sleep(0.01)
