# 16 Bit SAP-1 Computer/CPU
Welcome to the 16-Bit Minimalistic CPU project! This repository houses a unique project aimed at designing and building a simple, yet functional 16-bit computer from the ground up. The project focuses on implementing the core components of a CPU using basic logic gates (AND, OR) and memory ICs, organized into small modular boards. Each board represents a distinct part of the CPU's architecture, all interconnected via middle bus boards that manage communication and data flow.

This project is perfect for enthusiasts and learners who are interested in understanding the fundamental principles of CPU architecture and digital electronics. By breaking down the CPU into its simplest components, this project provides a clear and educational view of how a computer operates at a low level. Whether you're a student, a hobbyist, or an engineer looking to refresh your knowledge, this project offers hands-on experience in building a working 16-bit CPU from scratch.

Feel free to explore the documentation, check out the schematics, and get started with your own build!

<p align="center" >
  <a href="#features">Features</a> •
  <a href="#Files">Files</a> •
  <a href="#packages">Packages</a>   
</p>

## Features

Each board has debug pins and LEDs, and access points to the various signals

+ Clock & Power board
    + Switch between oscillator and 555 timer mode
    + Switch between clock and step mode
    + Possible stability with 1MHZ clock
    + Adjustable 555 timer speed
    + Single step button
    + Unhalt and reset button
    + <span style="color:green">Controls:
        + <span style="color:green">HALT - Stops the clock, needs manual pressing of the UNHALT button
+ Program Counter board
    + If enabled counts up in binary, in sync with the CLK signal
    + 16 bit program counter
    + <span style="color:green">Controls:
        + <span style="color:green">JMP - Loads in the bus content
        + <span style="color:green">PC_OUT - Output the counter to the bus
        + <span style="color:green">PCE - Enable the program counter
+ RAM Address Register board
    + 16 bit Register for accessing the correct location in the memory
    + Switch for changing between bus and dipswitch mode
    + Direct connection to the RAM board
    + <span style="color:green">Controls:
        + <span style="color:green">MA_IN - Loads in the bus content
        + <span style="color:green">MA_RST - Clears the register
+ RAM Module board
    + 4 seperate asynchronous 256 Kbit RAM ICs (each with 4bit address space)
    + 64k * 16 bit addressable memory
    + Debug pins for programming RAM with a developper board
    + Button/pin for enabling data transfer
    + <span style="color:green">Controls:
        + <span style="color:green">M_OUT - Outputs of the contents of the memory at the given address
        + <span style="color:green">M_IN - Loads in the bus content to the given memory address
+ Instructtion Register board
    + 16 bit register
    + Holds the current instruction
    + Direct connection to the Control Logic board
    + <span style="color:green">Controls:
        + <span style="color:green">I_OUT - Outputs the contents to the bus
        + <span style="color:green">I_IN - Loads in the bus content
        + <span style="color:green">I_RST - Clears the register
+ Control Logic board
    + Memory for the different instructions
    + Uses the instruction register as address, then outputs the control signals
    + 4 bit substep binary counter
    + Always outputs its content to the control signal pins
    + Debug pins for programming the control logic with a developper board
    + <span style="color:green">Controls:
        + <span style="color:green">CLC_RST - Resets the substep counter
        + <span style="color:green">CF - Carry Flag
        + <span style="color:green">ZF - Zero Flag
+ Universal two seperate 16 bit register board
    + 2 * 16 bit registers for integers mainly
    + Possible direct connection to the ALU board
    + <span style="color:green">Controls:
        + <span style="color:green"> A_IN - Loads in the bus content to the A register
        + <span style="color:green"> A_OUT - Outputs the A register's content to the bus
        + <span style="color:green"> A_RST - Clears the A register
        + <span style="color:green"> B_IN - Loads in the bus content to the B register
        + <span style="color:green"> B_OUT - Outputs the B register's content to the bus
        + <span style="color:green"> B_RST - Clears the B register
+ ALU board
    + Only addition and substraction
    + Carry flag and zero flag registers
    + <span style="color:green">Controls:
        + <span style="color:green">F_RST - Resets the flag register
        + <span style="color:green">EO - Outputs the result to the bus
        + <span style="color:green">SU - While active, substraction is on
        + <span style="color:green">FI - Fills flag registers (Checks if active or not)
    + <span style="color:green">Output signals:
        + <span style="color:green">CF - Carry Flag
        + <span style="color:green">ZF - Zero Flag
+ Output register board
    + 16 bit register for holding data
    + 7 segment decoder circuit
    + 4 digit hexa display, with an additional negative sign
    + <span style="color:green">Controls:
        + <span style="color:green">O_IN - Loads in the bus content

## Files

+ BOMs/digikey - List of components and ordering information from digikey
+ EasyEDA_projects - Project files for EasyEDA, each board a seperate small project
+ Gerbers - Gerber files for the printed circuit manufacturing
+ Logisim - A Logisim simulation of the underlying logic, with updated components
+ LogisimExact - A Logisim simulation of the exact underlying logic
+ Output_images - Rendered high quality images of the assembled CPU
+ modularprogrammer - This is a python script for programming the following boards:
    + Control Logic (decoding of the instruction codes)
    + Output board hexa decoder (binary to 7segment in hexa format)
    + RAM (uploading program, data, etc)
+ Programmer - A simple compiler for the custom assembly language, with microcodes explanation
+ sevenSegmentROMCoder - An another Output board hexa decoder (binary to 7segment in hexa format)


## Packages

This software uses the following programs and open source packages:

- [EasyEDA](https://easyeda.com/)
- [Python](https://www.python.org/)
