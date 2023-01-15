# import math
# import re


# txt = "input.txt"
# targetLine = 2000000
# # targetLine = 10

# with open(txt) as f:
#     sensorAndbeacons = []
#     for line in f:
#         sensorAndbeacons.append(tuple(map(int,re.findall(r"-?\d+",line))))
    
# # For part 1 we care only about what crosses our target line
# left = 0
# right = 0
# beacons = set()
# sensors = []
# for sX,sY,bX,bY in sensorAndbeacons:
#     beacons.add((bX,bY))
#     distance = abs(sX - bX) + abs(sY - bY)
#     left = min(sX - distance,left)
#     right = max(sX + distance,right)
#     if (sY <= targetLine and sY + distance >= targetLine) or (sY >= targetLine and sY - distance <= targetLine):
#         sensors.append((sX,sY,distance))

# count = 0
# # print(left,right)
# for x in range(left,right+1):
#     if (x,targetLine) in beacons:
#         continue
#     # for sensor in sensors:
#     #     disFromX = abs(x - sensor[0]) + abs(targetLine - sensor[1])
#     #     if disFromX <= sensor[2]:
#     #         count += 1
#     #         break

    
# print(count)

import re

ints = lambda s: map(int, re.findall(r'-?\d+', s))
dist = lambda x,y,p,q: abs(x-p) + abs(y-q)
data = [(x, y, dist(x,y,p,q)) for x,y,p,q in map(ints, open('test.txt'))]

A = 10
minV = 0
maxV = 0
for x,y,d in data:
    val1 = x - abs(A-y) + d
    val2 = x + abs(A-y) - d
    minV = min(val1,minV)
    maxV = max(val2,maxV)
    print(x,y,d,val1,val2)
# print(max(x - abs(A-y) + d for x,y,d in data),min(x + abs(A-y) - d for x,y,d in data))
# print(max(x - abs(A-y) + d for x,y,d in data) - min(x + abs(A-y) - d for x,y,d in data))
print(maxV - minV)

f = lambda x,y,d,p,q,r: ((p+q+r+x-y-d)//2, (p+q+r-x+y+d)//2+1)

# B = 4000000
# for X, Y in [f(*a,*b) for a in data for b in data]:
#     if 0<X<B and 0<Y<B and all(dist(X,Y,x,y)>d for x,y,d in data):
#         print(B*X + Y)