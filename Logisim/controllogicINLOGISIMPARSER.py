data = []

x = 0
with open("controllogicINLOGISIM.txt","r") as f:
    d = f.readlines()
    for line in d:
        stripped = line.strip().strip("\n").split()
        for strip in stripped:
            binary_value = format(int(strip, 16), '0' + str(len(strip) * 4) + 'b')
            binAddr = format(x, '014b')
            hexaAddr = format(x, '04x')
            x += 1
            data.append(binAddr + "\t" + hexaAddr + "\t" + binary_value)

x = 0
for d in data:
    print(d)
    if x > 10:
        break
    x += 1