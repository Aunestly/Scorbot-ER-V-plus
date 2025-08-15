# Scorbot-ER-V-plus
two vertical articulated robots, with five revolute joints. Gripper attached and five degrees of freedom, and a conveyor belt.

# Possible Technologies
- SCORBOT-ER 
- Thonny
- Micropython
- Gemini AI

# Project Overview
Engineer, design and build a custom controller box from the ground up for a SCORBOT-ER V Plus robotic arm and conveyor belt system. The goal is to replace the original, outdated controller with a flexible, powerful, and cost effective system built on contemporary components and open-source software. 

# Objectives
- Physically mount the Raspberry Pi Pico W, 6 H-Bridges, 1 x 2- Relay modules, fuse block, and buck converter into a single organzied enclosure.
- Correctly wire the 12 V power system from the main power supply, through the fuse block, to all H-bridges and the relay module using appropriate gauge wire.
- Sucessfully create and test the 5V power system using the buck converter.
- Complete all low-voltage signal wiring between the Raspberry Pi Pico W and the inputs of the H-bridges and relay module.
- Systematically identify and document the two wires for each of the six motors
- Identify and document the four wires (VCC, GND, Channel A, Channel B) for each of the six encoders.
- Identify and document the wires for each of the home switches.
- Produce a final, verified chart that maps every necessary wire from the robot's DB50 connector to a specific terminal on your breakout board.
- Sucessfully read all six encoders simultaneously and accurately using the Raspberry Pi Pico W's PIO feature.
- Write and test basic open-loop code to control the speed and direction of a single motor.
- Implement and tune a stable PID contrl loop for one joint, allowing it to move to a target position and hold it firmly.
- Expand the PID control system to manage all six joints concurrently
- Create a simpler user interface (e.g., via serial commands from your computer) to command the robot to move to a specific coordinates or positions.

  # Potential Methodology
  1. Physical Layout: Design a Layout for all components within your chosen enclosure
  2. Mounting: Securely mount the Raspberry Pi Pico, all 6 H bridge modules, the 2-Relay module, the fuse block, the 12V-to-5V buck converter and any terminal blocks.
  3. Wiring: Using thick 12 or 14 AWG wire, connect your main 12V power supply to the input of our fuse block
  4. Run Individual 12V Power and ground wires from the fused outputs of the fuse blcok to the + 12V and GND inputs of each of the 6 H-bridges and the 2-relay module.
  5. Wire the 5V Low-Power Circuit: Connect the input of your buck converter to one of the fused 12V outputs on our fuse blocks
  6. Adjust the buck converter to ensure its output is a stable 5V
  7. Run the 5V and ground wires from the buck converter's output to a dedicated terminal block. This weill be where we connect the encoder power lines later.
  8. Wiring the 3.3V Signal Logic: Using standard jumper wires, connect GPIO pins from the Raspberry Pi Pico to the control input pins (IN1, In2, ENA, etc.) of all six H-bridges.
  9. Connect trwo additional GPIO pins from he pico to the input pins of the 2-realy module for the conveyor
  10. Keep a detailed log of which GPIO pin is connected to which specific function
  11. Controller Bench Test: With the robot NOT connected. plug in and turn on our 12V power supply.
  12. Use a multimeter to confirm we have a stable 12V at the H-bridges and a stable 5V at the designated encoder power terminals.
  13. Plug the Pico W into your computer and run a simple "blink" script to ensre it is powered and functioning correctly.
  14. Set up for testing: Connect the SCORBOT's large DB50 Cable to your DB50 breakout board. You will perform all testing on the screw terminals of the breakout board,
  15. Identify Motor Wires: Use a multimeter in resistance mode to find pairs of terminals with low resistance.
  16. Once a pair is found, confirm its a motor by briefly applying 9V from a battery and observing which joint moves.
  17. Label the pair and repeat until all 6 motor pairs are found and documented.
  18. Identify Home switch wires: Manually move a robot joint unitil its home switch clicks.
  19. Use our multimeter in continuity mode to find the pair of (as-yet-unidentified) terminals that show a change (from open to closed, or vice versa)
  20. Label the pair and repeat for all 6 axes.
  21. Identify encoder wires: connect the 5V and ground from your controller's buck converter to a suspected VCC/GND pair among the remaining wires.
  22. Connect suspected signal wires (Channels A and B) to input pins on your Pico W.
  23. Run a simple script to monitor the pins and slowly turn the corresponding joint by hand. The correct wires will show the characteristic square-wave pulses of a quadrature encoder.
  24. Label the VCC, GND, A, and B wires and repeat for all 6 encoders.
  25. Create Master Pin OUt chart: Compile all your findings into a final, clean, document that maps every pin on the DB50 breakout board to its specific function. This chart is the master reference for the project.
  26. Set Up a MicroPython Environment: Install the Micropython firmwar on your Raspberry Pi Pico W
  27. Establish a connection using Thonny IDE.
  28. Open Loop Motor Test: Connect our controller to the robot arm/
  29. Write a simple program to control just one motor. The program should have functions to run the motor forward, backward, and at different speeds using PWM, without any geedback from the encoders.
  30. Encoder Reading Test: Write a program that uses a PIO state machine to read the encoder count from that same joint. The program should just print the live encoder position to the screen as you move the joint by hand.
  31. Combine the logic from steps 12 and 13.
  32. Implement a PID control algorithm that takes a "target position" (an encoder count) as an input. The algorhithm will use the live encoder reading to automatically calculate the required. motor speed and direct to reach the target and hold it there.
  33. PID Tuning: Carefully tuned the P, I, and D constants for that one joint until its movement is fast, accurate and stable with minimal overshoot or oscillation.
  34. Expand to all joints: expand your software architecture to handle all six joints. Each jiont will need its own set of tuned PID constants.

# Goals
Build a safe, reliable and fully wired custom controller box that can deliver power to all robotic components. Create a complete and accurate "pinout map" of the SCORBOT's 50-pin connector making the robot wiring fully understood. Then wire Micropython that achieves stable, precise and command-based control over all six joints of the SCORBOT arm.

# Table Of Contents
- [Project Overview]
- [Objective]
- [Goals]
- [Methodology]
- [Results]
- [Key Findings]
- [Visualizations]
- [Future Work]
- [Individual Contributions]

# Visualizations
Supplies:
1. Controller: 1 x Raspberry Pi Pico W Microcontroller
2. Power Supply: 1 x 12V 50A power supply
3. Safety: 6 Way fused distribution block**
4. Safety: 12-14 AWG wire**
5. Blade Fuses.**
6. Robot Arm Drivers: 6 x L28N H-bridge modules
7. Conveyor Driver: 1 x 2-Relay Module
8. Interface: BRKDD50FV2-D50 Connector
9. Power Conversion: 1 x DCDC Buck Converter
10. Terminal Block: Weidu TB2506
11. Soder bread board.
