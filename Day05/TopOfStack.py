import time

def makeStacks(txt):
    with open(txt) as f:
        dirtyStacks = []
        topText = []
        line = f.readline()
        while not line.startswith("move"):
            topText.append(line)
            line = f.readline()
            
        dirtyStacks = [[] for i in range(len(topText[0]))]
        for row in range(0,len(topText)-2):
            for i in range(1,len(dirtyStacks),4):
                if topText[row][i] != " ":
                    dirtyStacks[i].append(topText[row][i])

        cleanStacks = []
        for stack in dirtyStacks:
            if stack != []:
                cleanStacks.append(stack)
    return cleanStacks

def topOfStack(txt):
    stack = makeStacks(txt)
    with open(txt) as f:
        for line in f:
            if line.startswith("move"):
                line = line.split()
                amount = int(line[1])
                fromIndex = int(line[3]) - 1
                toIndex = int(line[5])  - 1  
                toAdd = stack[fromIndex][0:amount]
                stack[fromIndex] = stack[fromIndex][amount:]
                stack[toIndex] = toAdd + stack[toIndex]

    combined = ''
    for s in stack:
        combined+=s[0]
    return combined


if __name__ == "__main__":
    txt = "input.txt"
    print("Starting Part 2")
    start = time.perf_counter()
    print(topOfStack(txt))
    end = time.perf_counter()
    print(f"Time taken to complete Part 2 = {end - start:0.5f} seconds")   