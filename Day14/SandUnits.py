import math
import time
class SandGrid:
    def __init__(self,txt,isPart2) -> None:
        self.txt = txt
        self.isPart2 = isPart2
        self.grid = [] # (x,y) coordinates
        self.sandStart = (500,0)
        self.minX = 500
        self.maxX = 500
        self.maxY = 0
        self.restingSand = 0
        self.time = 0
        self.flowing = False
        self.createGrid()
        
        self.directions = [(0,1),(-1,1),(1,1)] # Sand turns to rock if cannot take any of these directions

    def createGrid(self):
        rowsWithRocks = dict() #A mapping of row: rock positions in that row
        with open(self.txt) as f:
            for line in f:
                line = line.strip().split()
                for y in range(0,len(line)-1,2):
                    rock1 = line[y].split(",")
                    rock2 = line[y+2].split(",")
                    rockStartX,rockStartY = int(rock1[0]),int(rock1[1])
                    rockEndX,rockEndY = int(rock2[0]),int(rock2[1])
                    if rockStartX == rockEndX:
                        #Then this straight line is in Y
                        rockMin = min(rockStartY,rockEndY)
                        rockMax = max(rockStartY,rockEndY)
                        self.maxY = max(rockMax,self.maxY)
                        
                        for y in range(rockMin,rockMax+1):
                            if y in rowsWithRocks.keys():
                                rowsWithRocks[y].add(rockStartX)
                            else:
                                rowsWithRocks[y] = {rockStartX}
                    else:
                        rockMin = min(rockStartX,rockEndX)
                        rockMax = max(rockStartX,rockEndX)
                        self.minX = min(rockMin,self.minX)
                        self.maxX = max(rockMax,self.maxX)
                        for x in range(rockMin,rockMax+1):
                            if rockStartY in rowsWithRocks.keys():
                                rowsWithRocks[rockStartY].add(x)
                            else:
                                rowsWithRocks[rockStartY] = {x}
        #minX -> 0, maxX -> maxX - minX
        for y in range(self.maxY+1):
            toAdd = []
            for x in range(self.minX,self.maxX+1):
                if y in rowsWithRocks.keys():
                    if x in rowsWithRocks[y]:
                        toAdd.append('#')
                    else:
                        toAdd.append('.')
                else:
                    toAdd.append('.')
            self.grid.append(toAdd)
        
        if self.isPart2:
            #Now we must reshape our grid slightly - We need to pad to the left and right
            self.maxY += 2
            padLeft = (self.maxY - (self.sandStart[0] - self.minX))
            padRight = (self.maxY - (self.maxX - self.sandStart[0]))
            self.minX -= padLeft
            self.maxX += padRight
            self.grid.append(['.']*len(self.grid[0]))
            self.grid.append(['#']*len(self.grid[0]))

            paddedGrid = []
            for y in range(len(self.grid)):
                toAdd = ['.']*padLeft + self.grid[y] + ['.']*padRight
                paddedGrid.append(toAdd)
            paddedGrid[-1] = ['#']*len(paddedGrid[0])
            self.grid = paddedGrid

    def inRockRange(self,a):
        xBool = 0 <= a[0] < len(self.grid[0])
        yBool = a[1] < len(self.grid)
        return xBool and yBool

    def advanceTime(self):
        #advances until sand lands, or if sand does not land then sets the flag
        self.time += 1
        currentPos = (self.sandStart[0] - self.minX,0)
        moveType = 0
        while moveType <= 2:
            dir = self.directions[moveType]
            nextPos = (currentPos[0] + dir[0], currentPos[1] + dir[1])
            if not self.inRockRange(nextPos):
                self.flowing = True
                break
            elif self.grid[nextPos[1]][nextPos[0]] == '.':
                #Then we can move here
                currentPos = nextPos
                moveType = 0
            else:
                moveType+=1
        if not self.flowing:
            #Then the sand has landed
            self.restingSand += 1
            self.grid[currentPos[1]][currentPos[0]] = 'o'

    def advanceUntilBlocked(self):
        #For part 2, with floor at bottom, this will continuously add sand until sand blocks the source
        blocked = False
        while blocked == False:
            self.time += 1
            currentPos = (self.sandStart[0] - self.minX,0)
            moveType = 0
            while moveType <= 2:
                dir = self.directions[moveType]
                nextPos = (currentPos[0] + dir[0], currentPos[1] + dir[1])
                if self.grid[nextPos[1]][nextPos[0]] == '.':
                    #Then we can move here
                    currentPos = nextPos
                    moveType = 0
                else:
                    moveType += 1
            self.restingSand += 1
            self.grid[currentPos[1]][currentPos[0]] = 'o'
            if currentPos == (self.sandStart[0] - self.minX,0):
                blocked = True

    def simulate(self):
        if self.isPart2:
            self.advanceUntilBlocked()
        else:
            while self.flowing == False:
                self.advanceTime()
        return self.restingSand

    def __str__(self):
        for line in self.grid:
            print(line)
        return (f'X = {self.minX,self.maxX}, Y is {self.maxY}')
                
if __name__ == "__main__":
    txt = "input.txt"
    
    start = time.perf_counter()
    print("Started Part 1 grid creation and simulation")
    grid = SandGrid(txt,False)
    print(grid.simulate())
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 = {end - start:0.5f} seconds")  
  
    start = time.perf_counter()
    print("Started Part 2 grid creation")
    grid2 = SandGrid(txt,True)
    print(grid2.simulate())
    end = time.perf_counter()
    print(f"Time taken to complete Part 2 = {end - start:0.5f} seconds")      

                        
