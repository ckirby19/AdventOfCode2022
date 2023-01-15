class Grid():
    def __init__(self,txt) -> None:
        self.txt = txt
        self.gridMinX = 0
        self.gridMinY = 0
        self.gridMaxX = 0
        self.gridMaxY = 0
        self.movementPreference = [(0,-1),(0,1),(-1,0),(1,0)]
        self.elfPositions = set()
        self.getInitialElfPos()
        self.rounds = 10

    def simulate(self):
        i = 0
        prevElfs = {}
        while self.elfPositions != prevElfs:
            prevElfs = self.elfPositions.copy()
            self.moveElves(i)
            i += 1
            if i == self.rounds:
                for elf in self.elfPositions:
                    print(elf)
                print("Part 1:", self.countEmptyTiles())
        print("Part 2:",i)
        i = 0

    def getInitialElfPos(self):
        with open(self.txt) as f:
            for y,line in enumerate(f):
                line = line.strip()
                for x,char in enumerate(line):
                    if char == '#':
                        self.elfPositions.add((x,y))
                        self.gridMinX = min(self.gridMinX,x)
                        self.gridMinY = min(self.gridMinY,y)
                        self.gridMaxX = max(self.gridMaxX,x)
                        self.gridMaxY = max(self.gridMaxY,y)    
    
    def moveElves(self,indexShift):
        proposedPositions = dict() #Dictionary of positions: elves who want to move there
        for elfPos in self.elfPositions:
            occupiedCells = set()
            for i in range(-1,2):
                for j in range(-1,2):
                    if (i,j) != (0,0):
                        val = (elfPos[0]+i,elfPos[1]+j)
                        if val in self.elfPositions:
                            occupiedCells.add(val)
            #Only consider move if occupiedCells is not empty
            if len(occupiedCells) > 0:
                motionIndex = 0
                while motionIndex < len(self.movementPreference):
                    motion = self.movementPreference[(motionIndex + indexShift)%len(self.movementPreference)]
                    nextPos = (elfPos[0]+motion[0],elfPos[1]+motion[1])
                    canMove = nextPos not in occupiedCells

                    if motion[0] != 0:
                        #Then we are moving East or West
                        canMove &= (elfPos[0]+motion[0],elfPos[1]+1) not in occupiedCells
                        canMove &= (elfPos[0]+motion[0],elfPos[1]-1) not in occupiedCells
                    else:
                        canMove &= (elfPos[0]+1,elfPos[1]+motion[1]) not in occupiedCells
                        canMove &= (elfPos[0]-1,elfPos[1]+motion[1]) not in occupiedCells
                    
                    if canMove:
                        if nextPos not in proposedPositions:
                            proposedPositions[nextPos] = [elfPos]
                        else:
                            proposedPositions[nextPos].append(elfPos)
                        break
                    else:
                        motionIndex += 1
        # Now we move to the second half of the motion
        # If there are moves than one elves who want to move to the same position, then they are not allowed to move
        for nextPos in proposedPositions:
            if len(proposedPositions[nextPos]) == 1:
                elfPos = proposedPositions[nextPos][0]
                self.elfPositions.remove(elfPos)
                self.elfPositions.add(nextPos)
                self.gridMinX = min(self.gridMinX,nextPos[0])
                self.gridMinY = min(self.gridMinY,nextPos[1])
                self.gridMaxX = max(self.gridMaxX,nextPos[0])
                self.gridMaxY = max(self.gridMaxY,nextPos[1])   
            
        
    def countEmptyTiles(self):
        x = self.gridMaxX + 1 - self.gridMinX
        y = self.gridMaxY + 1 - self.gridMinY
        return x*y - len(self.elfPositions)
                    

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: {} <input.txt>".format(sys.argv[0]))
        sys.exit(1)

    grid = Grid(sys.argv[1])
    grid.simulate()
