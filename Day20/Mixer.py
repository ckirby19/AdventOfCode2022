def ReadAndMix(txt,x,y):
    mixed = []
    with open(txt) as f:
        for line in f:
            mixed.append(int(line.strip()) * y)

    indices = list(range(len(mixed)))

    for i in indices*x:
        j = indices.index(i)
        indices.pop(j)
        indices.insert((j+mixed[i]) % (len(indices)), i)
        
    zero = indices.index(mixed.index(0))
    total = 0
    for n in [1000,2000,3000]:
        total += mixed[indices[(zero+n) % len(mixed)]]
    return total

if __name__ == "__main__":
    txt = "input.txt"
    print("Part 1 Answer:", ReadAndMix(txt,1,1))
    print("Part 2 Answer:", ReadAndMix(txt,10,811589153))
