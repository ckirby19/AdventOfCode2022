import re
import numpy as np
import time
DEBUG = False
class Grid():
    def __init__(self,txt,isPart2) -> None:
        self.txt = txt
        self.isPart2 = isPart2
        # All coordinates are in the form (row,column)
        self.grid,self.path = self.readInput()
        self.directions = {'R':np.array((0,1)), 'L':np.array((0,-1)), 'T':np.array((-1,0)), 'B':np.array((1,0))}
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
        print(self.position[0]+1,self.position[1]+1,(self.currentDirection[0],self.currentDirection[1]))
        return 1000*(self.position[0]+1) + 4*(self.position[1]+1) + self.score[(self.currentDirection[0],self.currentDirection[1])]

    def followPathPart2(self):
        for instruction in self.path:
            if type(instruction) == int:
                nextRow = self.position[0]
                nextColumn = self.position[1]
                for _ in range(1,(instruction+1)):
                    nextRow = (nextRow + self.currentDirection[0])
                    nextColumn = (nextColumn + self.currentDirection[1])
                    possibleNextColumn = None
                    possibleNextRow = None
                    newDirection = self.currentDirection
                    newSection = self.currentSection
                    if nextRow < self.sections[self.currentSection][0][0]:
                        # Top edge
                        newSection, newEdge = self.cubeMapping[self.currentSection]['T']
                        #our new edge may be left or bottom
                        if newEdge == 'L':
                            possibleNextColumn = self.sections[newSection][0][1]
                            rowDif = nextColumn - self.sections[self.currentSection][0][1]
                            possibleNextRow = self.sections[newSection][0][0] + rowDif
                            newDirection = self.directions['R']
                            
                        elif newEdge == 'B':
                            possibleNextRow = self.sections[newSection][1][0] 
                            columnDif = nextColumn - self.sections[self.currentSection][0][1]
                            possibleNextColumn = self.sections[newSection][0][1] + columnDif
                            newDirection = self.directions['T']

                    elif nextRow > self.sections[self.currentSection][1][0]:
                        # Bottom edge
                        newSection, newEdge = self.cubeMapping[self.currentSection]['B']
                        # new edge may be top or right
                        if newEdge == 'R':
                            possibleNextColumn = self.sections[newSection][1][1]
                            rowDif = nextColumn - self.sections[self.currentSection][0][1]
                            possibleNextRow = self.sections[newSection][0][0] + rowDif
                            newDirection = self.directions['L']
                        elif newEdge == 'T':
                            possibleNextRow = self.sections[newSection][0][0] 
                            columnDif = nextColumn - self.sections[self.currentSection][0][1]
                            possibleNextColumn = self.sections[newSection][0][1] + columnDif
                            newDirection = self.directions['B']


                    elif nextColumn < self.sections[self.currentSection][0][1]:
                        # Left edge
                        newSection, newEdge = self.cubeMapping[self.currentSection]['L']
                        # new edge may be L, R or T
                        if newEdge == 'R':
                            possibleNextColumn = self.sections[newSection][1][1]
                            possibleNextRow = nextRow
                            newDirection = self.directions['L']
                        elif newEdge == 'L':
                            #If left edge to left edge, we have to flip our reference edge
                            possibleNextColumn = self.sections[newSection][0][1]
                            rowDif = nextRow - self.sections[self.currentSection][0][0]
                            possibleNextRow = self.sections[newSection][1][0] - rowDif
                            newDirection = self.directions['R']
                        elif newEdge == 'T':
                            possibleNextRow = self.sections[newSection][0][0]
                            rowDif = nextRow - self.sections[self.currentSection][0][0]
                            possibleNextColumn = self.sections[newSection][0][1] + rowDif
                            newDirection = self.directions['B']

                    elif nextColumn > self.sections[self.currentSection][1][1]:
                        # Right edge
                        newSection, newEdge = self.cubeMapping[self.currentSection]['R']
                        # new edge may be L, R or B
                        if newEdge == 'R':
                            possibleNextColumn = self.sections[newSection][1][1]
                            rowDif = nextRow - self.sections[self.currentSection][0][0]
                            possibleNextRow = self.sections[newSection][1][0] - rowDif
                            newDirection = self.directions['L']
                        elif newEdge == 'L':
                            possibleNextColumn = self.sections[newSection][0][1]
                            possibleNextRow = nextRow
                            newDirection = self.directions['R']
                        elif newEdge == 'B':
                            possibleNextRow = self.sections[newSection][1][0]
                            rowDif = nextRow - self.sections[self.currentSection][0][0]
                            possibleNextColumn = self.sections[newSection][0][1] + rowDif
                            newDirection = self.directions['T']
                    if possibleNextRow != None:
                        nextRow = possibleNextRow
                        nextColumn = possibleNextColumn

                    
                    if self.grid[nextRow][nextColumn] == '#':
                        if DEBUG:
                            print("COLLISION",nextRow,nextColumn)
                        break
                    else:
                        self.grid[self.position[0]][self.position[1]] = '.'
                        self.position = (nextRow,nextColumn)
                        self.grid[self.position[0]][self.position[1]] = "*"
                        self.currentSection = newSection
                        self.currentDirection = newDirection
                        if DEBUG:
                            print(nextRow,nextColumn,self.currentSection,self.currentDirection)

            else:
                self.currentDirection = np.matmul(self.rotationMatrices[instruction],np.transpose(self.currentDirection))

        print(self.position[0]+1,self.position[1]+1,(self.currentDirection[0],self.currentDirection[1]))
        return 1000*(self.position[0]+1) + 4*(self.position[1]+1) + self.score[(self.currentDirection[0],self.currentDirection[1])]


if __name__ == "__main__":
    txt = "input.txt"

    start = time.perf_counter()
    print("Started Part 1")
    grid = Grid(txt,False)
    print("Part 1: {}".format(grid.followPath()))
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 = {end - start:0.5f} seconds")
    print("\n")
    start = time.perf_counter()
    print("Started Part 2")
    grid = Grid(txt,True)
    print("Part 2: {}".format(grid.followPathPart2()))
    end = time.perf_counter()
    print(f"Time taken to complete Part 2 = {end - start:0.5f} seconds")

