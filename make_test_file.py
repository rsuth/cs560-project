from random import randint
size = 5408*2-8
outputfile = 'testfile'

with open(outputfile, mode='w') as file:
    for i in range(1,size+1):
        file.write(str(i)+' '+str(randint(1,13))+'\n')
    file.close() 



