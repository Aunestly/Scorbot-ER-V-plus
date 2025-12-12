# Phase 1: Hardware Validation & Component Testing

## 🔬 Objective
Before attempting complex motion control, this phase focused on validating the individual electronic components to ensure they were functional and correctly wired. This "Unit Testing" approach minimized debugging variables in later phases.

## 🛠️ Hardware Tested
1.  **Raspberry Pi Pico W:** Verified firmware installation and internal LED control.
2.  **BTS7960 H-Bridge:** Verified logic level switching (3.3V signals triggering 12V output).
3.  **12V DC Motors:** Verified bidirectional rotation and current draw.
4.  **Quadrature Encoders:** Verified A/B phase signaling for position tracking.

## 📄 Validation Scripts

### 1. `blink_test.py` (The "Hello World")
* **Purpose:** Confirm MicroPython firmware is running and the Pico is alive.
* **Action:** Toggles the onboard LED (Pin "LED") every 0.5 seconds.
* **Result:** [SUCCESS] - Pico W confirmed operational.

### 2. `motor_test_class.py` (The Driver Check)
* **Purpose:** Test the custom `Motor` class abstraction layer.
* **Logic:**
    * Initialize a motor on dummy pins.
    * Call `.forward()` -> Check if RPWM is High.
    * Call `.backward()` -> Check if LPWM is High.
* **Result:** [SUCCESS] - Logic correctly toggles GPIO states.

### 3. `encoder_finder.py` (The Sensor Check)
* **Purpose:** Identify which wires in the legacy DB50 cable correspond to Encoder A/B channels.
* **Methodology:**
    * The script prints the raw state (0 or 1) of a specific GPIO pin to the console.
    * Manually rotating the motor shaft causes the state to flip.
* **Result:** [SUCCESS] - Mapped all 6 encoders (Base, Shoulder, Elbow, Pitch, Roll, Gripper) to the DB50 breakout board.

## 🔌 Connection Diagrams
* **LED Test:** Internal Connection.
* **Motor Test:** Pico GPIO -> BTS7960 (Logic) -> Multimeter (Output).

## 🏁 Phase 1 Conclusion
All critical subsystems (Compute, Actuation, Sensing) passed individual unit tests. The project is cleared to proceed to **Phase 2: Closed-Loop Control Integration**.
