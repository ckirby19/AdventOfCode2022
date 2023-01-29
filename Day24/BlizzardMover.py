import math
from collections import deque
class Grid():
    def __init__(self,txt) -> None:
        self.txt = txt
        # All coordinates are in the form (row,column)
        self.dirs = [(1,0),(-1,0),(0,1),(0,-1),(0,0)]
        self.motion = {'>':(0,1),'<':(0,-1),'^':(-1,0),'v':(1,0)}
        self.blizzardPositions = dict()
        self.blizzardPositionsAtTime = dict()
        self.walls = set() #Generated from initial grid
        self.grid = self.createInitialGrid()
        self.startPos = (0,1)
        self.goal = (len(self.grid)-1,len(self.grid[0])-2)
        self.lcmOfGrid = self.lcmCalculator(len(self.grid)-2,len(self.grid[0])-2) #minus two for the wall edges
        
        self.getAllBlizzards()

        time1,blizzardTime = self.simulate(self.startPos,self.goal,0)
        print(f"Part 1 time: {time1}")
        time2,blizzardTime = self.simulate(self.goal,self.startPos,blizzardTime)
        time3,blizzardTime = self.simulate(self.startPos,self.goal,blizzardTime)
        print(f"Part 2 time: {time1 + time2 + time3}")

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

    def getAllBlizzards(self):
        for nextTime in range(1,self.lcmOfGrid):
            nextBlizPos = dict()
            thisBliz = self.blizzardPositionsAtTime[nextTime-1]
            for pos in thisBliz:
                for arrow in thisBliz[pos]:
                    nextPosRow = pos[0]+self.motion[arrow][0]
                    if nextPosRow == 0:
                        nextPosRow = len(self.grid)-2
                    elif nextPosRow == len(self.grid)-1:
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

    def simulate(self,start,goal,blizzardStartTime):
        #dp[t][x][y] = shortest time if I'm currently at pos row, column and the time mod LCM is t
        dp = [[[math.inf for column in range(len(self.grid[0]))] for row in range(len(self.grid))] for t in range(self.lcmOfGrid)]
        dp[blizzardStartTime][start[0]][start[1]] = 0

        deq = deque()
        deq.append((0,start,blizzardStartTime))
        while deq:
            bestTimeAtPos,currentPos,blizzardTime = deq.popleft()
            if dp[blizzardTime][currentPos[0]][currentPos[1]] != bestTimeAtPos:
                #Then we are on a non optimal route
                continue 
            nxtBlizzardTime = (blizzardTime + 1) % self.lcmOfGrid
            nxtBlizPositions = self.blizzardPositionsAtTime[nxtBlizzardTime]
            for dir in self.dirs: #Includes zero motion dir
                nxtPos = (currentPos[0]+dir[0],currentPos[1]+dir[1])
                if nxtPos[0] >= 0 and nxtPos[0] < len(self.grid) and self.grid[nxtPos[0]][nxtPos[1]] != "#":
                    if nxtPos not in nxtBlizPositions and dp[nxtBlizzardTime][nxtPos[0]][nxtPos[1]] > bestTimeAtPos + 1:
                        dp[nxtBlizzardTime][nxtPos[0]][nxtPos[1]] = bestTimeAtPos + 1
                        deq.append((bestTimeAtPos+1, nxtPos, nxtBlizzardTime))

        ans = math.inf
        finalBlizzardTime = None
        for blizzardTime in range(self.lcmOfGrid):
            if ans > dp[blizzardTime][goal[0]][goal[1]]:
                ans = dp[blizzardTime][goal[0]][goal[1]]
                finalBlizzardTime = blizzardTime
        return ans,finalBlizzardTime

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: {} <input.txt>".format(sys.argv[0]))
        sys.exit(1)

    grid = Grid(sys.argv[1])






