import time
import os

# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BOARD)

# GPIO.setup(channel/channel_list, GPIO.OUT/IN)

# value = GPIO.input(channel(/channel_list?))
# GPIO.output(channel/channel_list, 0/1)


def set(chan, value):
    if type(chan) == list:
        for c in chan:
            if c not in output_chans:
                raise Exception("This pin is not an output - " + str(c))
    else:
        if chan not in output_chans:
            raise Exception("This pin is not an output - " + str(chan))

    # GPIO.output(chan, value)


def get(chan):
    if type(chan) == list:
        raise Exception("Must only get one pin at a time!")

    if chan not in input_chans:
        raise Exception("This pin is not an input - " + str(chan))

    # return GPIO.input(chan)


# START


def toBinary(x, digits):
    return ("0" * (digits - len(bin(x)[2:]))) + bin(x)[2:]


def toTwos(bin):
    return toBinary(256 - int(bin, 2), len(bin))


def resetPins(chip):
    if chip == "control":
        set([*LS_07,D_0, D_1, D_2, D_3, D_5, D_6, D_7 ,TWOS,CLK,SERIAL1,REG_CLK1,SERIAL_CLK1,SERIAL2,REG_CLK2,SERIAL_CLK2],0)
        set([CLR_INV1,CLR_INV2, D_4], 1)
    elif chip == "output":
        set([*LS_07,*D_07,TWOS,CLK,SERIAL1,REG_CLK1,SERIAL_CLK1,SERIAL2,REG_CLK2,SERIAL_CLK2, CLR_INV1,CLR_INV2],0)
        set([SERIAL2], 1)
    elif chip == "ram":
        pass


def clearScreen():
    # os.system('clear') # linux
    os.system("cls")  # windows
    
def convert_to_mm_ss(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60 + 1
    return f"{minutes:02d}:{remaining_seconds:02d}"


stripCount = 0
lastTime = None
def printLoading(title, current_s, max_s, numberOfStrips=50):
    global stripCount
    global lastTime
    
    if current_s == max_s-1:
        clearScreen()
        print(title)
        print("[" + "|" * numberOfStrips + "]")
        print("ETA: DONE\n")
        return
    
    if current_s == 0:
        clearScreen()
        lastTime = time.time()
        print(title)
        print("[" + "|" * 0 + " " * numberOfStrips + "]")
        print("ETA: -\n")
        return

    strip = int(current_s / float(max_s) * 100) // (100 // numberOfStrips)
    if stripCount != strip:
        stripCount = strip
        
        eta = int((numberOfStrips - strip)*(time.time()-lastTime))
        lastTime = time.time()
        time.sleep(0.001)
        clearScreen()
        print(title)
        print("[" + "|" * strip + " " * (numberOfStrips - strip) + "]")
        print("ETA: ~" + convert_to_mm_ss(eta) + "\n")
        
def binStringToList(s):
    return [int(bit) for bit in s]

def convertControlToBinList(controls):
    binary_string = "0" * 32
    for index in controls:
        binary_string = binary_string[:index] + "1" + binary_string[index + 1:]
    return binStringToList(binary_string)
        
        
microcodesIndex =                                                 \
{                                                                 \
"I_RST"     : 0	,                                                 \
"O_IN"	    : 1 ,                                                 \
"A_IN"	    : 2 ,                                                 \
"A_OUT"     : 3 ,                                                 \
"A_RST"	    : 4 ,                                                 \
"B_IN"	    : 5 ,                                                 \
"B_OUT"	    : 6 ,                                                 \
"B_RST"     : 7 ,                                                 \
"MA_IN"	    : 8 ,                                                 \
"MA_RST"    : 9 ,                                                 \
"M_IN"	    : 10,                                                 \
"M_OUT"     : 11,                                                 \
"F_RST"	    : 12,                                                 \
"E_OUT"	    : 13,                                                 \
"SU"	    : 14,                                                 \
"F_IN"      : 15,                                                 \
"I_IN"	    : 16,                                                 \
"I_OUT"	    : 17,                                                 \
"CLC_RST"   : 18,                                                 \
"HALT"      : 19,                                                 \
"PCE"       : 20,                                                 \
"PC_OUT"    : 21,                                                 \
"JMP"       : 22                                                  \
}


def loadMicrocodeForControlLogic():
    fetchSteps = [[microcodesIndex["PC_OUT"],microcodesIndex["MA_IN"]],[microcodesIndex["M_OUT"],microcodesIndex["I_IN"],microcodesIndex["PCE"]]]
    controlLogicRaw = []
    
    with open("microcodes.txt", "r") as file:
        data = [line.strip() for line in file.readlines()]

    for line in data:
        values = line.strip().split("\t")
        
        #[[Instruction],[Steps], ZF, CF, [OUTPUT]]
        if len(values) == 2:
            Code = values[0]
            ZC = values[1]
            
            for step in range(0,16):
                stepBin = binStringToList(toBinary(step, 4))
                if step == 0:
                    controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList(fetchSteps[0])])
                elif step == 1:
                    controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList(fetchSteps[1])])
                elif step == 2:
                    controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList([microcodesIndex["CLC_RST"]])])
                else:
                    controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), binStringToList("0"*32)])
            continue
            
        InstructionName = values[0]
        Param1 = values[1]
        Param2 = values[2]
        Code = values[3]
        ZC = values[4]
        ControlStepsIndexed = [[microcodesIndex[y.strip()] for y in x.split(',')] for x in values[5:]]
        
        for step in range(0,16):
            stepBin = binStringToList(toBinary(step, 4))
            if step == 0:
                controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList(fetchSteps[0])])
            elif step == 1:
                controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList(fetchSteps[1])])
            elif step <= len(ControlStepsIndexed)+1:
                controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList(ControlStepsIndexed[step-2])])
            else:
                controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), binStringToList("0"*32)])    
                
    return controlLogicRaw
    
