import math
class Rope():
    def __init__(self,txt) -> None:
        self.txt = txt
        self.currentH = (0,0) #(x,y), with (0,0) in top left
        self.currentT = (0,0)
        self.mapping = {"R":(1,0),"L":(-1,0),"U":(0,-1),"D":(0,1)}

    def tenTailMoves(self):
        #Now we have to move through, keeping track of the positions of 1...9 where 9 is now Tail
        visited = 1
        allCurrentPos = [(0,0)]*10 # H,1,2...9
        visitedPosLastTail = set()
        visitedPosLastTail.add((0,0))
        with open(self.txt) as f:
            for line in f:
                line = line.strip('/n').split()
                for _ in range(int(line[1])):
                    dir = self.mapping[line[0]]
                    allCurrentPos[0] = (allCurrentPos[0][0] + dir[0],allCurrentPos[0][1] + dir[1])
                    for i in range(1,10):
                        cur = allCurrentPos[i]
                        prev = allCurrentPos[i-1] 
                        dx = prev[0] - cur[0]
                        dy = prev[1] - cur[1]
                        if max(abs(dx),abs(dy)) > 1:
                            curX = cur[0]
                            curX += dx//abs(dx) if dx else 0
                            curY = cur[1]
                            curY += dy//abs(dy) if dy else 0
                            cur = (curX,curY)

                        allCurrentPos[i] = cur

                        if i == 9:
                            if cur not in visitedPosLastTail:
                                visitedPosLastTail.add(cur)
                                visited += 1

        #             print(f'Current positions {allCurrentPos} with visited = {visited}')
        #         print(f'Final positions {allCurrentPos} with visited = {visited}')
        #         print("\n")
        # print(sorted(list(visitedPosLastTail),key=lambda x: x[0]))
        return visited


    def singleTailMoves(self):
        visited = 1
        visitedPositions = set()
        visitedPositions.add((0,0))
        with open(self.txt) as f:
            for line in f:
                line = line.strip('/n').split()
                for _ in range(int(line[1])):
                    dir = self.mapping[line[0]]
                    self.currentH = (self.currentH[0] + dir[0],self.currentH[1] + dir[1])
                    xDistanceBetween = abs(self.currentH[0] - self.currentT[0])
                    yDistanceBetween = abs(self.currentH[1] - self.currentT[1])
                    distanceBetween = xDistanceBetween + yDistanceBetween #Manhattan distance
                    #If not in the same row and column and distance > 2, move diagonally
                    if self.currentH[0] != self.currentT[0] and self.currentH[1] != self.currentT[1] and distanceBetween > 2:
                        print("Tail moving diagonally")
                        if xDistanceBetween > 1:
                            direction = self.currentH[0] - self.currentT[0]
                            if direction > 0:
                                direction = 1
                            else:
                                direction = -1
                            self.currentT = (self.currentT[0] + direction,self.currentH[1])
                        else:
                            direction = self.currentH[1] - self.currentT[1]
                            if direction > 0:
                                direction = 1
                            else:
                                direction = -1
                            self.currentT = (self.currentH[0],self.currentT[1] + direction)

                    #if same column but distance equals 2
                    elif self.currentH[0] == self.currentT[0] and distanceBetween == 2:
                        print("Tail moving up/down")
                        direction = self.currentH[1] - self.currentT[1]
                        if direction > 0:
                            direction = 1
                        else:
                            direction = -1
                        self.currentT = (self.currentT[0],self.currentT[1] + direction)
                    elif self.currentH[1] == self.currentT[1] and distanceBetween == 2:
                        print("Tail moving left/right")
                        direction = self.currentH[0] - self.currentT[0]
                        if direction > 0:
                            direction = 1
                        else:
                            direction = -1
                        self.currentT = (self.currentT[0] + direction,self.currentT[1])
                    else:
                        print("Tail not moving")
                    if self.currentT not in visitedPositions:
                        visitedPositions.add(self.currentT)
                        visited += 1
                        
                print(f'End of move {line}, currently head {self.currentH} and tail {self.currentT}. Visited a total of {visited} places \n')
        return visited



if __name__ == "__main__":
    txt = "input.txt"
    rope = Rope(txt)
    # print(rope.singleTailMoves())
    print(rope.tenTailMoves())