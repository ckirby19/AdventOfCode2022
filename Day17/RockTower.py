import time
import math

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
                          "Type1": [[0,2,0],[2,2,2],[0,2,0]],
                          "Type2": [[0,0,3],[0,0,3],[3,3,3]],
                          "Type3": [[4],[4],[4],[4]],
                          "Type4": [[5,5],[5,5]]}  
        self.jetPattern = self.inputToJet()
        self.chamber = []
        self.gridUniqueKey = dict()
        self.maxColumnHeights = [0]*self.width
        self.maxHeight = 0
        for _ in range(self.disFromGround+1):
            self.chamber.append([0]*self.width)
        
        self.chamber.append([1]*self.width) #To mark the ground
            
        self.currentJetIndex = 0
        self.currentRockIndex = 0

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
                if a[i][0] > 0 and b[i][0] > 0:
                    return True
        else:
            #a and b will be row vectors in this case 
            #For example [0,1,0] and [0,1,0] 
            for i in range(len(a)):
                if a[i] > 0 and b[i] > 0:
                    return True
        return False
    
    def jetPush(self,leftEdge,currentRock,currentJet,k):
        rightEdge = (leftEdge[0] + len(currentRock[0]) -1,k)
        wouldCollide = False
        if currentJet == '>':
            jetDir = 1
            nextColumnIndex = rightEdge[0] + 1
            if nextColumnIndex < self.width:
                columnHeight = min(k,len(currentRock)-1)
                nextColumn = []
                columnToCheck = []
                for h in range(columnHeight+1):
                    nextColumn.insert(0,[self.chamber[k-h][nextColumnIndex]])
                    columnToCheck.insert(0,[self.chamber[k-h][rightEdge[0]]])
                wouldCollide = self.checkCollision(nextColumn,columnToCheck,True)

                if self.currentRockIndex == 1 and len(columnToCheck) != 2:
                    if columnToCheck[0][0] > 0 or columnToCheck[-1][0] > 0:
                        wouldCollide = True 
            else:
                wouldCollide = True
        else:
            jetDir = -1
            nextColumnIndex = leftEdge[0] - 1
            if nextColumnIndex >= 0:
                columnHeight = min(k,len(currentRock)-1)
                nextColumn = []
                columnToCheck = []
                for h in range(columnHeight+1):
                    nextColumn.insert(0,[self.chamber[k-h][nextColumnIndex]])
                    columnToCheck.insert(0,[self.chamber[k-h][leftEdge[0]]])
                wouldCollide = self.checkCollision(nextColumn,columnToCheck,True)

                if self.currentRockIndex == 1 and len(columnToCheck) != 2:
                    if columnToCheck[0][0] > 0 or columnToCheck[-1][0] > 0:
                        wouldCollide = True 

            else:
                wouldCollide = True
        if not wouldCollide:
            #Then we move leftEdge AND shift our rock in direction as required
            #Remove old rock values
            columnHeight = len(currentRock)
            for i in range(columnHeight):
                currentRow = k - i 
                if currentRow >= 0: 
                    for j in range(len(currentRock[0])):
                        self.chamber[currentRow][leftEdge[0] + j] -= currentRock[len(currentRock)-1-i][j]
            #Update left edge
            leftEdge = (leftEdge[0] + jetDir,k)
            for i in range(columnHeight):
                #From rock bottom to top
                currentRow = k - i 
                if currentRow >= 0: 
                    for j in range(len(currentRock[0])):
                        self.chamber[currentRow][leftEdge[0]+j] += currentRock[len(currentRock)-1-i][j]

        return leftEdge



    def timeStep(self,steps,checkCycles):
        k = 0
        leftEdge = (2,k)
        #First the rock appears in the first row
        currentRock = self.rockTypes[self.rockOrder[self.currentRockIndex]]
        for i in range(leftEdge[0],leftEdge[0]+len(currentRock[0])):
            self.chamber[0][i] = currentRock[-1][i-leftEdge[0]]

        while not self.landed:
            currentRock = self.rockTypes[self.rockOrder[self.currentRockIndex]]
            currentJet = self.jetPattern[self.currentJetIndex]
            #First we try jet push. If we can, this will also update chamber with new pos
            leftEdge = self.jetPush(leftEdge,currentRock,currentJet,k)

            #Now we try moving down
            belowCheck = k+1
            belowRow = self.chamber[belowCheck][leftEdge[0]:leftEdge[0]+len(currentRock[0])]
            thisRow = self.chamber[k][leftEdge[0]:leftEdge[0]+len(currentRock[0])]

            wouldCollide = self.checkCollision(thisRow,belowRow,False)
            #special check for plus signs:
            if self.currentRockIndex == 1:
                bottomRowLeft = self.chamber[k][leftEdge[0]]
                bottomRowRight = self.chamber[k][leftEdge[0] + len(currentRock[0])-1]
                if bottomRowLeft > 0 or bottomRowRight > 0:
                    wouldCollide = True

            if wouldCollide:
                #Then the rock should land here
                self.landed = True
            else:
                #we move the rock down
                #First delete old positions
                columnHeight = len(currentRock)
                for i in range(columnHeight):
                    middleRow = k - i 
                    if middleRow >= 0: 
                        for j in range(len(currentRock[0])):
                            self.chamber[middleRow][leftEdge[0]+ j] -= currentRock[len(currentRock)-1-i][j]
                    
                k+=1
                for i in range(columnHeight):
                    middleRow = k - i 
                    if middleRow >= 0: 
                        for j in range(len(currentRock[0])):
                            self.chamber[middleRow][leftEdge[0]+ j] += currentRock[len(currentRock)-1-i][j]

            self.currentJetIndex = (self.currentJetIndex + 1)%(len(self.jetPattern))

        #Now we have landed, we add the current grid to our cycle dict
        cycle = None
        if checkCycles:
            rowTop = max(0,k+1 - len(currentRock))
            for rowIncrement in range(rowTop, k+1):
                for column in range(leftEdge[0], leftEdge[0] + len(currentRock[0])):
                    if currentRock[max(0,rowIncrement-rowTop)][column - leftEdge[0]] > 0:
                        self.maxColumnHeights[column] = max(self.maxColumnHeights[column], len(self.chamber) - rowIncrement - 1)
                        if self.maxColumnHeights[column] > self.maxHeight:
                            self.maxHeight = self.maxColumnHeights[column]

            heightDif = [0]*len(self.chamber[0])
            for i in range(len(self.maxColumnHeights)):
                heightDif[i] = self.maxHeight - self.maxColumnHeights[i]
            nxtKey = ((*heightDif,self.currentJetIndex,self.currentRockIndex))
            if nxtKey in self.gridUniqueKey.keys():
                #We have a cycle 
                cycle = (self.gridUniqueKey[nxtKey],steps)
                print("CYCLE",nxtKey,self.gridUniqueKey[nxtKey],steps)
            else:
                self.gridUniqueKey[nxtKey] = steps
        if steps == self.targetSteps-1 or cycle:
            #Then we remove the top layers
            current = 0
            while 1:
                if not any(num >= 1 for num in self.chamber[current]):
                    current += 1
                else:
                    break
            self.chamber = self.chamber[current:]
        else:
            newRows = 4 - k + (len(self.rockTypes[self.rockOrder[self.currentRockIndex]])-1)
            toAdd = []
            for k in range(newRows):
                toAdd.append([0]*self.width)
            self.chamber = toAdd + self.chamber
        
        self.currentRockIndex = (self.currentRockIndex + 1)%(len(self.rockTypes))
        self.landed = False
        return cycle

    def simulate(self):
        cycle = None
        steps = 0
        x = 1
        # for steps in range(self.targetSteps):
        while not cycle and steps != self.targetSteps:
            cycle = self.timeStep(steps,True)
            steps += 1
            #We repeat this cycle x times s.t steps * x <= self.targetsteps
            if cycle:
                # Then our repeated part is between cycle[0] and cycle[1] steps
                cycleSection = cycle[1] - cycle[0]
                x = math.floor((self.targetSteps - cycle[0])/cycleSection)

        if cycle:
            self.chamber = self.chamber[:cycle[0]] + self.chamber[cycle[0]:cycle[1]]
            steps = cycle[0] + (cycleSection * x)
            for i in range(steps,self.targetSteps):
                self.timeStep(i,False)    
            return len(self.chamber)-1 + cycleSection*x
        else:
            return len(self.chamber)-1


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: {} <input.txt>".format(sys.argv[0]))
        sys.exit(1)

    start = time.perf_counter()
    print("Started traversal")
    rf = RockFall(sys.argv[1])
    simu = rf.simulate()
    print(simu)
    end = time.perf_counter()
    print(f"Time taken to complete Part 1 = {end - start:0.5f} seconds")      
