def countContainedRanges():
    with open('input.txt') as f:
        contained = 0
        for line in f:
            assignments = line.split(",")
            assignment1 = assignments[0].strip().split("-")
            assignment2 = assignments[1].strip().split("-")
            contain1 = int(assignment1[0]) >= int(assignment2[0]) and int(assignment1[1]) <= int(assignment2[1])
            contain2 = int(assignment2[0]) >= int(assignment1[0]) and int(assignment2[1]) <= int(assignment1[1])
            print(assignment1,assignment2,(contain1 or contain2))
            if contain1 or contain2:
                contained += 1

        return contained

def countOverlappingRanges():
    with open('input.txt') as f:
        overlapping = 0
        for line in f:
            assignments = line.split(",")
            assignment1 = assignments[0].strip().split("-")
            assignment2 = assignments[1].strip().split("-")
            contain1 = int(assignment1[0]) >= int(assignment2[0]) and int(assignment1[0]) <= int(assignment2[1])
            contain2 = int(assignment2[0]) >= int(assignment1[0]) and int(assignment2[0]) <= int(assignment1[1])
            print(assignment1,assignment2,(contain1 or contain2))
            if contain1 or contain2:
                overlapping += 1

        return overlapping


if __name__ == "__main__":
    print(countOverlappingRanges())            

