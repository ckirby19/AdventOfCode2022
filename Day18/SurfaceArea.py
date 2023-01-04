import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SACounter:
    def __init__(self,txt) -> None:
        self.txt = txt
        self.cubes = set()
        self.sides = lambda x,y,z: {(x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)}
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        self.minZ = 0
        self.maxZ = 0
        self.totalSA = 0
        self.inputParser()
        self.calculateTotalSA()

        self.externalSA = 0
        self.calculateExternalSA()
    
    def inputParser(self):

        with open(self.txt) as f:
            for line in f:
                allNums = line.strip().split(",")
                for i in range(len(allNums)):
                    allNums[i] = int(allNums[i])
                self.minX = min(self.minX,allNums[0])
                self.maxX = max(self.maxX,allNums[0])
                self.minY = min(self.minY,allNums[1])
                self.maxY = max(self.maxY,allNums[1])
                self.minZ = min(self.minZ,allNums[2])
                self.maxZ = max(self.maxZ,allNums[2])
                self.cubes.add(tuple(int(num) for num in line.strip().split(",")))
        print(f"Min max X {self.minX,self.maxX} Y {self.minY,self.maxY} Z {self.minZ,self.maxZ}")
        

    
    def plotSquares(self):
        #3D plot of the squares for visualisation
        fig = plt.figure()
        ax  = fig.add_subplot(111, projection = '3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        for cube in self.cubes:
            #(2,2,2) should have lines from (1,1,1) to (2,2,2) (excluding diagonals) so
            #edges = 12, 8 vertices
            #Plot each face, which corresponds to fixing X, then plotting all y and z clockwise,
            #Then fixing y and plotting all x and z clockwise
            for i in range(2):
                xEdge = [cube[0]-i]*5
                yEdge = [cube[1]]*2 + [cube[1]-1]*2 + [cube[1]]
                zEdge = [cube[2]] + [cube[2]-1]*2 + [cube[2]]*2
                ax.plot(xEdge,yEdge,zEdge,color="b")
            for i in range(2):
                xEdge = [cube[0]]*2 + [cube[0]-1]*2 + [cube[0]]
                yEdge = [cube[1]-i]*5
                zEdge = [cube[2]] + [cube[2]-1]*2 + [cube[2]]*2
                ax.plot(xEdge,yEdge,zEdge,color="b")

        plt.show()

        
    def calculateTotalSA(self):
        for cube in self.cubes:
            for s in self.sides(*cube):
                if s not in self.cubes:
                    self.totalSA += 1

    def calculateExternalSA(self):
        #Flood fill
        seen = set()
        stack = [(self.minX-1,self.minY-1,self.minZ-1)]
        xrange = range(self.minX-1,self.maxX+1)
        yrange = range(self.minY-1,self.maxX+1)
        zrange = range(self.minZ-1,self.maxZ+1)
        largestRange = max(self.maxX,max(self.maxY,self.maxZ))
        smallestRange = min(self.minX,min(self.minY,self.minZ))
        while stack:
            here = stack.pop()
            if here[0] not in xrange and here[1] not in yrange and here[2] not in zrange:
                continue

            stack += [s for s in (self.sides(*here) - self.cubes - seen) if all(smallestRange-1 <= c < largestRange+1 for c in s)]
            seen.add(here)

        self.externalSA = (sum((s in seen) for c in self.cubes for s in self.sides(*c)))


if __name__ == "__main__":
    txt = "input.txt"
    start = time.perf_counter()
    print("Started Part 1")
    saCounter = SACounter(txt)
    print(saCounter.totalSA) 
    print(saCounter.externalSA)
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 & 2 = {end - start:0.5f} seconds")    
    # saCounter.plotSquares()