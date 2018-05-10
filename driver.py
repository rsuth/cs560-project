import re
from HexGrid import HexGrid
from problemsearch import graph_search
import time

path_to_file = 'test_input_2.txt'

nodes = []
nodes.append(0)
with open(path_to_file) as input:
    for line in input:
        m = re.match(re.compile(r'(\d+) (-?\d+)'), line)
        if line != '\n':
            nodes.append(int(m.group(2)))
    input.close()

def tic():
    "Return current time representation"
    return time.time()

def tock(t):
    "Return time elapsed in sec since t where t is the output of tic()"
    return time.time() - t

start = tic()
test = HexGrid(nodes)
solution = graph_search(test)

output_file = open('output.txt', 'w+')
for node in reversed(solution[0]):
    output_file.write(str(node) + '\n')
output_file.write("MINIMAL-COST PATH COSTS: "+str(solution[1]) + '\n')
output_file.write(str(tock(start)))
