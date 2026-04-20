
# File: main.py (SAVE ON ARM 1 PICO)
import sys
import select
import time
import arm1

while True:
    # Listen to the USB serial port from the main computer
    if select.select([sys.stdin], [], [], 0)[0]:
        command = sys.stdin.readline().strip()
        
        # 1. Identity Check for the Pi
        if command == "WHO_ARE_YOU":
            print("ARM1")
            
        # 2. Execution Command
        elif command == "RUN" or command == "START":
            arm1.run_cycle()
            print("ARM1_READY")
            
    time.sleep(0.1)  
