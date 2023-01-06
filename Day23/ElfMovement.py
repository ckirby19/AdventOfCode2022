class Elf():
    def __init__(self,startPos) -> None:
        self.currentPos = startPos
        self.movementPreference = [(0,-1),(0,1),(-1,0),(1,0)]

class Grid():
    def __init__(self,txt) -> None:
        self.txt = txt
        self.gridMinX = 0
        self.gridMinY = 0
        self.gridMaxX = 0
        self.gridMaxY = 0
        self.elfPositions = set()
        self.elves = set()
        self.getInitialElfPos()
        self.rounds = 10

        for _ in range(self.rounds):
            self.moveElves()

        self.emptyTiles = self.countEmptyTiles()

    def getInitialElfPos(self):
        with open(self.txt) as f:
            for y,line in enumerate(f):
                line = line.strip()
                for x,char in enumerate(line):
                    if char == '#':
                        elf = Elf((x,y))
                        self.elves.add(elf)
                        self.elfPositions.add((x,y))
                        self.gridMinX = min(self.gridMinX,x)
                        self.gridMinY = min(self.gridMinY,y)
                        self.gridMaxX = max(self.gridMaxX,x)
                        self.gridMaxY = max(self.gridMaxY,y)    
    
    def moveElves(self):
        proposedPositions = dict() #Dictionary of positions: elves who want to move there
        for elf in self.elves:
            elfPos = elf.currentPos
            occupiedCells = set()
            for i in range(-1,2):
                for j in range(-1,2):
                    if (i,j) != (0,0):
                        if (elfPos[0]+i,elfPos[1]+j) in self.elfPositions:
                            occupiedCells.add((elfPos[0]+i,elfPos[1]+j))
            #Only consider move if occupiedCells is not empty
            if len(occupiedCells) > 0:
                motionIndex = 0
                while motionIndex < len(elf.movementPreference):
                    motion = elf.movementPreference[motionIndex]
                    canMove = True
                    nextPos = (elfPos[0]+motion[0],elfPos[1]+motion[1])
                    canMove &= nextPos not in occupiedCells

                    if motion[0] != 0:
                        #Then we are moving East or West
                        canMove &= (elfPos[0]+motion[0],elfPos[1]+1) not in occupiedCells
                        canMove &= (elfPos[0]+motion[0],elfPos[1]-1) not in occupiedCells
                    else:
                        canMove &= (elfPos[0]+1,elfPos[1]+motion[1]) not in occupiedCells
                        canMove &= (elfPos[0]-1,elfPos[1]+motion[1]) not in occupiedCells
                    
                    if canMove:
                        if nextPos not in proposedPositions:
                            proposedPositions[nextPos] = [elf]
                        else:
                            proposedPositions[nextPos].append(elf)

                        del elf.movementPreference[motionIndex]
                        elf.movementPreference.append(motion)
                        break
                    else:
                        motionIndex += 1
        # Now we move to the second half of the motion
        # If there are moves than one elves who want to move to the same position, then they are not allowed to move
        for nextPos in proposedPositions:
            if len(proposedPositions[nextPos]) == 1:
                elf = proposedPositions[nextPos][0]
                self.elfPositions.remove(elf.currentPos)
                elf.currentPos = nextPos
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
    print("Part 1: {}".format(grid.emptyTiles))
    # print("Part 2: {}".format(grid.countEmptyTiles()))
