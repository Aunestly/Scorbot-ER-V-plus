# SCORBOT Standalone Test: 4-Cycle Pick & Return
# Sequence: Turn Base>Extend>Grip>(Retract + Turn Base)>Release
# Runs 4 times.
# NOTE: CLEAN ENCODERS or Sensors TO FIX DRIFTING ISSUE AFTER 3rd Cycle

from machine import Pin
import time

# --- CONFIGURATION ---
LOOP_COUNT = 4           # How many times to run
ARM_MOVE_TIME = 1.2      # Time for Shoulder/Elbow to move
GRIPPER_MOVE_TIME = 0.8  # Time for Gripper
BASE_MOVE_TIME = 2.0     # Time for Base to Move

# --- Motor Class ---
class Motor:
    def __init__(self, name, rpwm_pin, lpwm_pin, r_en_pin, l_en_pin):
        self.name = name
        self.rpwm = Pin(rpwm_pin, Pin.OUT)
        self.lpwm = Pin(lpwm_pin, Pin.OUT)
        self.r_en = Pin(r_en_pin, Pin.OUT)
        self.l_en = Pin(l_en_pin, Pin.OUT)
        self.stop() 

    def forward(self):
        # Logic swapped per previous request (Forward is now Backward)
        self.r_en.value(1)
        self.l_en.value(1)
        self.rpwm.value(0) 
        self.lpwm.value(1) 

    def backward(self):
        # Logic swapped per previous request (Backward is now Forward)
        self.r_en.value(1)
        self.l_en.value(1)
        self.rpwm.value(1) 
        self.lpwm.value(0) 

    def hold(self):
        # Active Brake
        # print(f"[{self.name}] HOLDING (Brake ON)") # Commented out to reduce spam
        self.r_en.value(1)
        self.l_en.value(1)
        self.rpwm.value(0)
        self.lpwm.value(0)

    def stop(self):
        # Passive Coast
        # print(f"[{self.name}] Power Cut (Coast)")
        self.r_en.value(0)
        self.l_en.value(0)
        self.rpwm.value(0)
        self.lpwm.value(0)

# --- Hardware Setup ---
shoulder = Motor("Shoulder", 18, 19, 20, 21)
elbow = Motor("Elbow", 6, 7, 8, 9)
gripper = Motor("Gripper", 10, 11, 12, 15)
base = Motor("Base", 14, 13, 16, 17)

# --- Main Sequence ---
print("--- Pick & Return Loop Test (Standalone) ---")
print(f"Running sequence {LOOP_COUNT} times.")
print("Starting in 3 seconds...")
time.sleep(3)

try:
    # ---------------------------------------------------------
    # MAIN LOOP STARTS HERE
    # ---------------------------------------------------------
    for cycle in range(1, LOOP_COUNT + 1):
        print(f"\n=== STARTING CYCLE {cycle} OF {LOOP_COUNT} ===")

        # 1. BASE TURN (Move to Target)
        print(f">>> [Cycle {cycle}] 1. BASE TURNING TO TARGET...")
        base.forward()
        time.sleep(BASE_MOVE_TIME)
        base.stop()
        time.sleep(0.5)
        
        # 2. EXTEND ARM (Reach Out)
        print(f">>> [Cycle {cycle}] 2. EXTENDING ARM...")
        shoulder.forward()
        elbow.forward()
        time.sleep(ARM_MOVE_TIME)
        
        # Hold Arm Position
        shoulder.hold()
        elbow.hold()
        time.sleep(0.5)

        # 3. GRIP (Close Gripper)
        print(f">>> [Cycle {cycle}] 3. CLOSING GRIPPER...")
        gripper.backward() 
        time.sleep(GRIPPER_MOVE_TIME)
        gripper.hold() # Keep holding the object!
        time.sleep(0.5)
        
        # 4. SIMULTANEOUS RETURN (Retract + Turn Base)
        print(f">>> [Cycle {cycle}] 4. RETURNING HOME (Simultaneous)...")
        
        # A. Start ALL motors immediately
        base.backward()      # Turn base home
        shoulder.backward()  # Pull arm back
        elbow.backward()     # Pull arm back
        
        # B. Wait for Arm (It finishes first)
        time.sleep(ARM_MOVE_TIME)
        shoulder.hold()
        elbow.hold()
        
        # C. Wait for remaining Base time
        remaining_time = BASE_MOVE_TIME - ARM_MOVE_TIME
        if remaining_time > 0:
            time.sleep(remaining_time)
            
        # D. Stop Base
        base.stop()
        time.sleep(0.5)

        # 5. RELEASE (Open Gripper)
        print(f">>> [Cycle {cycle}] 5. RELEASING OBJECT...")
        gripper.forward()
        time.sleep(GRIPPER_MOVE_TIME)
        gripper.stop() # Relax gripper
        time.sleep(1.0) # Pause before next cycle starts

    
    # FINAL HOLD after all loops are done
    print("\n>>> All Cycles Complete. Holding Position (3s)...")
    shoulder.hold()
    elbow.hold()
    time.sleep(3.0)

finally:
    print("\n[SAFETY] Cutting Power to ALL Motors.")
    shoulder.stop()
    elbow.stop()
    gripper.stop()
    base.stop()
