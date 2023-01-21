import math
import time
from collections import deque
class Grid:
    def __init__(self,txt,isPart2) -> None:
        self.txt = txt
        self.isPart2 = isPart2
        self.possibleStartPositions = []
        self.grid = []
        self.endPos = None
        self.directions = [(1,0),(-1,0),(0,1),(0,-1)]
        startPositions = self.getStartPositions()
        minSteps = math.inf
        for pos in startPositions:
            steps = self.traverseGrid(pos)
            if steps:
                minSteps = min(steps,minSteps)
        print("Number of steps is: ",minSteps)
        

    def getStartPositions(self):
        startPositions = []
        with open(self.txt) as f:
            for i,line in enumerate(f):
                row = list(line.strip())
                for j,char in enumerate(row):
                    if char == "S":
                        row[j] = 'a'
                        startPositions.append((i,j))
                    elif char == "E":
                        self.endPos = (i,j)
                        row[j] = "z"
                    elif self.isPart2 and char == "a":
                        startPositions.append((i,j))
                self.grid.append(row)
        return startPositions

    def isValidPos(self,a):
        if a[0] < 0 or a[0] >= len(self.grid):
            return False
        elif a[1] < 0 or a[1] >= len(self.grid[0]):
            return False
        return True

    def traverseGrid(self,start):
        seen = set()
        stack = deque()
        stack.append((start,0))
        while stack:
            current,numSteps = stack.popleft()
            if current == self.endPos:
                return numSteps
            elif current in seen:
                continue
            else:
                seen.add(current)
                for dir in self.directions:
                    nextPos = (current[0] + dir[0],current[1] + dir[1])
                    if self.isValidPos(nextPos):
                        heightDif = ord(self.grid[nextPos[0]][nextPos[1]]) - ord(self.grid[current[0]][current[1]])
                        if heightDif <= 1:
                            stack.append((nextPos,numSteps + 1))

if __name__ == "__main__":
    txt = "input.txt"
    
    start = time.perf_counter()
    print("Started Part 1 traversal")
    grid = Grid(txt,False)
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 = {end - start:0.5f} seconds")

    start = time.perf_counter()
    print("Started Part 2 traversal")
    grid2 = Grid(txt,True)
    end = time.perf_counter()
    print(f"Time taken to complete Part 2 = {end - start:0.5f} seconds")

