# File: arm1.py (FINAL: RESTORED GRIPPER VOLTAGE + WALL BUMP + ACTIVE HOLD)
import machine
import time
import sys
from pid import PID
import mcp23017

# ==========================================
# 1. WAYPOINTS
# ==========================================
POS_HOME         = [    0,     0,     0]
POS_REACH        = [-6208, -6347,  1999]  # Yellow Block
POS_CONVEYOR     = [    0, -4799,  1968]  # Safe Drop Height

POS_CRUISE_REACH = [-6208,     0,     0]  # Safe height directly above Yellow Block
POS_CRUISE_CONV  = [    0,     0,     0]  # Safe height directly above Conveyor

# ==========================================
# 2. SYSTEM SETUP
# ==========================================
print(">>> SYSTEM BOOTING (ACTIVE HOLD MODE)...")

# I2C SETUP
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=400000)
mcp = None
try:
    mcp = mcp23017.MCP23017(i2c, 0x20)
    print(">>> Expander: ONLINE")
    
    # Initialize ALL pins as outputs (0-3 for Wrist 2, 4-7 for Wrist 1, 12-15 for Gripper)
    for p in [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15]: 
        mcp.pin(p, mode=0, value=0)
except:
    print(">>> Expander: FAILED")

# ==========================================
# 3. MOTOR CONFIGURATION
# ==========================================
BASE_RPWM = machine.PWM(machine.Pin(6)); BASE_RPWM.freq(1000) 
BASE_LPWM = machine.PWM(machine.Pin(7)); BASE_LPWM.freq(1000) 
BASE_EN   = machine.Pin(8, machine.Pin.OUT); BASE_EN.value(1)

SHL_RPWM = machine.PWM(machine.Pin(21)); SHL_RPWM.freq(1000)
SHL_LPWM = machine.PWM(machine.Pin(20)); SHL_LPWM.freq(1000)
SHL_EN   = machine.Pin(22, machine.Pin.OUT); SHL_EN.value(1)

ELB_RPWM = machine.PWM(machine.Pin(10)); ELB_RPWM.freq(1000)
ELB_LPWM = machine.PWM(machine.Pin(11)); ELB_LPWM.freq(1000)
ELB_EN   = machine.Pin(12, machine.Pin.OUT); ELB_EN.value(1)

# WRIST 1 (Right Side Motor)
WP1_RPWM = 4; WP1_LPWM = 5; WP1_REN = 6; WP1_LEN = 7

# WRIST 2 (Left Side Motor)
WP2_RPWM = 0; WP2_LPWM = 1; WP2_REN = 2; WP2_LEN = 3 

# GRIPPER
GRIP_RPWM = 12; GRIP_LPWM = 13; GRIP_REN = 14; GRIP_LEN = 15

# ==========================================
# 4. ENCODER CONFIGURATION
# ==========================================
enc_base_a = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
enc_base_b = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)
enc_shl_a  = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
enc_shl_b  = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
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
# 5. PID & ACTIVE HOLD CONFIG
# ==========================================
pid_base = PID(25.0,  0.0, 3.0,  45000, 65500)
pid_shl  = PID(100.0, 0.0, 15.0, 15000, 60000)
pid_elb  = PID(90.0,  0.0, 12.0, 15000, 60000)

def set_motor(rpwm, lpwm, power):
    if power > 0:
        rpwm.duty_u16(abs(power))
        lpwm.duty_u16(0)
    else:
        rpwm.duty_u16(0)
        lpwm.duty_u16(abs(power))

def active_hold(target, duration):
    start = time.time()
    while time.time() - start < duration:
        p_base = pid_base.compute(target[0], pos[0])
        p_shl  = pid_shl.compute(target[1], pos[1])
        p_elb  = pid_elb.compute(target[2], pos[2])
        
        set_motor(BASE_RPWM, BASE_LPWM, p_base)
        set_motor(SHL_RPWM, SHL_LPWM, p_shl)
        set_motor(ELB_RPWM, ELB_LPWM, p_elb)
        time.sleep(0.01)

