import math
class Grid():
    def __init__(self,txt) -> None:
        self.txt = txt
        # All coordinates are in the form (row,column)
        self.startPos = (0,1)
        self.motion = {'>':(0,1),'<':(0,-1),'^':(-1,0),'v':(1,0)}
        self.walls = set()
        self.blizzardPositions = dict()
        self.blizzardPositionsAtTime = dict()
        self.grid = self.createInitialGrid()
        self.goal = (len(self.grid)-1,len(self.grid[0])-2)
        self.lcmOfGrid = self.lcmCalculator(len(self.grid)-2,len(self.grid[0])-2) #minus two for the wall edges

        self.getAllBlizzards()
    

    def lcmCalculator(self,a,b):
        if a > b:
            greater = a
        else:
            greater = b
        while(True):
            if((greater % a == 0) and (greater % b == 0)):
                lcm = greater
                break
            greater += 1
        return lcm

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
                    elif char == "#":
                        self.walls.add((row,column))

        self.blizzardPositionsAtTime[0] = self.blizzardPositions
        return grid

    def getAllBlizzards(self):
        for nextTime in range(1,self.lcmOfGrid):
            nextBlizPos = dict()
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

    def simulate(self):
        bestTime = math.inf
        stack = [(self.startPos,0)]
        bestTimePath = dict()
        seen = set()
        while stack:
            print(len(stack))
            currentPos,currentTime = stack.pop()
            if currentPos == self.goal:
                print("WE MADE IT",currentTime)
                bestTime = min(bestTime,currentTime)
                continue
            #Check if we were in this pos previously with blizzard in equivalent point in time
            inLoop = False
            for other in seen:
                val = other[0]
                otherTime = other[1]
                if val == currentPos:
                    if abs(currentTime - otherTime)%self.lcmOfGrid == 0:
                        inLoop = True
                        break
            if inLoop == True:
                continue
            seen.add((currentPos,currentTime))

            #In order to choose our possible next positions, we advance our blizzard forward in time
            nextTime = currentTime + 1
            nextBlizPos = self.blizzardPositionsAtTime[nextTime%self.lcmOfGrid]
            
            #Now we check all directions for movement
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            canMove = False
            for d in dirs:
                myNextPos = (currentPos[0]+d[0],currentPos[1]+d[1])
                if myNextPos not in nextBlizPos and myNextPos[0] >= 0 and self.grid[myNextPos[0]][myNextPos[1]] != "#":
                    canMove = True
                    stack.append((myNextPos,nextTime))
            if canMove == False:
                # Just wait
                stack.append((currentPos,nextTime))
        return bestTime

    def move_optimally(self):
        begin = self.startPos
        target = self.goal
        states = {(begin,0)}
        highestSteps = 0
        while target not in states:

            new_states = set()

            for ((x,y),time) in states:
                for n in [(x-1, y),
                          (x+1, y),
                          (x, y-1),
                          (x, y+1)]:
                    if n in self.walls or n in self.blizzardPositionsAtTime[time]:
                        continue
                    nextStep = time+1
                    highestSteps = max(nextStep,highestSteps)
                    new_states.add((n,nextStep))
                    
                if (x, y) not in self.walls and (x, y) not in self.blizzardPositionsAtTime[time]:
                    nextStep = time+1
                    new_states.add(((x, y),time))

            states = new_states

        return highestSteps



if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: {} <input.txt>".format(sys.argv[0]))
        sys.exit(1)

    grid = Grid(sys.argv[1])
    print("Part 1: {}".format(grid.move_optimally()))
    # print("Part 2: {}".format(grid.countEmptyTiles()))






