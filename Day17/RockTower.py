import time

class RockFall():
    def __init__(self,txt) -> None:
        self.txt = txt
        self.width = 7
        self.targetSteps = 2022
        self.disFromGround = 3
        self.bottomRow = 0
        self.landed = False
        self.rockOrder = ["Type0","Type1","Type2","Type3","Type4"]
        self.rockTypes = {"Type0": [[1,1,1,1]],
                          "Type1": [[0,1,0],[1,1,1],[0,1,0]],
                          "Type2": [[0,0,1],[0,0,1],[1,1,1]],
                          "Type3": [[1],[1],[1],[1]],
                          "Type4": [[1,1],[1,1]]}  
        self.jetPattern = self.inputToJet()
        print(self.jetPattern,len(self.jetPattern))
        self.chamber = []
        for _ in range(self.disFromGround+1):
            self.chamber.append([0]*self.width)
        
        self.chamber.append([1]*self.width)
            
        self.currentJet = 0
        self.currentRock = 0

    def inputToJet(self):
        with open(self.txt) as f:
            data = f.readlines()
            data = data[0].strip()
        return data

    def checkCollision(self,a,b,isSideways):
        if isSideways:
            #a and b will be column vectors in this case
            #For example a = [[0],[1],[0]], b = [[0],[0],[1]] then no collision
            for i in range(len(a)):
                if a[i][0] == 1 and b[i][0] == 1:
                    return True
        else:
            #a and b will be row vectors in this case 
            #For example [0,1,0] and [0,1,0] 
            for i in range(len(a)):
                if a[i] == 1 and b[i] == 1:
                    return True
            return False
    
    def jetPush(self,leftEdge,currentRock,currentJet,k):
        rightEdge = (leftEdge[0] + len(currentRock[0]) -1,k)
        wouldCollide = False
        # print(f"Jet in direction {self.jetPattern[self.currentJet]}")
        if currentJet == '>':
            #Then we need to check the right-most column
            jetDir = 1
            nextColumnIndex = rightEdge[0] + 1
            if nextColumnIndex < self.width:
                #Then we are within the walls, but need to check for rock collisions
                columnHeight = min(k,len(currentRock))
                nextColumn = []
                columnToCheck = []
                for h in range(columnHeight):
                    nextColumn.insert(0,[self.chamber[k-h][nextColumnIndex]])
                    columnToCheck.insert(0,[self.chamber[k-h][rightEdge[0]]])
                wouldCollide = self.checkCollision(nextColumn,columnToCheck,True)
            else:
                wouldCollide = True
        else:
            jetDir = -1
            nextColumnIndex = leftEdge[0] - 1
            if nextColumnIndex >= 0:
                columnHeight = min(k,len(currentRock))
                nextColumn = []
                columnToCheck = []
                for h in range(columnHeight):
                    nextColumn.insert(0,[self.chamber[k-h][nextColumnIndex]])
                    columnToCheck.insert(0,[self.chamber[k-h][leftEdge[0]]])
                wouldCollide = self.checkCollision(nextColumn,columnToCheck,True)
            else:
                wouldCollide = True
        if not wouldCollide:
            # print("Jet move is possible")
            #Then we move leftEdge AND shift our rock in direction as required
            #Remove old rock values
            # print("Left edge:",leftEdge,"Removing")
            for i in range(len(currentRock)):
                currentRow = k - i 
                if currentRow >= 0: 
                    for j in range(len(currentRock[0])):
                        self.chamber[currentRow][leftEdge[0]+ j] = max(currentRock[len(currentRock)-1-i][j] - self.chamber[currentRow][leftEdge[0]+ j], 0)
            #Update left edge
            leftEdge = (leftEdge[0] + jetDir,k)
            for i in range(len(currentRock)):
                #From rock bottom to top
                currentRow = k - i 
                if currentRow >= 0: 
                    for j in range(len(currentRock[0])):
                        self.chamber[currentRow][leftEdge[0]+j] += currentRock[len(currentRock)-1-i][j]
            # print(f"This is after the wind move")
        # else:
            # print("Could not move with wind")

            
        # for line in self.chamber:
        #         print(line)
        # print("\n")
        return leftEdge


    def timeStep(self,steps):
        k = 0
        leftEdge = (2,k)
        #First the rock appears in the first row
        currentRock = self.rockTypes[self.rockOrder[self.currentRock]]
        for i in range(leftEdge[0],leftEdge[0]+len(currentRock[0])):
            self.chamber[0][i] = currentRock[-1][i-leftEdge[0]]
        # print("START")
        # for line in self.chamber:
        #     print(line)
        # print("\n")
        while not self.landed:
            currentRock = self.rockTypes[self.rockOrder[self.currentRock]]
            currentJet = self.jetPattern[self.currentJet]
            #First we try jet push. If we can, this will also update chamber with new pos
            updatedEdge = self.jetPush(leftEdge,currentRock,currentJet,k)
            leftEdge = (updatedEdge[0],k)

            #Now we try moving down
            belowCheck = k+1
            belowRow = self.chamber[belowCheck][leftEdge[0]:leftEdge[0]+len(currentRock[0])]
            thisRow = self.chamber[k][leftEdge[0]:leftEdge[0]+len(currentRock[0])]

            wouldCollide = self.checkCollision(thisRow,belowRow,False)
            #special check for plus signs:
            # if self.currentRock == 1:
            #     currentRow = self.chamber[k-1][leftEdge[0]:leftEdge[0]+len(currentRock[0])]
            #     wouldCollide = wouldCollide and self.checkCollision(currentRow,thisRow,False)

            if wouldCollide:
                #Then the rock should land here
                self.landed = True
            else:
                #we move the rock down
                #First delete old positions
                for i in range(len(currentRock)):
                    currentRow = k - i 
                    if currentRow >= 0: 
                        for j in range(len(currentRock[0])):
                            self.chamber[currentRow][leftEdge[0]+ j] = max(self.chamber[currentRow][leftEdge[0]+ j] - currentRock[len(currentRock)-1-i][j],0)
                    
                k+=1
                for i in range(len(currentRock)):
                    currentRow = k - i 
                    if currentRow >= 0: 
                        for j in range(len(currentRock[0])):
                            self.chamber[currentRow][leftEdge[0]+ j] += currentRock[len(currentRock)-1-i][j]

            # print("We moved down")
            # for line in self.chamber:
            #     print(line)
            # print("\n")
            self.currentJet = (self.currentJet + 1)%(len(self.jetPattern))

        if steps == self.targetSteps-1:
            #Then we remove the top layers
            current = 0
            while 1 not in self.chamber[current]:
                current+=1
            self.chamber = self.chamber[current:]
        else:
            newRows = 4 - k + (len(self.rockTypes[self.rockOrder[self.currentRock]])-1)
            toAdd = []
            for k in range(newRows):
                toAdd.append([0]*self.width)
            self.chamber = toAdd + self.chamber
        
        self.currentRock = (self.currentRock + 1)%(len(self.rockTypes))
        self.landed = False
            

    def simulate(self):
        for steps in range(self.targetSteps):
            self.timeStep(steps)
        return len(self.chamber)-1


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: {} <input.txt>".format(sys.argv[0]))
        sys.exit(1)

    start = time.perf_counter()
    print("Started Part 1")
    rf = RockFall(sys.argv[1])
    simu = rf.simulate()
    print(simu)
    # for i in range(80):
    #     print(rf.chamber[i])
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 = {end - start:0.5f} seconds")      
