# File: main.py (Phase 3A - Direct GPIO Listener)
# Hardware: H-Bridges wired directly to Pico GP0-GP7
import sys
import select
from machine import Pin

# --- CONFIGURATION ---
ROBOT_ID = "ARM_1"

# Setup Motor Pins (Direct GPIO)
# Note: Enables are hard-wired to 3.3V in this phase to save pins.
base_rpwm = Pin(0, Pin.OUT)
base_lpwm = Pin(1, Pin.OUT)

shoulder_rpwm = Pin(2, Pin.OUT)
shoulder_lpwm = Pin(3, Pin.OUT)

elbow_rpwm = Pin(4, Pin.OUT)
elbow_lpwm = Pin(5, Pin.OUT)

# --- MOTOR FUNCTIONS ---
def stop_all():
    base_rpwm.value(0); base_lpwm.value(0)
    shoulder_rpwm.value(0); shoulder_lpwm.value(0)
    elbow_rpwm.value(0); elbow_lpwm.value(0)

def base_fwd():
    base_rpwm.value(0)
    base_lpwm.value(1)

def base_back():
    base_rpwm.value(1)
    base_lpwm.value(0)

def shoulder_fwd():
    shoulder_rpwm.value(0)
    shoulder_lpwm.value(1)

# --- MAIN LISTENER LOOP ---
print(f"{ROBOT_ID}_READY_PHASE_3A")
stop_all() # Safety Start

while True:
    # Check if data is available on USB Serial (Non-blocking)
    if select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline().strip()
        
        # Parse Commands
        if line == "WHO_ARE_YOU":
            print(ROBOT_ID)
        elif line == "MOVE_BASE_FWD":
            base_fwd()
        elif line == "MOVE_BASE_BACK":
            base_back()
        elif line == "MOVE_SHOULDER_FWD":
            shoulder_fwd()
        elif line == "STOP":
            stop_all()
