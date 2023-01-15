import time
import re

def countRanges(txt,indexToCheck):
    with open(txt) as f:
        count = 0
        
        for line in f:
            assignments = re.findall("\d+-\d+",line)
            assignment1 = assignments[0].split("-")
            assignment2 = assignments[1].split("-")
            contain1 = int(assignment1[0]) >= int(assignment2[0]) and int(assignment1[indexToCheck]) <= int(assignment2[1])
            contain2 = int(assignment2[0]) >= int(assignment1[0]) and int(assignment2[indexToCheck]) <= int(assignment1[1])
            if contain1 or contain2:
                count += 1

        return count

if __name__ == "__main__":
    txt = "input.txt"
    print("Starting Part 1")
    start = time.perf_counter()
    print(countRanges(txt,1))
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 = {end - start:0.5f} seconds")

    print("Starting Part 2")
    start = time.perf_counter()
    print(countRanges(txt,0))
    end = time.perf_counter()
    print(f"Time taken to complete Part 2 = {end - start:0.5f} seconds")
        

