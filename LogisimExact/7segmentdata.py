import itertools

#ADDR - 13 bit -> 0-7 DATA, 8-10 GND, 11 - TWOS, 12 - 7S_CLK

digits = {"0":"abcdef","1":"bc","2":"abdeg","3":"abcdg","4":"bcfg","5":"acdfg","6":"acdefg","7":"abc","8":"abcdefg","9":"abcdfg",\
          "a":"abcefg","b":"cdefg","c":"adef","d":"bcdeg","e":"adefg","f":"aefg"," ":""}

positions = ["b","a","f","g","p","c","d","e"]

def sort_and_fill(s, order):
    sorted_string = ''.join(sorted(s, key=order.index if s else order))
    filled_string = ''
    for pos in order:
        filled_string += sorted_string[sorted_string.index(pos)] if pos in sorted_string else 'x'
    return filled_string

digits = {key: sort_and_fill(value, positions) for key, value in digits.items()}

#10110011
toFile = ""

for data in itertools.product([0,1], repeat=16):
    binary_string = ''.join(map(str, data))
    integer = int(binary_string, 2)
    string = hex(integer)[2:]
    for GND in itertools.product([0,1], repeat=3):
        for CLK in range(2):
            for TWOS in range(2):
                if CLK == 0:
                    
                    continue
                elif CLK == 1:
                    continue

"""
for i in itertools.product([0,1], repeat=16):
    binary_string = ''.join(map(str, i))
    integer = int(binary_string, 2)
    string = hex(integer)[2:]
    while len(string) < 4:
        string = " " + string
    
    toDigits = []

    value = ""
    for c in string:
        if c == " ":
            value = "00000000" + value
            continue
        digit = digits[c]
        bitValue = ""
        for d in digit:
            if d == "x":
                bitValue = "0" + bitValue
            else:
                bitValue = "1" + bitValue
        value = bitValue + value

    hexadecimal_value = format(int(value, 2), '08X')
    toFile += hexadecimal_value + " "
"""
"""
for i in itertools.product([0,1], repeat=16):
    binary_string = ''.join(map(str, i))
    integer = int(binary_string, 2) * -1
    print(integer)
    string = hex(integer)
    print(string)
    while len(string) < 4:
        string = " " + string
    
    toDigits = []
    
    value = ""
    for c in string:
        if c == " ":
            value = value + "00000000"
            continue
        digit = digits[c]
        for d in digit:
            if d == "x":
                value = value + "0"
            else:
                value = value + "1"

    hexadecimal_value = format(int(value, 2), '08X')
    toFile += hexadecimal_value + " "
    
    
    #['', 'abdeg', 'abcdeg', 'acdefg']
    #bafg
    #pcde
    
"""
"""
with open("hexadata.txt","w") as f:
    f.write(toFile)

print("Done!")
"""
