
import itertools

d = []
with open("binariesToCheck.txt","r") as f:
    d = f.readlines()

x = 0
error = []
for i in itertools.product([0,1], repeat=14):
    conv = "".join([str(y) for y in i])
    toComp = d[x].strip("\n")
    if conv != toComp:
        error.append([toComp,x])
    x += 1

print("DONE")
for e in error:
    print(e)