def loadMicrocodeForRAM():
    logicDict = {}
    
    with open("microcodes.txt", "r") as file:
        data = [line.strip() for line in file.readlines()]

    for line in data:
        values = line.strip().split("\t")
        
        if len(values) == 2:
            continue
            
        InstructionName = values[0].lower()
                 #Param1             Param2             Code
        Params = [values[1].lower(), values[2].lower(), values[3].lower()]
        if InstructionName not in logicDict and InstructionName[0] != "?":
            logicDict.update({InstructionName : {values[3] : Params}})
        elif InstructionName[0] != "?":
            if values[3] not in logicDict[InstructionName]:
                logicDict[InstructionName].update({values[3] : Params})
                
    return logicDict
        


# 7 segment hex codes
#      a,b,c,d,e,f,g,dp
hexes = [
    [1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [1, 0, 1, 1, 0, 1, 1, 0],
    [1, 0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 1, 1, 0],
    [1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0],
    [1, 0, 0, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 1, 1, 0],
]


def programOutputEEPROM():
    # AT28C64B-15PU
    """
    PI4 need to be plugged into the programmer board

    7S_CLK 0 -> LED1 and LED3
    7S_CLK 1 -> LED2 and LED4

    LS_0-LS_7 -> LED1 and LED2
    LS_8-LS_15 -> LED3 and LED4

    LS_0-LS_15 must be 1 to turn on the segment

    SERIAL2 is #WE
    """
    max_s = 2 * 2 * 256

    # print("CLK\tTWOS\tLS07    \tD07     ")
    for eepromCount in range(0, 2):
        resetPins("output")
        current_s = 0
        name = "first"
        if eepromCount == 1:
            name = "second"

        print("Put in the " + name + " AT28C64B-15PU EEPROM!")
        print("Press ENTER to program")
        input()

        for clk in range(0, 2):
            set(CLK, clk)
            for twos in range(0, 2):
                for x in range(0, 256):
                    set(TWOS, twos)
                    for LSi in range(len(LS_07)):
                        set(LS_07[LSi], 0)
                        set(D_07[LSi], 0)

                    set(SERIAL2, 1)
                    #time.sleep(0.001)
                    set(SERIAL2, 0)
                    printLoading("Clearing the " + name + " AT28C64B-15PU EEPROM...",current_s,max_s,)
                    current_s += 1

        resetPins("output")
        current_s = 0

        for clk in range(0, 2):
            set(CLK, clk)
            for twos in range(0, 2):
                for x in range(0, 256):
                    bin = toBinary(x, 8)

                    set(TWOS, twos)
                    # print(str(clk)+"\t", end="")
                    # print(str(twos)+"\t", end="")
                    # not negative
                    if twos == 0:
                        if clk == 0:
                            segments = hexes[int(bin[0:4], 2)]
                        else:
                            segments = hexes[int(bin[4:8], 2)]
                        for LSi in range(len(LS_07)):
                            set(LS_07[LSi], segments[LSi])
                            # print(segments[LSi], end="")
                        # print("\t", end="")
                        for LSi in range(len(LS_07)):
                            set(D_07[LSi], bin[-(LSi + 1)])
                            # print(bin[-(LSi+1)], end="")

                    # could be negative (twos comp)
                    else:
                        if x < 128:  # positive
                            if clk == 0:
                                segments = hexes[int(bin[0:4], 2)]
                            else:
                                segments = hexes[int(bin[4:8], 2)]
                            for LSi in range(len(LS_07)):
                                set(LS_07[LSi], segments[LSi])
                                # print(segments[LSi], end="")
                            # print("\t", end="")
                            for LSi in range(len(LS_07)):
                                set(D_07[LSi], bin[-(LSi + 1)])
                                # print(bin[-(LSi+1)], end="")

                        else:  # negative
                            neg_bin = toTwos(bin)
                            if clk == 0:
                                segments = hexes[int(neg_bin[0:4], 2)]
                            else:
                                segments = hexes[int(neg_bin[4:8], 2)]
                            for LSi in range(len(LS_07)):
                                set(LS_07[LSi], segments[LSi])
                                # print(segments[LSi], end="")
                            # print("\t", end="")
                            for LSi in range(len(LS_07)):
                                set(D_07[LSi], bin[-(LSi + 1)])
                                # print(neg_bin[-(LSi+1)], end="")

                    set(SERIAL2, 1)
                    #time.sleep(0.001)
                    set(SERIAL2, 0)
                    printLoading("Programming the " + name + " AT28C64B-15PU EEPROM...",current_s,max_s,)
                    current_s += 1
           
    clearScreen()
    print("Programming done!")
    print("Press ENTER to go back")
    input()
    clearScreen()


def doSerializer(data, cr1, cr2, name):
    clearScreen()
    max_s = len(data)
    current_s = 0
    resetPins("control")
    for i in range(0,2**14):
        set(LS_07, 0)
        set(D_07, 0)
        set(CLK, 0)
        set(TWOS, 0)
        
        set(CLR_INV2, 0)
        #time.sleep(0.0001)
        set(CLR_INV2, 1)
        
        for o_inst in range(0,8):
            set(SERIAL2, 0)
            set(SERIAL_CLK2, 1)
            #time.sleep(0.0001)
            set(SERIAL_CLK2, 0)
            
        set(REG_CLK2, 1)
        #time.sleep(0.0001)
        set(REG_CLK2, 0)
        
        set(D_4, 0)
        #time.sleep(0.0001)
        set(D_4, 1)
        
        printLoading("Clearing the " + name + " AT28HC256F-90SU-T EEPROM...",current_s,max_s,50)
        #time.sleep(0.001)
        current_s += 1

    current_s = 0
    resetPins("control")
    for i in range(len(data)):
        #[[Instruction],[Steps], ZF, CF, [OUTPUT]]
        
        #Instruction (LS_0-LS_7)
        for inst_i in range(len(data[i][0])):
            set(LS_07[inst_i], data[i][0][inst_i])
        
        #Steps
        for step_i in range(len(data[i][1])):
            set(D_07[step_i], data[i][1][step_i])
            
        #ZF, CF
        set(CLK, data[i][2])
        set(TWOS, data[i][3])
        
        set(CLR_INV2, 0)
        #time.sleep(0.0001)
        set(CLR_INV2, 1)
        
        #Output
        for o_inst in range(len(data[i][4][cr1:cr2])):
            set(SERIAL2, data[i][4][o_inst])
            set(SERIAL_CLK2, 1)
            #time.sleep(0.0001)
            set(SERIAL_CLK2, 0)

        set(REG_CLK2, 1)
        #time.sleep(0.0001)
        set(REG_CLK2, 0)
        
        set(D_4, 0)
        #time.sleep(0.0001)
        set(D_4, 1)
        
        #print(current_s, max_s)
        printLoading("Programming the " + name + " AT28HC256F-90SU-T EEPROM...",current_s,max_s,50)
        #time.sleep(0.001)
        current_s += 1

def programControlEEPROM():
    # AT28HC256F-90SU-T
    """
    !PI4 is not plugged into the programmer board!
    !Need to bridge the serializer's 8 signal to the programmer board from the PI4!

    D_0 - D_31 pcb output pins can be set through the serializer, 
    this can be used for the 4 chips like:
    -Chip1:            TO      -> CLO_0-CLO_7 (on control logic board)
                        FROM    -> D_0-D_7 (on programming board) (from serializer)

    -Chip2:            TO      -> CLO_8-CLO_15 (on control logic board)
                        FROM    -> D_8-D_15 (on programming board) (from serializer)

    -Chip3:            TO      -> CLO_16-CLO_23 (on control logic board)
                        FROM    -> D_16-D_23 (on programming board) (from serializer)

    -Chip4:            TO      -> CLO_24-CLO_31 (on control logic board)
                        FROM    -> D_24-D_31 (on programming board) (from serializer)

    -Instruction pins: TO     -> I_8-I_15 (on control logic board)
                        FROM   -> LS_0-LS8 (on PI4 header)

    -CF, ZF:           TO     -> CF, ZF pins (on control logic board)
                        FROM   -> TWOS, 7S_CLK (on PI4 header)

    -STEPS:            TO     -> STEP_0-STEP_3 (on control logic board, need to solder pins or wires to the SN74HC161N chip)
                        FROM   -> D_0-D_3 (on PI4 header)
                        
    -GND, A12, #CE to PI4 GND
    -VCC, #OE to PI4 Power
    -#WE to D_4 (on PI4 header)
    
    -!!!!SERIALIZERs #OE must be connected to GND somehow!!!!
    
    a[0:8], a[8:16], a[16:24], a[24:32]
    """
    data = loadMicrocodeForControlLogic()
    print("Make sure that:\n-GND, A12, #CE is connected to the PI4's GND\n-VCC, #OE is connected to the PI4's VCC")
    print("Press ENTER to continue")
    input()
    clearScreen()
    
    print("Connect the first AT28HC256F-90SU-T EEPROM!")
    print("Press ENTER to program")
    input()
    doSerializer(data, 0, 8, "first")
    
    print("Connect the second AT28HC256F-90SU-T EEPROM!")
    print("Press ENTER to program")
    input()
    doSerializer(data, 8, 16, "second")
    
    print("Connect the third AT28HC256F-90SU-T EEPROM!")
    print("Press ENTER to program")
    input()
    doSerializer(data, 16, 24, "third")
    
    print("Connect the fourth AT28HC256F-90SU-T EEPROM!")
    print("Press ENTER to program")
    input()
    doSerializer(data, 24, 32, "fourth")
    clearScreen()
    
    print("Programming done!")
    print("Press ENTER to go back")
    input()
    clearScreen()

def programRAM():
    """
    CY7C195-25PC
    
    INFO 
    
    """
    clearScreen()
    
    programs = os.listdir("programs")
    
    quitRam = False
    while not quitRam:
        for pi in range(len(programs)):
            print("(" + str(pi+1) + ")\t" + programs[pi])
        print("(" + str(len(programs)+1) + ")\tQuit")
        print("\nInput: ", end="")
        inp = input()
        
        clearScreen()
        inpInt = 0
        try:
            inpInt = int(inp)
        except:
            continue
            
        if inpInt == len(programs)+1:
            quitRam = True
        elif inpInt >= 1 and inpInt <= len(programs):
            endOfCode = None
            print("What should happen when the program reaches the end of the code?")
            while True:
                print("(1)\tHalt the computer")
                print("(2)\tRestart the program")
                print("(3)\tContinue with NOP instructions")
                print("\nInput: ", end="")
                inp = input()
                clearScreen()
                if inp == "1":
                    endOfCode = "halt"
                    break
                elif inp == "2":
                    endOfCode = "restart"
                    break
                elif inp == "3":
                    endOfCode = "continue"
                    break
        
            print("Programming " + programs[inpInt-1][:programs[inpInt-1].find(".")] + " code to the CY7C195-25PC RAMs...")
            print("Press ENTER to compile and program")
            input()
            clearScreen()
            compileAndProgramRam(programs[inpInt-1], endOfCode)
            clearScreen()
            quitRam = True

def programRamData(ramData, dataPart):
    resetPins("ram")
    current_s = 0
    max_s = 65536
    
    if dataPart == 0:
        name = "first"
    if dataPart == 1:
        name = "second"
    if dataPart == 2:
        name = "third"
    if dataPart == 3:
        name = "fourth"
    
    for i in range(65536):
        set(CLR_INV1, 0)
        set(CLR_INV1, 1)
        
        address = binStringToList(toBinary(i, 16))
        for addrBit in address:
            set(SERIAL1, addrBit)
            set(SERIAL_CLK1, 1)
            set(SERIAL_CLK1, 0)
            
        set(REG_CLK1, 1)
        set(REG_CLK1, 0)
        
        set(LS_07[0:4], 0)
        printLoading("Clearing the " + name + " CY7C195-25PC RAM...",current_s,max_s,50)
        current_s += 1

    resetPins("ram")
    current_s = 0
    max_s = len(ramData)
    
    for data in ramData:
        set(CLR_INV1, 0)
        set(CLR_INV1, 1)
        
        for addrBit in data[0]:
            set(SERIAL1, addrBit)
            set(SERIAL_CLK1, 1)
            set(SERIAL_CLK1, 0)
                
        set(REG_CLK1, 1)
        set(REG_CLK1, 0)
        
        toWriteData = []
        
        if dataPart == 0:
            toWriteData = data[1][0:4]        
        if dataPart == 1:
            toWriteData = data[1][4:8]        
        if dataPart == 2:
            toWriteData = data[2][0:4]        
        if dataPart == 3:
            toWriteData = data[2][4:8]
            
        for i in range(len(toWriteData)):
            set(LS_07[i], toWriteData[i])
            
        set(CLK, 0)
        set(CLK, 1)
        
        printLoading("Programming the " + name + " CY7C195-25PC RAM...",current_s,max_s,50)
        current_s += 1

def compileAndProgramRam(filename, endOfCode):
    with open("programs/"+filename, "r") as file:
        lines = [line.strip().lower() for line in file.readlines()]
    
    logicDict = loadMicrocodeForRAM()
    
    """
    for key in logicDict:
        print(key, logicDict[key])
    input()
    """
    
    if len(lines) >= 65535:
        print("Error - The program's code cannot be longer than 65534 lines!")
        print("\t->Number of lines: " + str(len(lines)))
        input()
        return
    
    current_s = 0
    max_s = len(lines)
    ramData = []
    for i in range(len(lines)):
        command = lines[i].split(" ")
        command = [line.strip(',') for line in lines[i].split(" ")]
        instructions = logicDict[command[0]]
        
        param_count = len(command)-1
        possible_params = []
        possible_instructions = []
        for instKey in instructions:
            count = 0
            for c in instructions[instKey][0:2]:
                if c != "":
                    count += 1
            if count not in possible_params:
                possible_params.append(count)
                
            if count == param_count:
                possible_instructions.append(instructions[instKey])
        
        if param_count not in possible_params:
            print("Error at line " + str(i+1) + " - Parameter count mismatch!")
            print("\t->(" + lines[i] + ")")
            input()
            return
        
        #("[" in a[ci] and "]" in a[ci])
        matchedInstruction = None
        justParams = command[1:]
        justParamsConv = command[1:]
        paramDigit = None
        for pi in range(len(justParamsConv)):
            if justParamsConv[pi][0] == "[" and justParamsConv[pi][-1] == "]":
                if justParamsConv[pi][1:-1].isdigit():
                    paramDigit = int(justParamsConv[pi][1:-1])
                    justParamsConv[pi] = "[mem]"
            elif justParamsConv[pi].isdigit():
                paramDigit = int(justParamsConv[pi])
                justParamsConv[pi] = "num"
        
        for a in possible_instructions:
            if len(justParamsConv) == 0:
                matchedInstruction = a
            for ci in range(len(justParamsConv)):
                if justParamsConv[ci] != a[ci]:
                    break
                    
                if ci == len(justParamsConv)-1:
                    matchedInstruction = a
        
        if matchedInstruction is None:
            print("Error at line " + str(i+1) + " - Cannot find instruction!")
            print("\t->(" + lines[i] + ")")
            input()
            return
            
        if paramDigit is not None and paramDigit >= 256:
            print("Error at line " + str(i+1) + " - Value or address cannot be larger than 255!")
            print("\t->(" + lines[i] + ")")
            input()
            return
            
        ramAddr = binStringToList(toBinary(i,16))
        ramInst = binStringToList(matchedInstruction[2])
        ramDataV = binStringToList("0"*8)
        if paramDigit != None:
            ramDataV = binStringToList(toBinary(paramDigit,8))
        ramData.append([ramAddr, ramInst, ramDataV])
        
        printLoading("Compiling " + filename + "...",current_s,max_s,50)
        current_s += 1
    
    if endOfCode == "halt":
        ramData.append([binStringToList(toBinary(len(lines),16)), [1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0]])
    elif endOfCode == "restart":
        ramData.append([binStringToList(toBinary(len(lines),16)), [0,0,0,1,0,1,1,1], [0,0,0,0,0,0,0,0]])
    
    
    
    print("Connect the first CY7C195-25PC RAM")
    print("LS0-3 TO MIO_12-15")
    print("Press ENTER to program")
    input()
    programRamData(ramData, 0)
    
    print("Connect the second CY7C195-25PC RAM")
    print("LS0-3 TO MIO_8-11")
    print("Press ENTER to program")
    input()
    programRamData(ramData, 1)
    
    print("Connect the third CY7C195-25PC RAM")
    print("LS0-3 TO MIO_4-7")
    print("Press ENTER to program")
    input()
    programRamData(ramData, 2)
    
    print("Connect the fourth CY7C195-25PC RAM")
    print("LS0-3 TO MIO_0-3")
    print("Press ENTER to program")
    input()
    programRamData(ramData, 3)

    clearScreen()
    print("Programming done!")
    print("Press ENTER to go back")
    input()
    clearScreen()

# Output EEPROM programming pins
LS_0 = 3
LS_1 = 5
LS_2 = 7
LS_3 = 11
LS_4 = 13
LS_5 = 15
LS_6 = 19
LS_7 = 21
LS_07 = [LS_0, LS_1, LS_2, LS_3, LS_4, LS_5, LS_6, LS_7]
D_0 = 31
D_1 = 33
D_2 = 35
D_3 = 37
D_4 = 40
D_5 = 38
D_6 = 36
D_7 = 32
D_07 = [D_0, D_1, D_2, D_3, D_4, D_5, D_6, D_7]
TWOS = 23
CLK = 29

# RAM programming pins
SERIAL1 = 8
REG_CLK1 = 10
SERIAL_CLK1 = 12
CLR_INV1 = 16

SERIAL2 = 26
REG_CLK2 = 24
SERIAL_CLK2 = 22
CLR_INV2 = 18

input_chans = []
output_chans = [*LS_07,*D_07,TWOS,CLK,SERIAL1,REG_CLK1,SERIAL_CLK1,CLR_INV1,SERIAL2,REG_CLK2,SERIAL_CLK2,CLR_INV2]

# MAIN START

clearScreen()

quit = False
while not quit:
    print("(1)\tProgram the output AT28C64B-15PU EEPROMs")
    print("(2)\tProgram the control logic AT28HC256F-90SU-T EEPROMs")
    print("(3)\tProgram the CY7C195-25PC RAMs")
    print("(4)\tQuit")
    print("\nInput: ", end="")
    inp = input()
    clearScreen()
    if inp == "1":
        programOutputEEPROM()
    elif inp == "2":
        programControlEEPROM()
    elif inp == "3":
        programRAM()
    elif inp == "4":
        quit = True
