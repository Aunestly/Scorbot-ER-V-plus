# File: mcp23017.py
# Description: Driver for MCP23017 I/O Expander
# Save this on BOTH Picos.

class MCP23017:
    IODIRA = 0x00
    IODIRB = 0x01
    GPIOA = 0x12
    GPIOB = 0x13

    def __init__(self, i2c, address=0x20):
        self.i2c = i2c
        self.address = address
        # Initialize all pins as outputs (0x00)
        try:
            self.i2c.writeto_mem(self.address, self.IODIRA, b'\x00')
            self.i2c.writeto_mem(self.address, self.IODIRB, b'\x00')
        except OSError:
            print(f"ERROR: Could not find Expander at {hex(address)}")

    def digital_write(self, pin, value):
        # Maps 0-7 to Port A, 8-15 to Port B
        reg = self.GPIOA if pin < 8 else self.GPIOB
        pin_offset = pin % 8
        
        # Read current state so we don't mess up other pins
        current_state = self.i2c.readfrom_mem(self.address, reg, 1)[0]
        
        if value == 1:
            new_state = current_state | (1 << pin_offset)
        else:
            new_state = current_state & ~(1 << pin_offset)
            
        self.i2c.writeto_mem(self.address, reg, bytes([new_state]))
