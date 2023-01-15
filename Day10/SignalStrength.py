def processSprite(cycle, x):
    mid = cycle % 40
    # Are we about to enter a new row?
    if mid == 0:
        # row += 1
        print() #New line
    if mid-1 <= x <= mid+1:
        print("#", end='')
    else:
        print(".", end='')

def calculateSignalStrength(txt):
    strengthTimes = {20,60,100,140,180,220}
    finalSum = 0
    with open(txt) as f:
        cycles = 0
        X = 1
        for line in f:
            cycles += 1
            processSprite(cycles,X)
            if cycles in strengthTimes:
                finalSum += X*cycles
            line = line.strip('/n').split()
            if line[0] == "addx":
                cycles += 1
                if cycles in strengthTimes:
                    finalSum += X*cycles
                X += (int(line[1]))
                processSprite(cycles,X)

    return finalSum

if __name__ == "__main__":
    txt = "input.txt"
    print(calculateSignalStrength(txt))
            
            