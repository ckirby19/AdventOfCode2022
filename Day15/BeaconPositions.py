import math

target = 2000000 + 910778

def readInput(txt):
    sensors = []
    sensorClosestDistance = dict()
    beacons = []
    maxX = 0
    minX = math.inf
    maxY = 0
    minY = math.inf
    with open(txt) as f:
        for line in f:
            line = line.strip().split()
            sensorX = int(line[2][2:].strip(","))
            sensorY = int(line[3][2:].strip(":"))
            beaconX = int(line[8][2:].strip(","))
            beaconY = int(line[9][2:])
            thisSensor = (sensorX,sensorY)
            thisBeacon = (beaconX,beaconY)
            distanceBetween = manhattanDis(thisSensor,thisBeacon)

            sensors.append(thisSensor)
            beacons.append(thisBeacon)
            #Set this to include distances of S to beacons
            maxX = max(maxX,max(sensorX + distanceBetween,beaconX))
            minX = min(minX,min(sensorX - distanceBetween,beaconX))
            #check if beacon is left or right of sensor
            maxY = max(maxY,max(sensorY + distanceBetween,beaconY))
            minY = min(minY,min(sensorY - distanceBetween,beaconY))

    print("MinY is:",minY)

    for i in range(len(sensors)):
        sensor = sensors[i]
        beacon = beacons[i]
        shiftedSensor = (sensor[0] - minX,sensor[1] - minY)
        shiftedBeacon = (beacon[0] - minX, beacon[1] - minY)
        sensors[i] = shiftedSensor
        beacons[i] = shiftedBeacon
        sensorClosestDistance[shiftedSensor] = manhattanDis(shiftedSensor,shiftedBeacon)

    i = target
    requiredMap = []
    sensors = set(sensors)
    beacons = set(beacons)
    for j in range(maxX - minX):
        if (j,i) in sensors:
            requiredMap.append('S')
        elif (j,i) in beacons:
            requiredMap.append('B')
        else:
            requiredMap.append('.')
    # print("created map",requiredMap)
    return requiredMap,sensors,sensorClosestDistance
    sbMap = []
    for i in range(maxY - minY):
        toAdd = []
        for j in range(maxX - minX):
            if (j,i) in sensors:
                toAdd.append('S')
            elif (j,i) in beacons:
                toAdd.append('B')
            else:
                toAdd.append('.')
        sbMap.append(toAdd)
    print("Created map")
    # for i,line in enumerate(sbMap):
    #     print(i, line)
    return sbMap,sensors,sensorClosestDistance

def manhattanDis(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def countBeaconNonSpots(sbMap,sensors,sensorClosestDistance):
    #For each row, go through each sensor and if the distance from that sensor is less than the distance to its corresponding beacon
    #Add a '#' there and add to count
    # rowTotals = [0]*len(sbMap)
    # for i in range(len(sbMap)):
    # i = 20
    # i = 2000000 + 910778
    totalInRow = 0

    for sensor in sensors:
        for i in range(sensorClosestDistance[sensor]):
            # print(i)
            posY1 = sensor[1] + i
            posY2 = sensor[1] - i
            width = (sensorClosestDistance[sensor] - i)
            print(width)
            # if posY1 == 2000000 + 910778:
            for j in range(-width,width+1):
                posX = sensor[0] + j
                # print(posX)
                if posY1 == target:
                    if sbMap[posX] == 'S':
                        totalInRow += 1
                    elif sbMap[posX] == '.':
                        totalInRow += 1
                        sbMap[posX] = '#'
                elif posY2 == target:
                    if sbMap[posX] == 'S':
                        totalInRow += 1
                    elif sbMap[posX] == '.':
                        totalInRow += 1
                        sbMap[posX] = '#'
    print("Final",sbMap)
    return totalInRow
                    
    for j in range(len(sbMap[0])):
        if sbMap[i][j] != 'B':
            if (j,i) in sensorsClosestDistance.keys():
                sbMap[i][j] = 'S'
                totalInRow += 1
            else:
                for k in range(len(sensors)):
                    sensor = sensors[k]
                    distanceToSensor = manhattanDis(sensor,(j,i))
                    if distanceToSensor <= sensorClosestDistance[sensor]:
                        sbMap[i][j] = '#'
                        totalInRow += 1
                        break
        # rowTotals[i] = totalInRow
    return totalInRow
    return rowTotals[2000000 + 910778]




if __name__ == '__main__':
    txt = "input.txt"
    sbMap,sensors,sensorsClosestDistance = readInput(txt)
    
    print(countBeaconNonSpots(sbMap,sensors,sensorsClosestDistance))
    # for i,line in enumerate(sbMap):
    #     print(line)