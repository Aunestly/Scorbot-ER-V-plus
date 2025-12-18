# This code is to verify that each joint is still connected to its original pin
import machine
import time

channel_a = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
channel_b = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)

print("Slowly turn a robot joint by hand. Looking for pulses...")

#Remember the last state to only print when a change occurs
last_a = channel_a.value()
last_b = channel_b.value()
print(f"Initial State -> A: {last_a}, B: {last_b}")

while True:
    current_a = channel_a.value()
    current_b = channel_b.value()

    # Check if the state has changed before printing
    if current_a != last_a or current_b != last_b:
        print(f"Pulse Detected! -> A: {current_a}, B: {current_b}")
        last_a = current_a
        last_b = current_b
        
    # Check for changes 100 times per second    
    time.sleep(0.01) 
