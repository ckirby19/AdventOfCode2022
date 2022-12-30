import time
import itertools

def createEdgeDict(txt):
    flowRates = dict()
    # Initial creation of (u,v):distance where (u,u) = 0, (u,v) if directly connected = 1
    distances = dict() 
    allValves = set()
    nonZeroValves = set()
    with open(txt) as f:
        for line in f:
            line = line.strip().split()
            name = line[1]
            distances[(name,name)] = 0
            rate = int(line[4][5:].strip(";"))
            allValves.add(name)
            if rate > 0:
                nonZeroValves.add(name)
            connections = line[9:]
            for i in range(len(connections)):
                connection = connections[i].strip(",")
                distances[(name,connection)] = 1
                connections[i] = connection
            flowRates[name] = rate 
    return distances,flowRates,allValves,nonZeroValves

def getAllshortestPaths(allValves,distances):
    #Using Floyd-Warshall algorithm

    d = {(u,v): float('inf') if u != v else 0 for u in allValves for v in allValves}
    for (u,v), w in distances.items():
        d[(u,v)] = w
    
    # Does the shortest path use k or not? 
    # Include k if d_uk + d_kv < d_uk
    for k in allValves:
        for u in allValves:
            for v in allValves:
                d[(u,v)] = min(d[(u,v)],d[(u,k)] + d[(k,v)])
    return d
                
def traverseGraph(startTime,shortestPathBetween,flowRates,nonZeroValves):
    stack = [[startTime,'AA',set(),0]]
    maxFlowRate = 0
    while stack:
        currentCase = stack.pop()
        time,current,openValves,currentFlow = currentCase
        if time == 0:
            maxFlowRate = max(maxFlowRate,currentFlow)
        if len(openValves) == len(nonZeroValves):
            currentFlowRate = 0
            for v in openValves:
                currentFlowRate += flowRates[v]
            maxFlowRate = max(maxFlowRate,currentFlow + currentFlowRate*time)
        else:
            currentFlowRate = 0
            for v in openValves:
                currentFlowRate += flowRates[v]

            noTimeLeft = True # For checking if there is any time left to move and open another valve
            for otherValve in nonZeroValves:
                if otherValve not in openValves:
                    timeAfterMoveAndOpen = time - shortestPathBetween[(current,otherValve)]-1
                    if timeAfterMoveAndOpen >= 0:
                        noTimeLeft = False
                        moveAndOpen = [timeAfterMoveAndOpen,otherValve,openValves.union({otherValve}),currentFlow + currentFlowRate*(time-timeAfterMoveAndOpen)]
                        if len(stack) == 0:
                            stack.append(moveAndOpen)
                        else:
                            stack = binaryInsert(moveAndOpen,stack,3)
            if noTimeLeft:
                #If there is not time, just stay still and add on the remaining flow
                maxFlowRate = max(maxFlowRate,currentFlow + currentFlowRate*time)
    return maxFlowRate

def twoTraverseGraph(shortestPathBetween,flowRates,nonZeroValves):
    #Take nonZeroValves and split in two, with every combination ignoring cases where myself and elephant are swapped
    # This will give us a total of (x = len(nonZeroValves)): (X choose X//2)/2 combinations

    combos = itertools.combinations(nonZeroValves,len(nonZeroValves)//2) #What will happen here if len is not divisible by 2
    l = [[set(x), set(y for y in nonZeroValves if y not in x)] for x in combos]
    finalCombos = l[:len(l)//2]
    bestTotal = 0
    for combo in finalCombos:
        me = traverseGraph(26,shortestPathBetween,flowRates,combo[0])
        other = traverseGraph(26,shortestPathBetween,flowRates,combo[1])
        bestTotal = max(bestTotal,me+other)
    return bestTotal


def binaryInsert(value,stack,index):
    # Insert a value into a stack, sorted (ascending) by element at index 
    left = 0
    right = len(stack)
    while left < right:
        middle = left + (right-left)//2
        this = stack[middle][index]
        if this < value[index]:
            left = middle + 1
        elif this > value[index]:
            right = middle
        else:
            return stack[:middle] + [value] + stack[middle:]
    return stack[:left] + [value] + stack[left:]

if __name__ == "__main__":
    txt = "input.txt"
    shortestPathBetween,flowRates,allValves,nonZeroValves = createEdgeDict(txt)
    shortestPathBetween = getAllshortestPaths(allValves,shortestPathBetween)
    start = time.perf_counter()
    print("Started Part 1 traversal")
    print(traverseGraph(30,shortestPathBetween,flowRates,nonZeroValves))
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 = {end - start:0.3f} seconds")

    start = time.perf_counter()
    print("Started Part 2 traversal")
    print(twoTraverseGraph(shortestPathBetween,flowRates,nonZeroValves))
    end = time.perf_counter()
    print(f"Time taken to complete Part 2 = {end - start:0.3f} seconds")
    