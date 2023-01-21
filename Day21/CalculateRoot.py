from sympy import symbols, solve
import time
ops = { '+': lambda x,y: x+y, '-': lambda x,y: x-y, '*': lambda x,y: x*y, '/': lambda x,y: x/y, '=': lambda x,y: solve(x-y)[0]}

def readInput(txt,part2):
    data = dict()
    with open(txt) as f:
        for line in f:
            line = line.strip().split()
            name = line[0].strip(":")
            if name == 'root' and part2:
                rootData = line[1:]
                rootData[1] = '='
                data[name] = rootData
            elif len(line) == 4:
                data[name] = line[1:]
            else:
                data[name] = line[1]
    return readData(data,'root',part2)

def readData(data,name,part2):
    monkeyData = data[name]
    if name == "humn" and part2:
        x = symbols('x')
        data[name] = x
        return x
    elif isinstance(monkeyData,list):
        left = readData(data,monkeyData[0],part2)
        right = readData(data,monkeyData[2],part2)
        newVal = ops[monkeyData[1]](left,right)
        data[name] = newVal
        return newVal
    else:
        return int(monkeyData)

if __name__ == "__main__":
    txt = "input.txt"
    start = time.perf_counter()
    print("Started Part 1")
    print(readInput(txt,False))
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 = {end - start:0.5f} seconds")  
  
    start = time.perf_counter()
    print("Started Part 2")
    print(readInput(txt,True))
    end = time.perf_counter()
    print(f"Time taken to complete Part 2 = {end - start:0.5f} seconds")      