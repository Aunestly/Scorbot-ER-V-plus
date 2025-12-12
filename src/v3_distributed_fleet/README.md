# Phase 3: Distributed Fleet Architecture

## 🔄 System Evolution
This phase represents the core engineering challenge of the project: **Scaling from a single device to a distributed network.**

This transition occurred in two distinct stages (3A and 3B), documenting the shift from a "Direct-Drive" topology to a "Bus-Based" topology to overcome physical hardware limitations.

---

## 🟢 Sub-Phase 3A: Direct GPIO Fleet
**"The Proof of Concept"**

In the initial fleet integration, the Raspberry Pi 4 communicated with the Picos, but the Picos controlled the motors by toggling their own GPIO pins directly.

* **Architecture:** `Pi 4` -> `USB` -> `Pico` -> `GPIO` -> `H-Bridge`
* **Limitation:** This approach worked for basic movements but instantly exhausted the Pico's available pins. We could not add limit switches or a second axis without running out of connections.
* **Code Characteristic:** The `main.py` file contains direct `Pin(x, Pin.OUT)` commands.

---

## 🔵 Sub-Phase 3B: I/O Expander Fleet
**"The Scalable Solution"**

To solve the pin shortage, I refactored the entire hardware abstraction layer (HAL) to use the **I2C Protocol**. Instead of using 4 pins per motor, the Pico now uses just 2 pins (SDA/SCL) to control *infinite* motors via addressable chips.

* **Architecture:** `Pi 4` -> `USB` -> `Pico` -> `I2C Bus` -> `MCP23017` -> `H-Bridge`
* **Improvement:** This reduced pin usage by 90%, allowing for the addition of 12 limit switches and a second robotic arm on the same network.
* **Code Characteristic:** The `main.py` file imports `mcp23017.py` and sends hex commands (e.g., `0x20`) instead of toggling pins.

## 📊 Comparison of Methodologies

| Feature | Phase 3A (Direct) | Phase 3B (Expander) |
| :--- | :--- | :--- |
| **Connectivity** | 1 Wire per Signal | 2 Wires for *All* Signals (Bus) |
| **Complexity** | Low (Simple logic) | High (Requires Driver Library) |
| **Scalability** | Low (Max 6 Motors) | High (Max 128 Motors) |
| **Safety** | Software Stops | Hardware Stops + Watchdogs |

## 📂 Navigation
* **[View Phase 3A Code](./v3a_direct_gpio_fleet/)** - The Direct Drive implementation.
* **[View Phase 3B Code](./v3b_io_expander_fleet/)** - The Final I2C implementation.
