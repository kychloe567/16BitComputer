import time
import os

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

def binStringToList(s):
    return [int(bit) for bit in s]

def toBinary(x, digits):
    return ("0" * (digits - len(bin(x)[2:]))) + bin(x)[2:]


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

def compileProgram(filename, endOfCode):
    with open(filename, "r") as file:
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

    return ramData


a = compileProgram("programAdder.txt", endOfCode="halt")
lines = ""
for b in a:
    c = b[1] + b[2]
    c = "".join([str(i) for i in c])
    print(c)
    hexadecimal_value = format(int(c, 2), '04X')
    lines += hexadecimal_value + " "


lines += "FFFF "

with open("ramdata.txt","w") as f:
    f.write(lines)

print("Done")