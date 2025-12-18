from machine import Pin
from time import sleep

led = Pin('WL_GPIO0', Pin.OUT)

while True:
    led.toggle()
    sleep(0.5)
