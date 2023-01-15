import math
import re
import sys
# import z3

txt = "input.txt"
targetLine = 2000000

with open(txt) as f:
    observations = [
        tuple(map(int, re.findall(r"-?\d+", observation)))
            for observation in f.read().strip().split("\n")
    ]

    XRanges = []
    for sx, sy, bx, by in observations:
        d = abs(sx - bx) + abs(sy - by) - abs(sy - targetLine)
        if d >= 0:
            XRanges.append((sx - d, sx + d))
            
    relevantXVals = set()
    val = len(
    # At some point, remind me to re-write this using interval sets.
    set.union(
        *[set(range(a, b + 1)) for a, b in XRanges]
    )
    # Don't forget to exclude known beacon positions!
    - set(bx for *_, bx, by in observations if by == 2000000))
    # val = len(relevantXVals - set(bx for *_, bx, by in observations if by == targetLine))
    print("Part 1:", val)


# def readInput(txt,targetLine):
#     noBeaconSpots = set()
#     maxX = 0
#     minX = math.inf
#     maxY = 0
#     minY = math.inf
#     noBeaconCount = 0
#     with open(txt) as f:
#         for line in f:
#             line = line.strip().split()
#             sensorX = int(line[2][2:].strip(","))
#             sensorY = int(line[3][2:].strip(":"))
#             beaconX = int(line[8][2:].strip(","))
#             beaconY = int(line[9][2:])
#             #Other than beacon spot, we are looking at inequalities of x_s - dist < x < x_s + dist
#             # y_s - dist < y < y_s + dist
#             #  (x_s - x) + (y_s - y) <= dist
#             thisSensor = (sensorX,sensorY)
#             thisBeacon = (beaconX,beaconY)
#             distanceX = abs(sensorX - beaconX)
#             distanceY = abs(sensorY - beaconY)
#             distanceBetween = distanceX + distanceY
#             maxX = max(maxX,max(sensorX + distanceBetween,beaconX))
#             minX = min(minX,min(sensorX - distanceBetween,beaconX))
#             #check if beacon is left or right of sensor
#             maxY = max(maxY,max(sensorY + distanceBetween,beaconY))
#             minY = min(minY,min(sensorY - distanceBetween,beaconY))
            
#             if sensorY + distanceBetween < targetLine or sensorY - distanceBetween > targetLine:
#                 continue
#             else:
#                 for x in range(sensorX - distanceBetween,sensorX + distanceBetween):
#                     yRange = distanceBetween - abs(sensorX - x)
#                     for yShift in range(yRange+1):
#                         spot1 = (x,sensorY + yShift)
#                         spot2 = (x,sensorY - yShift)
#                         if (spot1[1] == targetLine and spot1 != thisBeacon):
#                             if spot1 not in noBeaconSpots:
#                                 print(thisSensor,thisBeacon,distanceBetween,x,yRange)
#                                 noBeaconCount += 1
#                                 noBeaconSpots.add(spot1)
                        
#                         if (spot2[1] == targetLine and spot2 != thisBeacon):
#                             if spot2 not in noBeaconSpots:
#                                 print(thisSensor,thisBeacon,distanceBetween,x,yRange)
#                                 noBeaconCount += 1
#                                 noBeaconSpots.add(spot2)

            

#     print(minX,minY,maxX,maxY)
    
#     # for x in range(int(minX),int(maxX)):
#     #     if (x,targetLine) in noBeaconSpots:
#     #         noBeaconCount += 1
#     return noBeaconCount


# if __name__ == '__main__':
#     txt = "input2.txt"
#     target1 = 10
#     target2 = 2000000
#     print(readInput(txt,target2))