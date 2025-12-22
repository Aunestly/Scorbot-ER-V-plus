# File: mcp23017.py
# Save this on the Pico. Do NOT run it.

import time

class MCP23017:
    def __init__(self, i2c, address=0x20):
        self.i2c = i2c
        self.address = address
        self.init()

    def init(self):
        # Configure IODIR to 0 (all outputs) initially
        self.write_reg(0x00, 0x00) # IODIRA
        self.write_reg(0x01, 0x00) # IODIRB

    def write_reg(self, reg, value):
        self.i2c.writeto_mem(self.address, reg, bytes([value]))

    def read_reg(self, reg):
        return self.i2c.readfrom_mem(self.address, reg, 1)[0]

    def pin(self, pin, mode=None, value=None):
        # Determine port (A or B) and pin bit (0-7)
        # Pins 0-7 are Port A, Pins 8-15 are Port B
        reg_gpio = 0x12 if pin < 8 else 0x13
        reg_iodir = 0x00 if pin < 8 else 0x01
        bit = pin % 8

        # Set Mode (0=Output, 1=Input) if provided
        if mode is not None:
            current_iodir = self.read_reg(reg_iodir)
            if mode == 1:
                new_iodir = current_iodir | (1 << bit)
            else:
                new_iodir = current_iodir & ~(1 << bit)
            self.write_reg(reg_iodir, new_iodir)

        # Set Value (0=Low, 1=High) if provided
        if value is not None:
            current_gpio = self.read_reg(reg_gpio)
            if value == 1:
                new_gpio = current_gpio | (1 << bit)
            else:
                new_gpio = current_gpio & ~(1 << bit)
            self.write_reg(reg_gpio, new_gpio)
