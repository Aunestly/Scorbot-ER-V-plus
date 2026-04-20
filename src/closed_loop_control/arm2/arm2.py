
# File: arm2.py (FINAL: DELAYED WRIST PITCH ON APPROACH)
import machine
import time
import sys
from pid import PID
import mcp23017

# ==========================================
# 1. WAYPOINTS
# ==========================================
POS_HOME          = [    0,      0,    0 ] 
POS_GRAB_ORANGE   = [    0, -5240, 1968 ] 
POS_GRAB_BLUE     = [    0, -5240, 1968 ] 

POS_RELEASE_A     = [ -3107, -6315,  811 ] 
POS_RELEASE_B     = [ -4838, -4868, 1769 ] 

POS_CRUISE_A      = [ POS_RELEASE_A[0], 0, 0 ]
POS_CRUISE_B      = [ POS_RELEASE_B[0], 0, 0 ]

# ==========================================
# 2. SYSTEM SETUP 
# ==========================================
print(">>> SYSTEM BOOTING (ARM 2)...")

# --- I2C SETUP (Hardware I2C - Exactly like Arm 1) ---
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=400000)
mcp = None
try:
    mcp = mcp23017.MCP23017(i2c, 0x20)
    print(">>> Expander: ONLINE")
except Exception as e:
    print(f">>> Expander: FAILED ({e})")

# --- MOTOR PINS ---
BASE_RPWM = machine.PWM(machine.Pin(18)); BASE_RPWM.freq(1000)
BASE_LPWM = machine.PWM(machine.Pin(19)); BASE_LPWM.freq(1000)
BASE_EN   = machine.Pin(7, machine.Pin.OUT); BASE_EN.value(1)

SHL_RPWM = machine.PWM(machine.Pin(21)); SHL_RPWM.freq(1000)
SHL_LPWM = machine.PWM(machine.Pin(20)); SHL_LPWM.freq(1000)
SHL_EN   = machine.Pin(22, machine.Pin.OUT); SHL_EN.value(1)

ELB_RPWM = machine.PWM(machine.Pin(10)); ELB_RPWM.freq(1000)
ELB_LPWM = machine.PWM(machine.Pin(11)); ELB_LPWM.freq(1000)
ELB_EN   = machine.Pin(12, machine.Pin.OUT); ELB_EN.value(1)

# --- WRIST & GRIPPER PINS ---
WP1_RPWM = 4; WP1_LPWM = 5; WP1_REN = 6; WP1_LEN = 7
WP2_RPWM = 0; WP2_LPWM = 1; WP2_REN = 2; WP2_LEN = 3 
GRIP_RPWM = 12; GRIP_LPWM = 13; GRIP_REN = 14; GRIP_LEN = 15

# --- ENCODERS ---
enc_base_a = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
enc_base_b = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)
enc_shl_a  = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
enc_shl_b  = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
enc_elb_a  = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
enc_elb_b  = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

pos = [0, 0, 0]

def handle_base(p):
    if enc_base_b.value() != enc_base_a.value(): pos[0] += 1
    else: pos[0] -= 1
def handle_shl(p):
    if enc_shl_b.value() != enc_shl_a.value(): pos[1] += 1
    else: pos[1] -= 1
def handle_elb(p):
    if enc_elb_b.value() != enc_elb_a.value(): pos[2] += 1
    else: pos[2] -= 1

enc_base_a.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=handle_base)
enc_shl_a.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=handle_shl)
enc_elb_a.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=handle_elb)

# ==========================================
# 4. UTILITIES (PIDs, GRIPPER, & WRIST)
# ==========================================
pid_base = PID(15.0, 0.0, 5.0, 40000, 65535) 
pid_shl  = PID(100.0, 0.0, 15.0, 15000, 65535) 
pid_elb  = PID(90.0,  0.0, 12.0, 15000, 65535) 

def set_motor(rpwm, lpwm, power):
    if power > 0:
        rpwm.duty_u16(abs(int(power))); lpwm.duty_u16(0)
    else:
        rpwm.duty_u16(0); lpwm.duty_u16(abs(int(power)))

# --- ACTIVE HOLD ---
def active_hold(target, duration, lock_base=False):
    start = time.time()
    while time.time() - start < duration:
        cur_base = pos[0] if lock_base else target[0]
        p_base = pid_base.compute(cur_base, pos[0])
        p_shl  = pid_shl.compute(target[1], pos[1])
        p_elb  = pid_elb.compute(target[2], pos[2])
        
        set_motor(BASE_RPWM, BASE_LPWM, p_base)
        set_motor(SHL_RPWM, SHL_LPWM, p_shl)
        set_motor(ELB_RPWM, ELB_LPWM, p_elb)
        time.sleep(0.01)

# --- GRIPPER ---
def grip_control(action, current_target, duration=1.5, lock_base=False):
    if mcp is None: 
        print(f"   [!] Expander Offline. Skipping Gripper {action}.")
        return
        
    mcp.pin(GRIP_REN, value=1); mcp.pin(GRIP_LEN, value=1)
    
    if action == "OPEN":
        mcp.pin(GRIP_RPWM, value=1); mcp.pin(GRIP_LPWM, value=0)
    elif action == "CLOSE":
        mcp.pin(GRIP_RPWM, value=0); mcp.pin(GRIP_LPWM, value=1)
        
    active_hold(current_target, duration, lock_base)
    
    mcp.pin(GRIP_RPWM, value=0); mcp.pin(GRIP_LPWM, value=0)

