import time

def findCommonLetters(a,b,findSingle):
    aSet = set()
    final = ""
    for letter in a:
        aSet.add(letter)
    for letter in b:
        if letter in aSet:
            if findSingle:
                return letter
            final += letter
    return final


def calculatePriority(txt):
    total = 0
    with open(txt) as f:
        for line in f:
            line = line.strip()
            middle = len(line)//2
            left = line[:middle]
            right = line[middle:]
            letter = findCommonLetters(left,right,True)
            if letter.islower():
                total += ord(letter) - 96
            else:
                total += ord(letter) - 38
    return total

def calculatePriority2(txt):
    total = 0
    common = None
    with open(txt) as f:
        text = [line.rstrip() for line in f]
        for i in range(0,len(text),3):
            group = text[i:i+3]
            common = findCommonLetters(findCommonLetters(group[0],group[1],False),group[2],True)
            if common.islower():
                total += ord(common) - 96
            else:
                total += ord(common) - 38
    return total

if __name__ == "__main__":
    print("Starting Part 1")
    start = time.perf_counter()
    print(calculatePriority("input.txt"))
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 = {end - start:0.5f} seconds")

    print("Starting Part 2")
    start = time.perf_counter()
    print(calculatePriority2("input.txt"))
    end = time.perf_counter()
    print(f"Time taken to complete Part 2 = {end - start:0.5f} seconds")