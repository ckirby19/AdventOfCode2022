# SNAFU is a base 5 number system that uses 2,1,0, - (minus) and = (double minus)
# Either convert each SNAFU input to decimal, add them all together and convert back
# Or create system to add SNAFU's

# class snafuCalculator():
#     def __init__(self) -> None:
#         pass

    # @staticmethod
# def add(a,b):
def calculateSum(txt):
    total = 0
    with open(txt) as f:
        for line in f:
            line = line.strip("\n")
            total += convertFromSNAFU(line)
    return total

def convertToSNAFU(a):
    #convert from decimal to snafu
    output = ""
    #find the two 5 slots that the number will be between
    num = 1
    while 5**num < a:
        num+=1
    return num


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
    # print(convertToSNAFU(decimalSum))
