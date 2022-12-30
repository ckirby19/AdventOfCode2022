
def getMax():
    best = 0
    current = 0
    with open('input.txt') as f:

        for line in f:
            if line == "\n":
                best = max(current,best)
                # current = 0
            else:
                current += int(line)
    return best


if __name__ == "__main__":
    print(getMax())