# --- WRIST ---
def move_wrist(action, duration=0.5):
    if mcp is None: 
        print(f"   [!] Expander Offline. Skipping Wrist {action}.")
        return 
        
    mcp.pin(WP1_REN, value=1); mcp.pin(WP1_LEN, value=1)
    mcp.pin(WP2_REN, value=1); mcp.pin(WP2_LEN, value=1)
    
    if action == "PITCH_UP": 
        mcp.pin(WP1_RPWM, value=1); mcp.pin(WP1_LPWM, value=0)
        mcp.pin(WP2_RPWM, value=0); mcp.pin(WP2_LPWM, value=1)
    elif action == "PITCH_DOWN":
        mcp.pin(WP1_RPWM, value=0); mcp.pin(WP1_LPWM, value=1)
        mcp.pin(WP2_RPWM, value=1); mcp.pin(WP2_LPWM, value=0)
        
    time.sleep(duration)
    
    mcp.pin(WP1_RPWM, value=0); mcp.pin(WP1_LPWM, value=0)
    mcp.pin(WP2_RPWM, value=0); mcp.pin(WP2_LPWM, value=0)
    mcp.pin(WP1_REN, value=0); mcp.pin(WP1_LEN, value=0)
    mcp.pin(WP2_REN, value=0); mcp.pin(WP2_LEN, value=0)

def go_to(target, name, lock_base=False, timeout=8.0, tol=60):
    print(f"--> {name}...")
    start = time.time()
    while time.time() - start < timeout:
        
        # --- ANTI-CRASH LIMITS ---
        if pos[1] > 800 or pos[1] < -7500:
            print("\n[!] EMERGENCY CUTOFF [!]")
            break
            
        cur_base = pos[0] if lock_base else target[0]
        p_base = pid_base.compute(cur_base, pos[0])
        p_shl  = pid_shl.compute(target[1], pos[1])
        p_elb  = pid_elb.compute(target[2], pos[2])
        
        set_motor(BASE_RPWM, BASE_LPWM, p_base)
        set_motor(SHL_RPWM, SHL_LPWM, p_shl)
        set_motor(ELB_RPWM, ELB_LPWM, p_elb)
        
        if abs(target[0]-pos[0])<tol and abs(target[1]-pos[1])<tol and abs(target[2]-pos[2])<tol:
            break
        time.sleep(0.01)

def auto_home():
    global pos 
    
    print("--> CENTERING BASE...")
    go_to([0, pos[1], pos[2]], "BASE RETURN", lock_base=False, timeout=15.0, tol=40)
    
    print("--> FOLDING WRIST BACK...")
    move_wrist("PITCH_DOWN", 0.5)
    
    print("--> FORCING SHOULDER TO BACK WALL...")
    set_motor(SHL_RPWM, SHL_LPWM, 45000) 
    time.sleep(1.5) 
    
    print(">>> SHUTTING DOWN MOTORS <<<")
    set_motor(BASE_RPWM, BASE_LPWM, 0)
    set_motor(SHL_RPWM, SHL_LPWM, 0)
    set_motor(ELB_RPWM, ELB_LPWM, 0)
    
    pos = [0, 0, 0] 
    print("--> TRUE ZERO FOUND AT WALL.")

# ==========================================
# 5. EXECUTION 
# ==========================================
def run_cycle_orange():
    print("\n>>> SORTING ORANGE -> BOX A <<<")
    
    print("--> PREPARING JAWS...")
    grip_control("OPEN", POS_HOME, 1.5) 
    
    # --- FIX: Wrist pitches up right as it approaches the block ---
    print("--> PITCHING WRIST FORWARD...")
    move_wrist("PITCH_UP", 0.3)
    
    go_to(POS_GRAB_ORANGE, "GRAB", lock_base=True, timeout=10.0, tol=30)
    grip_control("CLOSE", POS_GRAB_ORANGE, 1.5, lock_base=True) 
    
    go_to(POS_HOME, "FLY-UP", lock_base=True, timeout=10.0, tol=80) 
    go_to(POS_RELEASE_A, "SWING", timeout=12.0, tol=40)
    
    print("--> DROPPING ITEM...")
    grip_control("OPEN", POS_RELEASE_A, 1.0) 
    
    time.sleep(0.5) 
    
    print("--> PARKING GRIPPER (CLOSE)...")
    grip_control("CLOSE", POS_RELEASE_A, 1.5, lock_base=True)
    
    go_to(POS_CRUISE_A, "CLEAR", lock_base=True, timeout=10.0, tol=80)
    
    auto_home()

def run_cycle_blue():
    print("\n>>> SORTING BLUE -> BOX B <<<")
    
    print("--> PREPARING JAWS...")
    grip_control("OPEN", POS_HOME, 1.5) 
    
    # --- FIX: Wrist pitches up right as it approaches the block ---
    print("--> PITCHING WRIST FORWARD...")
    move_wrist("PITCH_UP", 0.3)
    
    go_to(POS_GRAB_BLUE, "GRAB", lock_base=True, timeout=10.0, tol=30)
    grip_control("CLOSE", POS_GRAB_BLUE, 1.5, lock_base=True) 
    
    go_to(POS_HOME, "FLY-UP", lock_base=True, timeout=10.0, tol=80)
    go_to(POS_RELEASE_B, "SWING", timeout=12.0, tol=40)
    
    print("--> DROPPING ITEM...")
    grip_control("OPEN", POS_RELEASE_B, 1.0) 
    
    time.sleep(0.5)
    
    print("--> PARKING GRIPPER (CLOSE)...")
    grip_control("CLOSE", POS_RELEASE_B, 1.5, lock_base=True)
    
    go_to(POS_CRUISE_B, "CLEAR", lock_base=True, timeout=10.0, tol=80)
    
    auto_home()
