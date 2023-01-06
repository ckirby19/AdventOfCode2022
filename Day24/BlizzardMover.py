import math
class Grid():
    def __init__(self,txt) -> None:
        self.txt = txt
        # All coordinates are in the form (row,column)
        self.startPos = (0,1)
        self.motion = {'>':(0,1),'<':(0,-1),'^':(-1,0),'v':(1,0)}
        self.blizzardPositions = dict()
        self.blizzardPositionsAtTime = dict()
        self.grid = self.createInitialGrid()
        self.goal = (len(self.grid)-1,len(self.grid[0])-2)
        for line in self.grid:
            print(line)
        
    
    def createInitialGrid(self):
        with open(self.txt) as f:
            grid = []
            for row,line in enumerate(f):
                line = list(line.strip())
                grid.append(line)
                for column,char in enumerate(line):
                    if char in self.motion.keys():
                        if (row,column) in self.blizzardPositions:
                            self.blizzardPositions.append(char)
                        else:
                            self.blizzardPositions[(row,column)] = [char]
        self.blizzardPositionsAtTime[0] = self.blizzardPositions
        return grid

    def getNextBlizzard(self,nextTime):
        nextBlizPos = dict()
        if nextTime in self.blizzardPositionsAtTime:
            nextBlizPos = self.blizzardPositionsAtTime[nextTime]
        else:
            #We need to calculate our next blizzard positions and update our dictionary
            thisBliz = self.blizzardPositionsAtTime[nextTime-1]
            for pos in thisBliz:
                for arrow in thisBliz[pos]:
                    nextPosRow = pos[0]+self.motion[arrow][0]
                    if nextPosRow == 0:
                        nextPosRow = len(self.grid[0])-2
                    elif nextPosRow == len(self.grid[0])-1:
                        nextPosRow = 1
                    nextPosColumn = pos[1]+self.motion[arrow][1]
                    if nextPosColumn == 0:
                        nextPosColumn = len(self.grid[0])-2
                    elif nextPosColumn == len(self.grid[0])-1:
                        nextPosColumn = 1
                        
                    nextPos = (nextPosRow,nextPosColumn)
                    if nextPos in nextBlizPos:
                        nextBlizPos[nextPos].append(arrow)
                    else:
                        nextBlizPos[nextPos] = [arrow]
            self.blizzardPositionsAtTime[nextTime] = nextBlizPos
        return nextBlizPos

    def simulate(self):
        bestTime = math.inf
        stack = [(self.startPos,0)]
        while stack:
            currentPos,currentTime = stack.pop()
            if currentPos == self.goal:
                bestTime = min(bestTime,currentTime)
                continue
            #In order to choose our possible next positions, we advance our blizzard forward in time
            nextTime = currentTime + 1
            nextBlizPos = self.getNextBlizzard(nextTime)
            
            #Now we check all directions for movement
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            canMove = False
            for d in dirs:
                
                myNextPos = (currentPos[0]+d[0],currentPos[1]+d[1])
                # print("Direction",d,"New pos:",myNextPos)
                # print(nextBlizPos)
                if myNextPos not in nextBlizPos and myNextPos[0] >= 0 and self.grid[myNextPos[0]][myNextPos[1]] != "#":
                    canMove = True
                    stack.append((myNextPos,nextTime))
                    # print(stack)
            if canMove == False:
                # Just wait
                stack.append((currentPos,nextTime))
            # print(stack)

        return bestTime



if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: {} <input.txt>".format(sys.argv[0]))
        sys.exit(1)

    grid = Grid(sys.argv[1])
    print("Part 1: {}".format(grid.simulate()))
    # print("Part 2: {}".format(grid.countEmptyTiles()))






