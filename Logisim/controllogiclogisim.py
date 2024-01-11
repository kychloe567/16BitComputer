

microcodesIndex =                                                     \
{                                                                     \
"PC_OUT"        : 0	,                                                 \
"PCE"           : 1 ,                                                 \
"J"             : 2 ,                                                 \
"A_IN"          : 3 ,                                                 \
"A_OUT"         : 4 ,                                                 \
"A_RST"         : 5 ,                                                 \
"B_IN"          : 6 ,                                                 \
"B_OUT"         : 7 ,                                                 \
"B_RST"         : 8 ,                                                 \
"SU"            : 9 ,                                                 \
"F_RST"         : 10,                                                 \
"F_IN"          : 11,                                                 \
"E_OUT"         : 12,                                                 \
"O_IN"          : 13,                                                 \
"O_RST"         : 14,                                                 \
"TWOS"          : 15,                                                 \
"MA_IN"         : 16,                                                 \
"MA_RST"        : 17,                                                 \
"M_IN"          : 18,                                                 \
"M_OUT"         : 19,                                                 \
"I_IN"          : 20,                                                 \
"I_OUT"         : 21,                                                 \
"I_RST"         : 22,                                                 \
"CLC_RST"       : 23,                                                 \
"HALT"          : 24                                                  \
}

inverted_microcodesIndex = {v: k for k, v in microcodesIndex.items()}

def binStringToList(s):
    return [int(bit) for bit in s]

def toBinary(x, digits):
    return ("0" * (digits - len(bin(x)[2:]))) + bin(x)[2:]

def convertControlToBinList(controls):
    binary_string = "0" * 32
    for index in controls:
        binary_string = binary_string[:index] + "1" + binary_string[index + 1:]
    return binStringToList(binary_string)

def convertToControls(binary):
    controls = ""
    for i in range(len(binary)):
        if binary[i] == 1:
            controls += inverted_microcodesIndex[i] + " "
    return controls

def loadMicrocodeForControlLogic():
    fetchSteps = [[microcodesIndex["PC_OUT"],microcodesIndex["MA_IN"]],[microcodesIndex["M_OUT"],microcodesIndex["I_IN"],microcodesIndex["PCE"]]]
    controlLogicRaw = []
    
    with open("microcodes.txt", "r") as file:
        data = [line.strip() for line in file.readlines()]

    for line in data:
        values = line.strip().split("\t")
        
        #[[Instruction],[Steps], ZF, CF, [OUTPUT]]
        InstructionName = values[0]

        if len(values) == 2:
            Code = values[0]
            ZC = values[1]
            
            for step in range(0,16):
                stepBin = binStringToList(toBinary(step, 4))
                if step == 0:
                    controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList(fetchSteps[0]), InstructionName, convertToControls(convertControlToBinList(fetchSteps[0]))])
                elif step == 1:
                    controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList(fetchSteps[1]), InstructionName, convertToControls(convertControlToBinList(fetchSteps[1]))])
                elif step == 2:
                    controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList([microcodesIndex["CLC_RST"]]), InstructionName, convertToControls(convertControlToBinList([microcodesIndex["CLC_RST"]]))])
                else:
                    controlLogicRaw.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), binStringToList("0"*32), InstructionName, convertToControls(binStringToList("0"*32))])
            continue
            
        Param1 = values[1]
        Param2 = values[2]
        Code = values[3]
        ZC = values[4]
        ControlStepsIndexed = [[microcodesIndex[y.strip()] for y in x.split(',')] for x in values[5:]]

        asd = []
        for step in range(0,16):
            stepBin = binStringToList(toBinary(step, 4))
            if step == 0:
                asd.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList(fetchSteps[0]), InstructionName, convertToControls(convertControlToBinList(fetchSteps[0]))])
            elif step == 1:
                asd.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList(fetchSteps[1]), InstructionName, convertToControls(convertControlToBinList(fetchSteps[1]))])
            elif step <= len(ControlStepsIndexed)+1:
                asd.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), convertControlToBinList(ControlStepsIndexed[step-2]), InstructionName, convertToControls(convertControlToBinList(ControlStepsIndexed[step-2]))])
            else:
                asd.append([binStringToList(Code), stepBin, int(ZC[0]), int(ZC[1]), binStringToList("0"*32), InstructionName, convertToControls(binStringToList("0"*32))])    
        controlLogicRaw = controlLogicRaw + asd
                
    return controlLogicRaw

def sort_elements(elements):
    def element_to_binary(element):
        binary_sequence = element[0] + element[1] + [element[2], element[3]] 

        return int(''.join(map(str, binary_sequence)), 2)

    return sorted(elements, key=element_to_binary)


a = loadMicrocodeForControlLogic()
a = sort_elements(a)
lines = ""
lines2 = ""
isOpened = False
x = 0
for b in a:
    for c in range(len(b[4])):
        b[4][c] = str(b[4][c])
    b[4] = "".join(b[4])

    """
    if x > 32 and x < 40:
        y = 5
    print(str(x) + ": " , b)
    """
    #print(str(x) + ": " , b)
    hexadecimal_value = format(int(b[4], 2), '08X')

    lines2 += hexadecimal_value + " " + "".join([str(i) for i in b[0]]) + "".join([str(i) for i in b[1]]) + str(b[2]) + str(b[3]) + "\t" + b[4] + str(b) + "\n"
    #189:  [[0, 0, 0, 0, 0, 0, 1, 0], [1, 1, 0, 1], 1, 1, '00000000000000000000000000000000', 'MOV', '']
    #if b[0] == [0, 0, 0, 0, 0, 0, 1, 0]:
    #    y = 5
    x += 1

    
    lines += hexadecimal_value + " "
    #if isOpened:
    #    if len(hexadecimal_value) == 4:
    #        lines += hexadecimal_value + " "
    #        isOpened = False
    #    else:
    #        lines += hexadecimal_value[0:4] + " " + hexadecimal_value[4:8]
    #else:
    #    if len(hexadecimal_value) == 4:
    #        lines += hexadecimal_value
    #        isOpened = True
    #    else:
    #        lines += hexadecimal_value + " "

if True:
    with open("controllogicdata.txt","w") as f:
        f.write(lines)
    with open("test1.txt","w") as f:
        f.write(lines2)