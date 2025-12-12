# Phase 2: Standalone Control & Hardware Validation

## 🎯 Objective
The goal of this phase was to establish a baseline **Direct-Drive Topology**. Before introducing the complexity of the distributed fleet architecture (Phase 3), we needed to validate the electromechanical performance of the SCORBOT-ER V Plus 12V motors and the BTS7960 drivers using a single microcontroller.

## ⚙️ Hardware Configuration
* **Controller:** 1x Raspberry Pi Pico W (Standalone)
* **Drivers:** 4x BTS7960 High-Current H-Bridges
* **Communication:** USB Serial (REPL) via Thonny IDE
* **Wiring Strategy:** **Direct GPIO**
    * Unlike the later production phases, this phase bypassed I/O expanders.
    * Each motor control line (`RPWM`, `LPWM`, `R_EN`, `L_EN`) was wired directly to the Pico's GPIO pins to minimize latency and isolate signal variables.

## 📄 Key Scripts

### `4cycle.py`
This is the core validation script for this phase. It implements an **Open-Loop Control Sequence** to stress-test the mechanical linkages and power delivery.

**The Sequence Logic:**
1.  **Forward:** Drive motor at 100% duty cycle for `T` seconds.
2.  **Active Brake:** Pull both `RPWM` and `LPWM` LOW while keeping Enables (`R_EN`, `L_EN`) HIGH. This engages the H-Bridge's internal braking to stop momentum instantly.
3.  **Reverse:** Drive motor in reverse at 100% duty cycle.
4.  **Stop:** Full system idle.

## 🔌 Wiring Map (Prototype)
*This mapping is specific to the Phase 2 validation prototype. Note that the Enable pins are "Hard-Wired" High to save GPIO pins.*

| Motor | Pico Pin (RPWM) | Pico Pin (LPWM) | R_EN & L_EN | Logic |
| :--- | :--- | :--- | :--- | :--- |
| **Base** | GP0 | GP1 | **3.3V (Physical Pin 36)** | Direct Drive |
| **Shoulder** | GP2 | GP3 | **3.3V (Physical Pin 36)** | Direct Drive |
| **Elbow** | GP4 | GP5 | **3.3V (Physical Pin 36)** | Direct Drive |
| **Gripper** | GP6 | GP7 | **3.3V (Physical Pin 36)** | Direct Drive |

**Wiring Note:**
* All `R_EN` and `L_EN` pins from all 4 drivers were daisy-chained together and connected to the single **3.3V (OUT)** pin on the Pico.
* This keeps the drivers "Armored" (Enabled) 100% of the time, allowing `RPWM` and `LPWM` to handle all motion and braking logic.
