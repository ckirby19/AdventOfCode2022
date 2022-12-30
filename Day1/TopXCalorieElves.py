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
    print(getMaxXElves(3))