from machine import Pin, PWM
import time

#Pin initialization with debugging
print("[DEBUG] Entering pin initialization block...")

pins_initializated_successfully = False
try:
    print("[DEBUG] Initializing GP14 as rpwm_pin...")
    rpwm_pin = Pin(14, Pin.OUT)
    print("[DEBUG] Initializing GP13 as lpwm_pin...")
    lpwm_pin = Pin(13, Pin.OUT)
    print("[DEBUG] Initializing GP16 as r_en_pin...")
    r_en_pin = Pin(16, Pin.OUT)
    print("[DEBUG] Initializing GP17 as l_en_pin...")
    l_en_pin = Pin(17, Pin.OUT)
    
    pins_initialized_successfully = True
    print("SUCCESS: All control pins initialized without error...")
    
except Exception as e:
    print(f" - Details: {e}")
    
    #motor control functions feedback
def motor_forward():
    print("Action: Moving Forward...")
    rpwm_pin.value(1)
    lpwm_pin.value(0)
    r_en_pin.value(1)
    l_en_pin.value(1)
    print(f" - [DEBUG] Pin States -> RPWM: {rpwm_pin.value()}, LPWM: {lpwm_pin.value()}, R_EN: {r_en_pin.value()}, L_EN: {l_en_pin.value()}")
    
def motor_backward():
    print("ACTION: Moving Backward...")
    rpwm_pin.value(0)
    lpwm_pin.value(1)
    r_en_pin.value(1)
    l_en_pin.value(1)
    print(f" - [DEBUG] Pin States -> RPWM: {rpwm_pin.value()}, LPWM: {lpwm_pin.value()}, R_EN: {r_en_pin.value()}, L_EN: {l_en_pin.value()}")
def motor_stop():
    print("ACTION: Stopping Motor...")
    rpwm_pin.value(0)
    lpwm_pin.value(0)
    r_en_pin.value(0)
    l_en_pin.value(0)
    print(f" - [DEBUG] Pin States -> RPWM: {rpwm_pin.value()}, LPWM: {lpwm_pin.value()}, R_EN: {r_en_pin.value()}, L_EN: {l_en_pin.value()}")
    
#main test sequence
if pins_initialized_successfully:
    print("\nStarting SCORBOT Motor Hardware Test")
    
    try:
        print("[DEBUG] Entering main test sequence 'try' block...")
        motor_forward()
        print("[DEBUG] motor_forward() call complete.")
        
        print("[DEBUG] Starting 3-second sleep...")
        time.sleep(3)
        print("[DEBUG] 3-second sleep complete.")
        
        print("[DEBUG] Calling motor_stop...")
        motor_stop()
        print("[DEBUG] motor_stop() call complete.")
        
        print("[DEBUG] Starting 2-second sleep...")
        time.sleep(2)
        print("[DEBUG] 2-second sleep complete.")
        
        print("[DEBUG] Calling motor_backward()...")
        motor_backward()
        print("[DEBUG]motor)backward() call complete")
        
        print("[DEBUG] Starting 3-second sleep...")
        time.sleep(3)
        print("[DEBUG] 3-second sleep complete.")
        
        print("[DEBUG] Main test sequence finished successfully.")
        
    finally:
        print("[DEBUG] Entering 'finally' block for safety cleanup...")
        motor_stop()
        print("---test complete---")
else:
    print("\n--- Test Aborted: Pink initialization failed. ---")
  
 
