import sys
import select
import time
import arm1

continuous_mode = False

print("ARM1_CORE_ONLINE")

while True:
    # 1. Non-blocking check for Serial Commands
    if select.select([sys.stdin], [], [], 0)[0]:
        command = sys.stdin.readline().strip()
        
        if command == "WHO_ARE_YOU":
            print("ARM1")
            
        elif command == "START":
            print("CONTINUOUS_MODE_ON")
            continuous_mode = True
            arm1.stop_requested = False
            
        elif command == "STOP":
            print("EMERGENCY_STOP_TRIGGERED")
            continuous_mode = False
            arm1.stop_requested = True
            # Kill power immediately
            arm1.set_motor(arm1.BASE_RPWM, arm1.BASE_LPWM, 0)
            arm1.set_motor(arm1.SHL_RPWM, arm1.SHL_LPWM, 0)
            arm1.set_motor(arm1.ELB_RPWM, arm1.ELB_LPWM, 0)

    # 2. If in continuous mode, run the cycle
    if continuous_mode:
        arm1.run_cycle()
        
        # After one cycle, check if we should wait or if we were stopped mid-way
        if continuous_mode:
            print("CYCLE_COMPLETE_WAITING_3S")
            time.sleep(3.0) 
        else:
            print("ARM1_HALTED")

    time.sleep(0.01) # High speed loop
