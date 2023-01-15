import math
import re
import numpy as np
class Grid():
    def __init__(self,txt,isPart2) -> None:
        self.txt = txt
        self.isPart2 = isPart2
        # All coordinates are in the form (row,column)
        self.grid,self.path = self.readInput()
        self.directions = {'R':np.array((0,1)), 'L':np.array((0,-1)), 'T':np.array((0,-1)), 'B':np.array((0,1))}
        self.currentDirection = self.directions['R'] # Start facing right

        self.rotationMatrices = {'R': np.array([[0,1],[-1,0]]), 'L': np.array([[0,-1],[1,0]])}
        self.score = {(0,1):0, (1,0):1, (0,-1):2, (-1,0):3}
        self.sections = {1:((0,50),(49,99)), 2:((0,100),(49,149)), 3:((50,50),(99,99)), 4:((100,0),(149,49)), 5:((100,50),(149,99)), 6:((150,0),(199,49))}
        self.cubeMapping = {1:{'R':(2,'L'),'L':(4,'L'),'T':(6,'L'),'B':(3,'T')},
                            2:{'R':(5,'R'),'L':(1,'R'),'T':(6,'B'),'B':(3,'R')},
                            3:{'R':(2,'B'),'L':(4,'T'),'T':(1,'B'),'B':(5,'T')},
                            4:{'R':(5,'L'),'L':(1,'L'),'T':(3,'L'),'B':(6,'T')},
                            5:{'R':(2,'R'),'L':(4,'R'),'T':(3,'B'),'B':(6,'R')},
                            6:{'R':(5,'B'),'L':(1,'T'),'T':(4,'B'),'B':(2,'T')}}
        self.currentSection = 1
        self.position = None 
        if not self.isPart2:
            for i in range(len(self.grid[0])):
                if self.grid[0][i] == '.':
                    self.position = (0,i)
                    self.grid[0][i] = "*"
                    break
        else:
            self.position = self.sections[self.currentSection][0]
            
    
    def readInput(self):
        with open(self.txt) as f:
            allText = f.readlines()
            grid = []
            gridText = allText[:-2]
            maxLineLength = 0
            for line in gridText:
                toAdd = list(line.strip("\n"))
                grid.append(toAdd)
                maxLineLength = max(len(toAdd),maxLineLength)
            for line in grid:
                if len(line) < maxLineLength:
                    line.extend([' ']*(maxLineLength - len(line)))

            path = allText[-1].strip()
            path = re.findall("\d+|\D+",path)
            for i in range(len(path)):
                if i%2==0:
                    path[i] = int(path[i])
        return grid, path


    def followPath(self):
        for instruction in self.path:
            if type(instruction) == int:
                # We move forward until either we hit the number
                # or we hit a wall. If we reach the end of something, we check
                # if we can move back to the start of that space if there is no wall in the way
                # if the start of a space is not a wall, we can move there, otherwise stop before
                nextRow = self.position[0]
                nextColumn = self.position[1]
                for i in range(1,(instruction+1)):
                    nextRow = (nextRow + self.currentDirection[0]) % len(self.grid)
                    nextColumn = (nextColumn + self.currentDirection[1]) % len(self.grid[0])
                    while self.grid[nextRow][nextColumn] == ' ':
                        nextRow = (nextRow + self.currentDirection[0]) % len(self.grid)
                        nextColumn = (nextColumn + self.currentDirection[1]) % len(self.grid[1])
                    if self.grid[nextRow][nextColumn] == "#":
                        break
                    else:
                        self.grid[self.position[0]][self.position[1]] = '.'
                        self.position = (nextRow,nextColumn)
                        self.grid[self.position[0]][self.position[1]] = "*"

            else:
                self.currentDirection = np.matmul(self.rotationMatrices[instruction],np.transpose(self.currentDirection))
        return 1000*(self.position[0]+1) + 4*(self.position[1]+1) + self.score[(self.currentDirection[0],self.currentDirection[1])]

    def followPathPart2(self):
        for instruction in self.path:
            if type(instruction) == int:
                nextRow = self.position[0]
                nextColumn = self.position[1]
                for i in range(1,(instruction+1)):
                    nextRow = (nextRow + self.currentDirection[0]) % len(self.grid)
                    nextColumn = (nextColumn + self.currentDirection[1]) % len(self.grid[0])
                    possibleNextColumn = None
                    possibleNextRow = None
                    newSection = None
                    if nextRow < self.sections[self.currentSection][0][0]:
                        # Top edge
                        newSection, newEdge = self.cubeMapping[self.currentSection]['T']
                        #our new edge may be left or bottom
                        if newEdge == 'L':
                            #We need to map column of old section to row of new section
                            #Column = left edge of new section
                            possibleNextColumn = self.sections[newSection][0][1]
                            rowDif = nextColumn - self.sections[self.currentSection][0][1]
                            possibleNextRow = self.sections[newSection][0][0] + rowDif
                            self.currentDirection = self.directions['R']
                            
                        elif newEdge == 'B':
                            # Map column of old section to column of new section
                            possibleNextRow = self.sections[newSection][1][0] 
                            columnDif = nextColumn - self.sections[self.currentSection][0][1]
                            possibleNextColumn = self.sections[newSection][0][1] + columnDif
                            self.currentDirection = self.directions['T']

                    elif nextRow > self.sections[self.currentSection][1][0]:
                        # Bottom edge
                        newSection, newEdge = self.cubeMapping[self.currentSection]['B']
                        # new edge may be top or right
                        if newEdge == 'R':
                            #We need to map column of old section to row of new section
                            #Column = left edge of new section
                            possibleNextColumn = self.sections[newSection][1][1]
                            rowDif = nextColumn - self.sections[self.currentSection][0][1]
                            possibleNextRow = self.sections[newSection][0][0] + rowDif
                            self.currentDirection = self.directions['L']
                        elif newEdge == 'T':
                            # Map column of old section to column of new section
                            possibleNextRow = self.sections[newSection][0][0] 
                            columnDif = nextColumn - self.sections[self.currentSection][0][1]
                            possibleNextColumn = self.sections[newSection][0][1] + columnDif
                            self.currentDirection = self.directions['B']


                    elif nextColumn < self.sections[self.currentSection][0][1]:
                        # Left edge
                        newSection, newEdge = self.cubeMapping[self.currentSection]['L']
                        # new edge may be L, R or T
                        if newEdge == 'R':
                            possibleNextColumn = self.sections[newSection][1][1]
                            possibleNextRow = nextRow
                            self.currentDirection = self.directions['L']
                        elif newEdge == 'L':
                            possibleNextColumn = self.sections[newSection][0][1]
                            rowDif = nextRow - self.sections[self.currentSection][0][0]
                            possibleNextRow = self.sections[newSection][0][0] + rowDif
                            self.currentDirection = self.directions['R']
                        elif newEdge == 'T':
                            possibleNextRow = self.sections[newSection][0][0]
                            rowDif = nextRow - self.sections[self.currentSection][0][0]
                            possibleNextColumn = self.sections[newSection][0][1] + rowDif
                            self.currentDirection = self.directions['B']

                    elif nextColumn > self.sections[self.currentSection][1][1]:
                        # Right edge
                        newSection, newEdge = self.cubeMapping[self.currentSection]['R']
                        # new edge may be L, R or B
                        if newEdge == 'R':
                            possibleNextColumn = self.sections[newSection][1][1]
                            rowDif = nextRow - self.sections[self.currentSection][0][0]
                            possibleNextRow = self.sections[newSection][0][0] + rowDif
                            self.currentDirection = self.directions['L']
                        elif newEdge == 'L':
                            possibleNextColumn = self.sections[newSection][0][1]
                            possibleNextRow = nextRow
                            self.currentDirection = self.directions['R']
                        elif newEdge == 'B':
                            possibleNextRow = self.sections[newSection][1][0]
                            rowDif = nextRow - self.sections[self.currentSection][0][0]
                            possibleNextColumn = self.sections[newSection][0][1] + rowDif
                            self.currentDirection = self.directions['T']
                    if possibleNextRow != None:
                        nextRow = possibleNextRow
                        nextColumn = possibleNextColumn
                        self.currentSection = newSection

                    print(nextRow,nextColumn,self.currentSection,self.currentDirection)
                    if self.grid[nextRow][nextColumn] == '#':
                        break
                    else:
                        self.grid[self.position[0]][self.position[1]] = '.'
                        self.position = (nextRow,nextColumn)
                        self.grid[self.position[0]][self.position[1]] = "*"

            else:
                self.currentDirection = np.matmul(self.rotationMatrices[instruction],np.transpose(self.currentDirection))

        return 1000*(self.position[0]+1) + 4*(self.position[1]+1) + self.score[(self.currentDirection[0],self.currentDirection[1])]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: {} <input.txt>".format(sys.argv[0]))
        sys.exit(1)

    # grid = Grid(sys.argv[1],False)
    # print("Part 1: {}".format(grid.followPath()))

    grid = Grid(sys.argv[1],True)
    print("Part 2: {}".format(grid.followPathPart2()))

