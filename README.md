# SCORBOT-ER V Plus Controller Modernization

> **Portfolio Link:** [https://aunestly.github.io]

![Project Banner](https://github.com/Aunestly/Scorbot-ER-V-Hardware-Test/blob/95b3f52d41798fb5e0a2a74700c69d04ce0dbfac/IMG_8894.png)

## 📖 Executive Summary
**Architected a system evolution from a tethered legacy prototype to a standalone distributed computing model.**

This project engineered a custom, dual-arm control system for SCORBOT-ER V Plus robotics, leveraging AI-augmented research to design and fabricate a modernized control panel integrating high-current drivers and distributed microcontrollers. By deploying a Raspberry Pi 4 as the central process controller, I orchestrated multiple robotic arms via serial communication, effectively transforming "dark data" (legacy hardware) into a programmable, modern Cyber-Physical System.

---

## 📂 Repository Structure
This repository is organized by engineering phase, documenting the evolution from simple hardware validation to complex fleet management.

```text
SCORBOT-ER-V-Plus-Modernization/
│
├── README.md                          # The Main Executive Summary (Portfolio Landing Page)
│
├── src/                               # Source Code Repository
│   │
│   ├── v1_hardware_validation/        # PHASE 1: Component Verification
│   │   ├── blinkLED.py                # Simple LED test
│   │   ├── motortestoriginal.py       # Single motor class test
│   │   └── encoder_finder.py          # Script to identify A/B encoder phases
│   │
│   ├── v2_standalone_control/         # PHASE 2: Single Arm Prototype (Laptop Controlled)
│   │   ├── README.md                  # Doc: Explains the "Direct Drive" wiring (Hardwired Enables)
│   │   └── 4cycle.py                  # The Open-Loop "Forward/Back" validation loop
│   │
│   ├── v3_distributed_fleet/          # PHASE 3: The Fleet Architecture
│   │   ├── README.md                  # Doc: Explains evolution from 3A (Direct) to 3B (Expander)
│   │   │
│   │   ├── v3a_direct_gpio_fleet/     # SUB-PHASE 3A: The "Pin-Constrained" Prototype
│   │   │   ├── fleet_manager.py       # Python: Controls 2 Picos, runs 4-motor sequence
│   │   │   └── pico_code/             # MicroPython: Code for the Picos
│   │   │       ├─ arm_1/main.py       # Listener: ARM 1 Controls motors via GP0-GP7 (Direct)
|   |   |       └─ arm_2/main.py       # Listener: ARM 2 Controls motors via GP0-GP7
│   │   │
│   │   └── v3b_io_expander_fleet/     # SUB-PHASE 3B: The "Production" System (Scalable)
│   │       ├── fleet_manager.py       # Python: Complex mission (Arm 1 Base -> Arm 2 Task)
│   │       └── pico_code/             # MicroPython: Code for the Picos
│   │           ├── mcp23017.py        # Library: The I2C Driver (Standard for both)
│   │           ├── arm1/main.py       # Arm 1 Logic: Hybrid (Expander + Direct Pins)
│   │           └── arm2/main.py       # Arm 2 Logic: Dual Expander (0x20, 0x21)
│   │
│   └── v4_autonomy_vision/            # PHASE 4: Computer Vision (Future Roadmap)
│       ├── training_data/             # Placeholder for images
│       └── vision_control.py          # Placeholder for logical control
│
└── tests/                             # Verification Logs
    └── logs/                          # Save your "Terminal Output" text files here
```

-----
## 🧰 Hardware and Software Supply

### Hardware Components
- **2x SCORBOT-ER V Plus** robotic arm
- **1x Conveyor built** transport
- **1x Raspberry Pi 4** (Fleet Manager)  
- **2x Raspberry Pi Pico W** (Distributed Controllers)
- **2x MCP23017 IO Expanders** Pin expansion
- **12x BTS7960 H-Bridge Drivers** for high-current motor control  
- **2x DB50 Breakout Board** for legacy interface mapping  
- **2x 6-Way Fuse Block** for power distribution  
- **1x 12V DC Power Supply** for motors  
- **1x Buck Converter** for logic-level voltage regulation  
- **50+ Jumper Wires & Terminal Blocks** for signal routing
- **4x Terminal Blocks** for signal routing  

### Software Tools
- **Python 3.x** for control logic and orchestration  
- **MicroPython** for Pico W firmware  
- **I2C and UART Protocols** for communication  
- **LabelImg** for dataset annotation (Computer Vision phase)  
- **TensorFlow Lite** for object detection (Future roadmap)  
- **Git & GitHub** for version control and collaboration  



## 📊 Master Pinout & Data Architecture

To manage the complexity of the legacy 50-pin interface, I normalized the hardware connections into a relational dataset. This abstracts physical wiring into logical addresses for the software.

### Master DB50 Pinout Map

*The following mapping was verified using multimeter continuity testing against legacy documentation. This schema represents the final "Production" architecture utilizing dual I/O expanders.*

| Axis | Component | DB50 Pin (+) | DB50 Pin (-) | Controller Logic | Address/Pin |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Axis 1** | Base Motor | 50 | 17 | Expander 1 (0x20) | `GPA0` - `GPA3` |
| | Base Encoder | 2 (A) | 5 (B) | Pico Direct | `GP18` / `GP19` |
| | Base Home | 23 (Sig) | 33 (GND) | Pico Direct | `GP22` |
| **Axis 2** | Shoulder Motor | 49 | 16 | Expander 1 (0x20) | `GPA4` - `GPA7` |
| | Shoulder Encoder | 1 (A) | 21 (B) | Pico Direct | `GP20` / `GP21` |
| | Shoulder Home | 7 (Sig) | 32 (GND) | Pico Direct | `GP26` |
| **Axis 3** | Elbow Motor | 48 | 15 | Expander 1 (0x20) | `GPB0` - `GPB3` |
| | Elbow Encoder | 36 (A) | 4 (B) | Pico Direct | `GP27` / `GP28` |
| | Elbow Home | 24 (Sig) | 31 (GND) | Pico Direct | `GP16` |
| **Axis 4** | Wrist Pitch | 47 | 14 | Expander 2 (0x21) | `GPA1` - `GPA4` |
| | Pitch Encoder | 35 (A) | 20 (B) | Pico Direct | `GP17` / `GP15` |
| | Pitch Home | 8 (Sig) | 30 (GND) | Pico Direct | `GP14` |
| **Axis 5** | Wrist Roll | 46 | 13 | Expander 2 (0x21) | `GPB4` - `GPB7` |
| | Roll Encoder | 18 (A) | 3 (B) | Pico Direct | `GP13` / `GP12` |
| | Roll Home | 6 (Sig) | 29 (GND) | Pico Direct | `GP11` |
| **Axis 6** | Gripper Motor | 45 | 12 | Expander 1 (0x20) | `GPB4` - `GPB7` |
| | Gripper Encoder | 34 (A) | 19 (B) | Pico Direct | `GP10` / `GP9` |
| **Aux** | Conveyor Relay | N/A | N/A | Expander 2 (0x21) | `GPB0` / `GPB1` |

**Power Distribution Notes:**

  * **Encoder Power (VLED):** All encoders connect to the common **5V Rail** on pins 11, 27, 10, 26, 9, 25.
  * **Common Ground:** All sensor grounds connect to the **Negative Bus Bar**.

-----

## 🛠️ Engineering Methodology

### 1. Direct GPIO Hardware Interface (Prototype Phase)

For the initial multi-axis cyclic tests (`4cycle.py`), the system utilized a **Direct-Drive Topology**. The Raspberry Pi Pico W served as the centralized motion controller, interfacing directly with four independent BTS7960B H-Bridge drivers. This configuration bypassed the I2C bus to minimize latency and isolate variables during the initial motion sequencing validation.

  * **Signal Mapping:** GPIO pins were assigned in contiguous blocks to optimize routing. For example, the Base Axis utilized the lower-mid section of the Pico header, while the Elbow Axis utilized the upper section to physically separate signal paths.
  * **Abstraction:** The control logic utilized a custom `Motor` class acting as a **Hardware Abstraction Layer (HAL)**. This allowed the software to define high-level behaviors (e.g., `shoulder.forward()`) which were dynamically translated into specific voltage states.

### 2. Distributed Fleet Architecture (Production Phase)

To scale beyond the pin limitations of a single microcontroller, I architected a **Distributed Control System**:

  * **The Brain (Raspberry Pi 4):** Acts as the central "Mission Control." It runs the main Python logic, calculates timing, and manages the fleet state. It communicates via USB Serial (UART) to multiple subordinates.
  * **The Spinal Cords (Pico W):** Act as real-time hardware controllers. They run a "Listener" loop that waits for serial commands (`MOVE_BASE`, `STOP`) and handles the high-speed GPIO switching.
  * **Power Topology:** A Dual-Rail Power Architecture was implemented to isolate high-current inductive loads (12V Motors) from sensitive logic components (5V/3.3V). A common ground reference was established at the fuse block to ensure signal integrity across the distributed system.

-----

## 🚀 Future Roadmap: Closed-Loop Autonomy

The next phase introduces "Visual Autonomy" using the **Google Data Analytics Process**:

1.  **Collect:** Capture image datasets of target objects via Pi Camera.
2.  **Process:** Annotate images using LabelImg to define bounding boxes.
3.  **Analyze:** Train a TensorFlow Lite model for object detection.
4.  **Act:** Convert pixel coordinates into motor step commands for precise pick-and-place operations.



