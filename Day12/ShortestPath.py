import math
import time
class Grid:
    def __init__(self,txt) -> None:
        self.txt = txt
        self.grid = []
        self.startPos = None # (row,column)
        self.endPos = None
        self.createGrid()
        
        self.directions = [(1,0),(-1,0),(0,1),(0,-1)]

    def createGrid(self):
        with open(self.txt) as f:
            for i,line in enumerate(f):
                row = list(line.strip())
                if not self.startPos and "S" in row:
                    startIndex = row.index("S")
                    self.startPos = (i,startIndex)
                    row[startIndex] = "a"
                if not self.endPos and "E" in row:
                    endIndex = row.index("E")
                    self.endPos = (i,endIndex)
                    row[endIndex] = "z"
                
                self.grid.append(row)

    def isValidPos(self,a):
        if a[0] < 0 or a[0] >= len(self.grid):
            return False
        elif a[1] < 0 or a[1] >= len(self.grid[0]):
            return False
        return True
    
    def distanceToGoal(self,a):
        return abs(self.endPos[0] - a[0]) + abs(self.endPos[1] - a[1])
    
    def binaryInsert(self,value,stack,index):
        # Insert a value into a stack, sorted (descending) by element at index 
        left = 0
        right = len(stack)
        # print("Stack before:", stack)
        while left < right:
            middle = left + (right-left)//2
            this = stack[middle][index]
            if this > value[index]:
                left = middle + 1
            elif this < value[index]:
                right = middle
            else:
                # print("stack after:",stack[:middle] + [value] + stack[middle:])
                return stack[:middle] + [value] + stack[middle:]
        # print("stack after:",stack[:left] + [value] + stack[left:])
        return stack[:left] + [value] + stack[left:]

    def traverseGrid(self):
        ##checks all paths but preference for those that have the lowest score, where score = numSteps + Euclidean distanceToGoal
        minSteps = math.inf
        bestPath = None
        shortestPathLengths = dict()
        shortestPathLengths[self.startPos] = 0
        stack = [(self.startPos,0,{self.startPos},self.distanceToGoal(self.startPos))]
        while stack:
            current,numSteps,currentPath,_ = stack.pop()
            if current == self.endPos:
                if numSteps < minSteps:
                    minSteps = numSteps
                    bestPath = currentPath
            else:
                for dir in self.directions:
                    nextPos = (current[0] + dir[0],current[1] + dir[1])
                    if self.isValidPos(nextPos) and nextPos not in currentPath:
                        heightDif = ord(self.grid[nextPos[0]][nextPos[1]]) - ord(self.grid[current[0]][current[1]])
                        if heightDif <= 1:
                            newSteps = numSteps+1
                            if nextPos not in shortestPathLengths.keys():
                                shortestPathLengths[nextPos] = newSteps
                            #Only add to stack if this is the shortest path to this location
                            if newSteps <= shortestPathLengths[nextPos]:
                                shortestPathLengths[nextPos] = newSteps
                                newData = [nextPos,newSteps,currentPath.union({nextPos}),self.distanceToGoal(nextPos)+newSteps]
                                stack = self.binaryInsert(newData,stack,1)
            # if self.grid[current[0]][current[1]] == 'd':
        #     print(f'Current stack has {stack} with {newSteps} steps and score of {newData[3]}')
        # print(f'Final path is: {bestPath}')
        return minSteps

    def __str__(self) -> str:
        print(f'Starting position is {self.startPos} with a goal of {self.endPos}. Grid is:')
        for line in self.grid:
            print(line)
        


if __name__ == "__main__":
    txt = "input.txt"
    grid = Grid(txt)
    start = time.perf_counter()
    print("Started Part 1 traversal")
    steps = grid.traverseGrid()
    print("Number of steps =",steps)
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 = {end - start:0.5f} seconds")