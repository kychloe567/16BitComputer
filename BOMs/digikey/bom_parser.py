f = open("boms.txt","r")

d = {}
for l in f.readlines():
  a,b = l.split('\t')
  a = a.strip('"')
  b = int(b.strip().strip('"'))

  if a not in d:
    d.update({a : b})
  else:
    d.update({a : b + d[a]})

f.close()

f = open("boms_parsed.txt","w")
f.write("Name\tQuantity\n")
for a, b in d.items():
  f.write("\"" + a + "\"\t\"" + str(b) + "\"\n")

f.close()
