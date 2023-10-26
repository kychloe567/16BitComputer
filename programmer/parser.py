import os

def toBinary(x, digits):
    return ("0" * (digits - len(bin(x)[2:]))) + bin(x)[2:]
    
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

def binStringToList(s):
    return [int(bit) for bit in s]

def convertControlToBinList(controls):
    binary_string = "0" * 32
    for index in controls:
        binary_string = binary_string[:index] + "1" + binary_string[index + 1:]
    return binStringToList(binary_string)

def parse_data(data):
    fetchSteps = [[microcodesIndex["PC_OUT"],microcodesIndex["MA_IN"]],[microcodesIndex["M_OUT"],microcodesIndex["I_IN"],microcodesIndex["PCE"]]]
    controlLogicRaw = []

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
        
"""
        Steps = []
        for rest in line_values[5:]:
            Steps.append([int(x) for x in rest.strip().split(",")])
        StepsIndexed = []
        for step in Steps:
            StepsIndexed.append([index_dict[str(x)] for x in step])
            
        binary_strings = []
        for step in StepsIndexed:
            binary_string = "0" * 32
            for index in step:
                binary_string = binary_string[:index] + "1" + binary_string[index + 1:]
            binary_strings.append([int(x) for x in binary_string])
            
        instruction_binary = [int(x) for x in format(int(Instruction, 2), "08b")]
        for i in range(2 ** len(Steps)):
            for j in range(2):
                for k in range(2):
                    output.append([instruction_binary, [int(x) for x in format(i, f"0{len(Steps)}b")], int(ZC[0]), int(ZC[1]), binary_strings[j * 2 + k]])
                        
    return output
    """

with open("microcodes.txt", "r") as file:
    lines = [line.strip() for line in file.readlines()]
    
a = parse_data(lines)
print("done")