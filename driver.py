import re
from HexGrid import HexGrid
from problemsearch import graph_search
import time

path_to_file = 'inputfile.txt'

nodes = []
nodes.append(0)
with open(path_to_file) as input:
    for line in input:
        m = re.match(re.compile(r'(\d+) (-?\d+)'), line)
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

for node in solution[0]:
    print(node)
print("MINIMAL-COST PATH COSTS: "+str(solution[1]))
print(tock(start))
