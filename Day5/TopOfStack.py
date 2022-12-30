
txt = "input.txt"
def makeStacks():
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
        print(cleanStacks)
    return cleanStacks

def topOfStack():
    stack = makeStacks()
    with open(txt) as f:
        for line in f:
            if line.startswith("move"):
                line = line.split()
                amount = int(line[1])
                fromIndex = int(line[3]) - 1
                toIndex = int(line[5])  - 1  
                # print("MOVE",amount,fromIndex,toIndex)
                toAdd = stack[fromIndex][0:amount]
                stack[fromIndex] = stack[fromIndex][amount:]
                # print(toAdd)
                stack[toIndex] = toAdd + stack[toIndex]
                # print("Move made",stack)
    combined = ''
    for s in stack:
        combined+=s[0]
    return combined
    



if __name__ == "__main__":
    print(topOfStack())    