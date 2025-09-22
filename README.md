# Scorbot-ER-V plus with Conveyor Belt
two vertical articulated robots, with five revolute joints. Gripper attached and five degrees of freedom, and a conveyor belt.

## Table Of Contents
- [Project Overview](https://github.com/Aunestly/Scorbot-ER-V-plus/blob/main/README.md#project-overview)
- [Possible Technologies](https://github.com/Aunestly/Scorbot-ER-V-plus/blob/main/README.md#possible-technologies)
- [Software](https://github.com/Aunestly/Scorbot-ER-V-plus/blob/main/README.md#software)
- [Safety Precautions](https://github.com/Aunestly/Scorbot-ER-V-plus?tab=readme-ov-file#safety-precautions)
- [Hardware Test]()
- [Objective](https://github.com/Aunestly/Scorbot-ER-V-plus/blob/main/README.md#objectives)
- [Methodology](https://github.com/Aunestly/Scorbot-ER-V-plus/blob/main/README.md#potential-methodology)
- [Goals](https://github.com/Aunestly/Scorbot-ER-V-plus/blob/main/README.md#goals)
- [Results]()
- [Key Findings]()
- [Visualizations]()
- [Equipment](https://github.com/Aunestly/Scorbot-ER-V-plus/blob/main/README.md#equipment)
- [Future Work]()
- [Individual Contributions]()
- [Acknowledgement](https://github.com/Aunestly/Scorbot-ER-V-plus/blob/main/README.md#acknowledgement)

## Project Overview
Engineer, design and build a custom controller box from the ground up for a SCORBOT-ER V Plus robotic arm and conveyor belt system. The goal is to replace the original, outdated controller with a flexible, powerful, and cost effective system built on contemporary components and open-source software. 

## Possible Technologies
- SCORBOT-ER V Plus
- H-Bridge Modules
- MCP23017 I/O Expander
- Optical Quadrature Encoders
- Fused Power Distribution System
- 
## Software
- Micropython 
- Thonny IDE
- Custom Libraies
- Gemini AI

## Safety Precautions
### High Current
- Risks: The 12V 50A power supply can deliver a huge amount of energy. A short circuit in my wiring or failed motor could cause wires to melt and components to burn out instantly.
 <br><br>  _Precaution:_ The fuse block and 5A blade fuses are our essential safety net. They are the first line of defense and will instantly cut the power to a faulty circuit before any serious damage can occur. Using thick 12-14 AWG for all 12V connections is also a critical part of this.

### Operator Error Protection
- Risks: When controlling the arm manually with the joystick, a momonet of distraction or an accidental twitch could send the arm crashing into itself or its surroundings.
 <br><br> _Precaution:_ The "Dead Man's Switch" logic in the code is the most important operational safety feature. The arm should be programmed to be completely limp and powerless unless im actively holding down the joysticks button. If I let go for any reason, the arm must freeze instantly

### Software "Guardrails" 
- Risks: If we accidentally write a command in our autonomous sequence that tells a joint to move past its physical limits (eg., move_joint_to_position(1,99999)). This will cause the arm to jam, stall the motor, and potentiallly break gears
<br><br>  _Precautions:_ Implement "soft stops" in our code from day one, our program must have a defined list of the safe minimum and maximum encoder values for each joint. Our move_to_joint_position() function must always check these limits before it starts moving the motor. If a command is outside the safe zone, the function should refuse to execute it and print an error message.
  
- Risk: A command could tell a joint to move past its physical limits, causing the arm to jam, stall a motor, and potentially break a gear.
<br><br>  _Precaution:_ The "Soft Stops" in the code are essential. Our program must know the safe minimum and maximum encoder values for each joint. Before moving a motor , the code should always check if the joint is already at its limit. If so, the code should ignore the command.

## Emergency Stop Plan
- if I upload new code, and a hidden bug causes the arm to start moving erratically
  <br><br> _Precaution:_ Have a clear and immediate way to shut everything down. The easiest way is to have our 12V power supply plugged into a power strip with a switch. Keep the power strip within arm's reach at all times during testing. If anything goes wrong, I can slap the switch to cut all power to the motors. 
# Hardware Test
# Main Power Circuit (12V): 
# Provides the high-current power to drive the motor
- 12V PSU (+) Terminal → Fuse Block Main Positive Input.
- 12V PSU(-) Terminal → Fuse Block Main Negative Input
- Fuse Block Fused Output → H-Bridge B+ (Battery Positive) screw terminal.
- Fuse Block Negative Bus Bar → H-bridge B- (Battery Negative) screw terminal
# Logic Power Circuit (5V): 
# Provides the brain of your H-bridge module.
- Pico W VBUS Pin → H-bridge VCC pin.
# Control Signals Circuit: 
# The command wires from the pico’s brain to the H-bridge.
- Jumper Wires from Pico W GP14 → H-Bridge RPWM 
- Jumper Wires from Pico W GP13 → H-Bridge LPWM
- Jumper Wires from Pico W GP16 → H-Bridge R_EN (Right Enable)
- Jumper Wires from Prico W GP17 → H-Bridge L_EN(Left Enable)
## Motor Output Circuit: 
# The final path where switched power travels to the motor
- H-Bridge Motor Positive → DB50 Breakout Terminal #17
- H-Bridge Motor Negative → DB50 Breakout Terminal #50
# Shared Ground
# Provides the high-current power to drive the motor
- A jumper wire from PICO W GND Pin to the Fuse Blocks Negative Bus Bar.
- A jumper wire from PICO W GND Pin to H-Bridge GND Pin.

## Objectives
- Physically mount the Raspberry Pi Pico W, 6 H-Bridges, 1 x 2- Relay modules, fuse block, and buck converter into a single organzied enclosure.
- Correctly wire the 12 V power system from the main power supply, through the fuse block, to all H-bridges and the relay module using appropriate gauge wire.
- Sucessfully create and test the 5V power system using the buck converter.
- Complete all low-voltage signal wiring between the Raspberry Pi Pico W and the inputs of the H-bridges and relay module.
- Systematically identify and document the two wires for each of the six motors
- Identify and document the four wires (VCC, GND, Channel A, Channel B) for each of the six encoders.
- Identify and document the wires for each of the home switches.
- Produce a final, verified chart that maps every necessary wire from the robot's DB50 connector to a specific terminal on my breakout board.
- Sucessfully read all six encoders simultaneously and accurately using the Raspberry Pi Pico W's PIO feature.
- Write and test basic open-loop code to control the speed and direction of a single motor.
- Implement and tune a stable PID contr0l loop for one joint, allowing it to move to a target position and hold it firmly.
- Expand the PID control system to manage all six joints concurrently
- Create a simpler user interface (e.g., via serial commands from my computer) to command the robot to move to a specific coordinates or positions.

  ## Potential Methodology
  1. Physical Layout: Design a Layout for all components within my chosen enclosure
  2. Mounting: Securely mount the Raspberry Pi Pico, all 6 H bridge modules, the 2-Relay module, the fuse block, the 12V-to-5V buck converter and any terminal blocks.
  3. Wiring: Using thick 12 or 14 AWG wire, connect mg main 12V power supply to the input of our fuse block
  4. Run Individual 12V Power and ground wires from the fused outputs of the fuse blcok to the + 12V and GND inputs of each of the 6 H-bridges and the 2-relay module.
  5. Wire the 5V Low-Power Circuit: Connect the input of my buck converter to one of the fused 12V outputs on our fuse blocks
  7. Adjust the buck converter to ensure its output is a stable 5V
  8. Run the 5V and ground wires from the buck converter's output to a dedicated terminal block. This weill be where we connect the encoder power lines later.
  9. Wiring the 3.3V Signal Logic: Using standard jumper wires, connect GPIO pins from the Raspberry Pi Pico to the control input pins (IN1, In2, ENA, etc.) of all six H-bridges.
  10. Connect trwo additional GPIO pins from he pico to the input pins of the 2-realy module for the conveyor
  11. Keep a detailed log of which GPIO pin is connected to which specific function
  12. Controller Bench Test: With the robot NOT connected. plug in and turn on our 12V power supply.
  13. Use a multimeter to confirm we have a stable 12V at the H-bridges and a stable 5V at the designated encoder power terminals.
  14. Plug the Pico W into my computer and run a simple "blink" script to ensre it is powered and functioning correctly.
  15. Set up for testing: Connect the SCORBOT's large DB50 Cable to my DB50 breakout board. I will perform all testing on the screw terminals of the breakout board,
  16. Identify Motor Wires: Use a multimeter in resistance mode to find pairs of terminals with low resistance.
  17. Once a pair is found, confirm its a motor by briefly applying 9V from a battery and observing which joint moves.
  18. Label the pair and repeat until all 6 motor pairs are found and documented.
  19. Identify Home switch wires: Manually move a robot joint unitil its home switch clicks.
  20. Use our multimeter in continuity mode to find the pair of (as-yet-unidentified) terminals that show a change (from open to closed, or vice versa)
  21. Label the pair and repeat for all 6 axes.
  22. Identify encoder wires: connect the 5V and ground from my controller's buck converter to a suspected VCC/GND pair among the remaining wires.
  23. Connect suspected signal wires (Channels A and B) to input pins on my Pico W.
  24. Run a simple script to monitor the pins and slowly turn the corresponding joint by hand. The correct wires will show the characteristic square-wave pulses of a quadrature encoder.
  25. Label the VCC, GND, A, and B wires and repeat for all 6 encoders.
  26. Create Master Pin OUt chart: Compile all my findings into a final, clean, document that maps every pin on the DB50 breakout board to its specific function. This chart is the master reference for the project.
  27. Set Up a MicroPython Environment: Install the Micropython firmwar on my Raspberry Pi Pico W
  28. Establish a connection using Thonny IDE.
  29. Open Loop Motor Test: Connect our controller to the robot arm/
  30. Write a simple program to control just one motor. The program should have functions to run the motor forward, backward, and at different speeds using PWM, without any geedback from the encoders.
  31. Encoder Reading Test: Write a program that uses a PIO state machine to read the encoder count from that same joint. The program should just print the live encoder position to the screen as I move the joint by hand.
  32. Combine the logic from steps 12 and 13.
  33. Implement a PID control algorithm that takes a "target position" (an encoder count) as an input. The algorhithm will use the live encoder reading to automatically calculate the required. motor speed and direct to reach the target and hold it there.
  34. PID Tuning: Carefully tuned the P, I, and D constants for that one joint until its movement is fast, accurate and stable with minimal overshoot or oscillation.
  35. Expand to all joints: expand my software architecture to handle all six joints. Each jiont will need its own set of tuned PID constants for that one joint until its movement is fast, accurate, and stable with minimal overshoot or oscillation.
  36. Establish WiFi Connection: Write a MicroPython script that connects my Raspberry Pi Pico W, to my local WiFi network using my  network's SSID and password.
  37. Develop Wireless Command Interface: We will create a simple server on the Pico W. A great option is a basic web server that hosts a simple webpage with buttons like "Move Joint 1 Forward," "Home Robot," etc.
  38. When I click a button on the webpage from another computer's browser, it will send a command to the Pico W.
  39. Integrate Control and Network Code: Mergemy PID control code with my new wireless server code. The server's job will be able to receive a wireless command and then call the appropriate function in my PID control Systen. (e.g., (joint=3, position=5000))
  40. Implement Homing Sequence: Write a final routine that, on startup or when a "Home" command is received wireelssly, slowly moves each joint until its home switch is triggered. This is supposed to zero the encoder counts and give the robot a known starting position.

## Goals
- Build a safe, reliable and fully wired custom controller box that can deliver power to all robotic components.
- Create a complete and accurate "pinout map" of the SCORBOT's 50-pin connector making the robot wiring fully understood.
- Then wire Micropython that achieves stable, precise and command-based control over all six joints of the SCORBOT arm.



## Visualizations

## Equipment:
1. Controller: 1 x Raspberry Pi Pico W Microcontroller
2. Power Supply: 1 x 12V 50A power supply
3. Safety: 6 Way fused distribution block**
4. Safety: 12-14 AWG wire
5. Blade Fuses.**
6. Robot Arm Drivers: 6 x L28N H-bridge modules
7. Conveyor Driver: 1 x 2-Relay Module
8. Interface: BRKDD50FV2-D50 Connector
9. Power Conversion: 1 x DCDC Buck Converter
10. Terminal Block: Weidu TB2506
11. Soder bread board.
12. Adafruit MCP23017 I2C GPIO Expander Breakout

## Individual Contribution

## Acknowledgement
<p> I'd like to extend my sincere gratitiude to the entire team. This project would not have been possible without the ressources and support of CS Robotics Lab. Special thanks for providing access to the SCORBOT-ER V Plus Robotic arms, workbench space, and essential tools required for builiding the custom controller.Their generosity in providing the tools and supploes for the success of this project. The supportive and innovative environment of the lab was a constant source motivation </p>
<p>
I would like to acknowledge the assitance of GOogle's Gemini, a large language model, which was instrumental in the development of this project. The AI provided support in areas such as:
<br>- code generation for the m MicroPython control system,
<br>- debugging of hardware communication protocols,
<br>- conceptual brainstorming for the project's methodology,
<br>- drafting of project documentation. 
