def calculateSum(txt):
    total = 0
    with open(txt) as f:
        for line in f:
            line = line.strip("\n")
            total += convertFromSNAFU(line)
    return total

def convertFromSNAFU(a):
    #Convert from snafu form to decimal
    total = 0
    for i in range(len(a)):
        num = a[len(a)-1-i]
        if num == "-":
            num = -1
        elif num == "=":
            num = -2
        else:
            num = int(num)
        num = num * pow(5,i)
        total += num
    return total


if __name__ == "__main__":
    txt = "input.txt"
    decimalSum = calculateSum(txt)
    print(decimalSum)
    print(convertFromSNAFU("2011-=2=-1020-1===-1"))
