class TreeHouseLocationFinder():
    def __init__(self,txtFile) -> None:
        self.visibleTreeCount = 0
        self.matrix = self.convertDataToMatrix(txtFile)
        #0 = not visible, 1 = visible
        self.visibility = []
        for i in range(len(self.matrix)):
            if i == 0 or i == len(self.matrix)-1:
                self.visibility.append([1]*len(self.matrix[0]))
                self.visibleTreeCount += len(self.matrix[0])
            else:
                toAppend = [1] + [0]*(len(self.matrix[0])-2) + [1]
                self.visibility.append(toAppend)
                self.visibleTreeCount += 2


    def convertDataToMatrix(self,txtFile):
        output = []
        with open(txtFile) as f:
            for line in f:
                cur = []
                row = line.split()[0]
                for char in row:
                    cur.append(int(char))
                output.append(cur)
        return output

    def countVisibleTrees(self):
        #First we go top -> bottom, left -> right
        largestInColumn = self.matrix[0]
        largestInRow = [0]*len(self.matrix)
        
        for i,row in enumerate(self.matrix):
            largestInRow[i] = row[0]

        self.visibilityLoop(largestInRow,largestInColumn,False)

        largestInColumn = self.matrix[-1]
        largestInRow = [0]*len(self.matrix)

        for i,row in enumerate(self.matrix):
            largestInRow[i] = row[-1]
        # print("start of second pass",largestInRow,largestInColumn)
        self.visibilityLoop(largestInRow,largestInColumn,True)

        # print("Final vis loop is:")
        # for row in self.visibility:
        #     print(row)


    
    def visibilityLoop(self,largestInRow,largestInColumn,backwards):
        if backwards:
            iRange = range(len(self.matrix)-2,0,-1)
            jRange = range(len(self.matrix[0])-2,0,-1)
        else:
            iRange = range(1,len(self.matrix)-1)
            jRange = range(1,len(self.matrix[0])-1)
        for i in iRange:
            for j in jRange:
                current = self.matrix[i][j]
                if current > largestInRow[i]:
                    if self.visibility[i][j] == 0:
                        self.visibility[i][j] = 1
                        self.visibleTreeCount += 1
                    largestInRow[i] = current
                if current > largestInColumn[j]:
                    if self.visibility[i][j] == 0:
                        self.visibility[i][j] = 1
                        self.visibleTreeCount += 1
                    largestInColumn[j] = current
     
    def highestScenicScore(self):
        highest = 0
        dirs = [[1,0],[-1,0],[0,1],[0,-1]]
        print("Starting matrix for scenic score is:")
        for line in self.matrix:
            print(line)
        print("\n")
        for i in range(1,len(self.matrix)-1):
            for j in range(1,len(self.matrix[0])-1):
                #i = row, j = column. next = (i)
                current = self.matrix[i][j]
                score = 1
                distance = 1
                for dir in dirs:
                    notBlocked = True
                    nextPos = (i + dir[0]*distance, j + dir[1]*distance) #(row,column)
                    while notBlocked:
                        nextPosVal = self.matrix[nextPos[0]][nextPos[1]]
                        if nextPosVal >= current:
                            notBlocked = False
                            print(f'{nextPos} with value {nextPosVal} is bigger than or equal to {(i,j)} in direction {dir} with distance {distance}')
                        else:
                            #We can see beyond the current tree so we are either at the end or check next tree
                            distance += 1
                            nextPos = (i + dir[0]*distance, j + dir[1]*distance)
                            if (nextPos[0] < 0 or nextPos[1] < 0):
                                distance -= 1
                                break
                            if (nextPos[0] >= len(self.matrix) or nextPos[1] >= len(self.matrix[0])):
                                distance -= 1
                                break

                    if notBlocked:
                        print(f'Current {(i,j)} is tallest tree in direction {dir} with distance of {distance}')
                    score *=  distance
                    distance = 1

                highest = max(score,highest)
                print(f'Highest score for {(i,j)} is {score}')
                print("\n")

        print(f'Highest score is {highest}')
        return highest

if __name__ == "__main__":
    txt = "input.txt"
    THLF = TreeHouseLocationFinder(txt)
    # THLF.countVisibleTrees() #This one is modifying the self.matrix somehow!!
    # print(THLF.visibleTreeCount)
    print("\n")
    print(THLF.highestScenicScore())
                

