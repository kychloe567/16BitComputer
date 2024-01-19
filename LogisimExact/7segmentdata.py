import itertools
import math

#ADDR - 13 bit -> 0-7 DATA, 8-10 GND, 11 - TWOS, 12 - 7S_CLK

digits = {"0":"abcdef","1":"bc","2":"abdeg","3":"abcdg","4":"bcfg","5":"acdfg","6":"acdefg","7":"abc","8":"abcdefg","9":"abcdfg",\
          "a":"abcefg","b":"cdefg","c":"adef","d":"bcdeg","e":"adefg","f":"aefg"," ":""}

#positions = ["p","c","d","e","b","a","f","g"]
positions = ["a","b","c","d","e","f","g","p"]

def sort_and_fill(s, order):
    sorted_string = ''.join(sorted(s, key=order.index if s else order))
    filled_string = ''
    for pos in order:
        filled_string += sorted_string[sorted_string.index(pos)] if pos in sorted_string else 'x'
    return filled_string

def getBinaryFor7Seg(d):
    digit = digits[d]
    bitValue = ""
    for d in digit:
        if d == "x":
            bitValue = "0" + bitValue
        else:
            bitValue = "1" + bitValue
    return bitValue

digits = {key: sort_and_fill(value, positions) for key, value in digits.items()}

toFileLeft = ""
toFileRight = ""
lastPerc = -1

with open("7SEG_LEFT.txt","w") as f:
    f.write("")
with open("7SEG_RIGHT.txt","w") as f:
    f.write("")


dec = 0
for CLK in range(2):
    CLK_string = str(CLK)
    for TWOS in range(2):
        TWOS_string = str(TWOS)
        for GND in itertools.product([0,1], repeat=3):
            GND_string = "000"

            for data in itertools.product([0,1], repeat=8):
                binary_string = ''.join(map(str, data))
                integer = int(binary_string, 2)
                max_ = int("1"*8,2)
                perc = math.floor((integer/max_)*100)
                if perc != lastPerc:
                    lastPerc = perc

                leftString = hex(int(binary_string + "00000000",2))[2:].zfill(4)
                rightString = hex(int(binary_string,2))[2:].zfill(4)
                if CLK == 0:
                    left = leftString[1]
                    right = rightString[3]
                if CLK == 1:
                    left = leftString[0]
                    right = rightString[2]

                hexLeft = format(int(getBinaryFor7Seg(left), 2), '02X')
                hexRight = format(int(getBinaryFor7Seg(right), 2), '02X')

                #print(str(dec) + ": \t" + hexRight + "\t" + rightString + "\t" + CLK_string)

                toFileLeft += hexLeft + " "
                toFileRight += hexRight + " "
                dec += 1




with open("7SEG_LEFT.txt","w") as f:
    f.write(toFileLeft)
with open("7SEG_RIGHT.txt","w") as f:
    f.write(toFileRight)


print("Done!")