# GRIPPER CONTROL (FIXED: Added 'value=' back to restore voltage)
def grip_control(action, current_target, duration=1.5):
    if mcp is None: return
    mcp.pin(GRIP_REN, value=1); mcp.pin(GRIP_LEN, value=1)
    
    if action == "OPEN":
        mcp.pin(GRIP_RPWM, value=1); mcp.pin(GRIP_LPWM, value=0)
    elif action == "CLOSE":
        mcp.pin(GRIP_RPWM, value=0); mcp.pin(GRIP_LPWM, value=1)
        
    active_hold(current_target, duration)
    
    mcp.pin(GRIP_RPWM, value=0); mcp.pin(GRIP_LPWM, value=0)
    # We do NOT turn off the Enables here so the jaws hold their position

# --- DIFFERENTIAL WRIST LOGIC --- (FIXED: Added 'value=')
def move_wrist(action, duration=0.5):
    if mcp is None: return 
    
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

def kickstart_away():
    BASE_LPWM.duty_u16(55000)
    time.sleep(0.1)
    BASE_LPWM.duty_u16(0)

def kickstart_home():
    BASE_RPWM.duty_u16(55000)
    time.sleep(0.1)
    BASE_RPWM.duty_u16(0)

def go_to(target, timeout=8.0):
    print(f"   Moving to {target}...", end="")
    start = time.time()
    while time.time() - start < timeout:
        p_base = pid_base.compute(target[0], pos[0])
        p_shl  = pid_shl.compute(target[1], pos[1])
        p_elb  = pid_elb.compute(target[2], pos[2])
        
        set_motor(BASE_RPWM, BASE_LPWM, p_base)
        set_motor(SHL_RPWM, SHL_LPWM, p_shl)
        set_motor(ELB_RPWM, ELB_LPWM, p_elb)
        
        if abs(target[0]-pos[0])<50 and abs(target[1]-pos[1])<50 and abs(target[2]-pos[2])<50:
            print(" Arrived!")
            break
        time.sleep(0.01)

# ==========================================
# 6. CYCLE EXECUTION
# ==========================================
def run_cycle():
    global pos 
    
    print("\n>>> STARTING MISSION <<<")
    
    print("\n1. APPROACHING...")
    move_wrist("PITCH_UP", 0.3)
    kickstart_away()
    go_to(POS_CRUISE_REACH, timeout=12.0) 
    
    print("\n2. GRABBING...")
    grip_control("OPEN", POS_REACH, 1.5)
    active_hold(POS_REACH, 0.2)
    go_to(POS_REACH) 
    active_hold(POS_REACH, 0.5) 
    
    grip_control("CLOSE", POS_REACH, 2.0)
    active_hold(POS_REACH, 0.5) 
    
    print("\n3. RETRACTING...")
    move_wrist("PITCH_DOWN", 0.3)
    go_to(POS_CRUISE_REACH) 
    
    print("\n4. TRANSPORTING...")
    if abs(pos[0] - POS_CONVEYOR[0]) > 500:
        kickstart_home() 
    go_to(POS_CRUISE_CONV) 
    
    print("\n5. DROPPING...")
    go_to(POS_CONVEYOR) 
    active_hold(POS_CONVEYOR, 0.5)
    
    grip_control("OPEN", POS_CONVEYOR, 1.5) 
    
    print("   (Backing away...)")
    go_to(POS_CRUISE_CONV) 
    
    grip_control("CLOSE", POS_CRUISE_CONV, 2.0) 
    
    print("\n6. RETURNING HOME...")
    go_to([POS_CONVEYOR[0], 0, 0])
    
    print("   (Kicking Base Home...)")
    kickstart_home()
    go_to(POS_HOME)
    
    print("   (Forcing Shoulder to Back Wall...)")
    set_motor(SHL_RPWM, SHL_LPWM, 45000) 
    time.sleep(0.5)
    
    print("\n>>> SHUTTING DOWN MOTORS <<<")
    set_motor(BASE_RPWM, BASE_LPWM, 0)
    set_motor(SHL_RPWM, SHL_LPWM, 0)
    set_motor(ELB_RPWM, ELB_LPWM, 0)
    
    pos = [0, 0, 0] 
    print("   (True Zero Locked!)")
    print("\n>>> MISSION COMPLETE <<<")
