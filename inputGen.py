import random

f = open('inputfile.txt','w+')
for index in range(1,234):
    value = str(random.randint(1,20))
    f.write(str(index)+" "+value+"\n")
f.close
