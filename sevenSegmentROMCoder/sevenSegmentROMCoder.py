i = 0
m = 65536

def numToSeg(n):
    if(n == 0):
        return "c0"
    if(n == 1):
        return "f9"
    if(n == 2):
        return "a4"
    if(n == 3):
        return "b0"
    if(n == 4):
        return "99"
    if(n == 5):
        return "92"
    if(n == 6):
        return "82"
    if(n == 7):
        return "f8"
    if(n == 8):
        return "80"
    if(n == 9):
        return "90"

def numToBCD(n):
    if(n == 0):
        return "00"
    if(n == 1):
        return "01"
    if(n == 2):
        return "02"
    if(n == 3):
        return "03"
    if(n == 4):
        return "04"
    if(n == 5):
        return "05"
    if(n == 6):
        return "06"
    if(n == 7):
        return "07"
    if(n == 8):
        return "08"
    if(n == 9):
        return "09"

for d in range(1,6):
    f = open("sevenSegmentD_"+str(d)+".txt", "w", encoding="utf-8")
    for i in range(100):
        num = str(i)
        if(len(num)-d >= 0):
            dec = num[len(num)-d]
            #h = str(numToSeg(int(dec)))
            h = str(numToBCD(int(dec)))
            f.write(h + " ")
        else:
            f.write("00 ")
    f.close()
    print("done: " + str(d))
