import time

def binaryInsert(l,val):
    left = 0
    right = len(l)
    while left<right:
        middle = left + (right - left)//2
        if l[middle] >= val:
            left = middle + 1
        else:
            right = middle - 1
    return l[:left] + [val] + l[left:]

def getMaxXElves(X):
    topX = [0]*X
    current = 0
    with open('input.txt') as f:
        for line in f:
            if line == "\n":
                if current >= topX[-1]:
                    topX = binaryInsert(topX,current)[:X]
                current = 0
            else:
                current += int(line)
    return topX,sum(topX)


if __name__ == "__main__":
    print("Starting Part 1")
    start = time.perf_counter()
    print(getMaxXElves(1))
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 = {end - start:0.5f} seconds")

    print("Starting Part 2")
    start = time.perf_counter()
    print(getMaxXElves(3))
    end = time.perf_counter()
    print(f"Time taken to complete Part 2 = {end - start:0.5f} seconds")