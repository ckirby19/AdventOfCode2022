import math
import re
from z3 import *
# target = 2000000 + 910778
class BeaconPos():
    def __init__(self,txt,target) -> None:
        self.txt = txt
        self.originalTarget = target
        self.target = target
        self.data = []
        self.sensors = []
        self.beacons = []
        self.sbMap = []
        self.sensorDistanceToBeacon = dict()
        self.maxX = 0
        self.minX = math.inf
        self.maxY = 0
        self.minY = math.inf
        self.readInput()

    def manhattanDis(self,a,b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def readInput(self):
        with open(self.txt) as f:
            for line in f:
                sX,sY,bX,bY = tuple(map(int,re.findall(r"-?\d+",line)))
                self.data.append((sX,sY,bX,bY))
                thisSensor = (sX,sY)
                thisBeacon = (bX,bY)
                distanceBetween = self.manhattanDis(thisSensor,thisBeacon)

                self.sensors.append(thisSensor)
                self.beacons.append(thisBeacon)

                self.maxX = max(self.maxX,max(sX + distanceBetween,bX))
                self.minX = min(self.minX,min(sX - distanceBetween,bX))
                self.maxY = max(self.maxY,max(sY + distanceBetween,bY))
                self.minY = min(self.minY,min(sY - distanceBetween,bY))

        for i in range(len(self.sensors)):
            sensor = self.sensors[i]
            beacon = self.beacons[i]
            shiftedSensor = (sensor[0] - self.minX,sensor[1] - self.minY)
            shiftedBeacon = (beacon[0] - self.minX, beacon[1] - self.minY)
            self.sensors[i] = shiftedSensor
            self.beacons[i] = shiftedBeacon
            self.sensorDistanceToBeacon[shiftedSensor] = self.manhattanDis(shiftedSensor,shiftedBeacon)

        self.target -= self.minY
        self.sensors = set(self.sensors)
        self.beacons = set(self.beacons)
        for i in range(self.maxX - self.minX):
            if (i,target) in self.sensors:
                self.sbMap.append('S')
            elif (i,target) in self.beacons:
                self.sbMap.append('B')
            else:
                self.sbMap.append('.')

    def countBeaconNonSpots(self):
        #For each sensor, if the distance from that sensor is less than the distance to its corresponding beacon
        #Add a '#' there and add to count
        totalInRow = 0
        for i in range(len(self.sbMap)):
            if self.sbMap[i] == "B":
                continue
            elif self.sbMap[i] == "S":
                totalInRow += 1
            else:
                for sensor in self.sensors:
                    if self.manhattanDis((i,target),sensor) <= self.sensorDistanceToBeacon[sensor]:
                        totalInRow += 1
                        self.sbMap[i] = '#'
                        break
        return totalInRow

    def getDistressBeacon(self):
        val = self.originalTarget*2
        s = z3.Solver()
        x, y = z3.Int("x"), z3.Int("y")

        s.add(0 <= x) 
        s.add(x <= val)
        s.add(0 <= y)
        s.add(y <= val)

        z3_abs = lambda x: z3.If(x>=0,x,-x)

        for sx, sy, bx, by in self.data:
            m = abs(sx - bx) + abs(sy - by)
            s.add(z3_abs(sx - x) + z3_abs(sy - y) > m)
        assert s.check() == z3.sat
        model = s.model()
        return model[x].as_long() * val + model[y].as_long()

if __name__ == '__main__':
    txt = "input.txt"
    target = 2000000
    bp = BeaconPos(txt,target)
    print("Running Part 1")
    print("Part 1: ",bp.countBeaconNonSpots())
    print("Running Part 2")
    print("Part 2: ",bp.getDistressBeacon())