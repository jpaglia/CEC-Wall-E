import request
import copy
import math

def main():
    instanceData = request.createinstance()
    if (instanceData !='ERROR'):
        instanceData = instanceData['payload']
        roomMatrix, spaceMatrix = createRoom(instanceData)
        location = instanceData['location']
        locX = location['x']
        locY = location['y']

        setNew(spaceMatrix)


def createRoom(instanceData):
    #room logic
    ROOM_DIMENSIONS = instanceData['constants']['ROOM_DIMENSIONS']
    xMin = ROOM_DIMENSIONS['X_MIN']
    xMax = ROOM_DIMENSIONS['X_MAX']
    yMin = ROOM_DIMENSIONS['Y_MIN']
    yMax = ROOM_DIMENSIONS['Y_MAX']

    # Bin logic
    bins = instanceData['constants']['BIN_LOCATION']
    organicBin = bins['ORGANIC']
    organicX = organicBin['X']
    organicY = organicBin['Y']
    recycleBin = bins['RECYCLE']
    recycleX = recycleBin['X']
    recycleY = recycleBin['Y']
    garbageBin = bins['GARBAGE']
    garbageX = garbageBin['X']
    garbageY = garbageBin['Y']

    location = instanceData['location']
    locX = location['x']
    locY = location['y']

    iterateX = xMin
    roomMatrix = []
    spaceMatrix = []
    while (iterateX <= xMax):
        row = []
        row2 = []
        iterateY = yMin
        while(iterateY <= yMax):
            if (iterateX == organicX and iterateY == organicY):
                row.append('C')
            elif (iterateX == recycleX and iterateY == recycleY):
                row.append('R')
            elif (iterateX == garbageX and iterateY == garbageY):
                row.append('G')
            else:
                row.append(0)
            row2.append(0)
            iterateY += 1
        roomMatrix.append(row)
        spaceMatrix.append(row2)
        iterateX += 1
# xMin = str(instanceData['ROOM_DIMENSIONS'])
    return roomMatrix, spaceMatrix

def printRoom(roomMatrix):
    for row in roomMatrix:
        print(row)

def roomScanned(instanceData, roomMatrix):
    scanData = instanceData['itemsLocated']
    tempArray = copy.deepcopy(roomMatrix)
    for elem in scanData:
        print(elem)
        x = elem['x']
        y = elem['y']
        id = elem['id']
        type = elem['type']
        if (tempArray[y][x] != 0):
            tempArray[y][x].append(type)
        else:
            tempArray[y][x] = [type]

    return tempArray

def goTo(row, col):
    currentInstance = request.getinstance()
    currentInstance = currentInstance.json()['payload']
    print(currentInstance)

def setNew(spaceMatrix):
    #go to ideal
    instance = request.getinstance()
    currentInstance = instance.json()['payload']
    ROOM_DIMENSIONS = currentInstance['constants']['ROOM_DIMENSIONS']
    xMin = ROOM_DIMENSIONS['X_MIN']
    # xMax = ROOM_DIMENSIONS['X_MAX']
    yMin = ROOM_DIMENSIONS['Y_MIN']
    # yMax = ROOM_DIMENSIONS['Y_MAX']
    # location = currentInstance['location']
    # locX = location['x']
    # locY = location['y']
    scanRadius = currentInstance['constants']['SCAN_RADIUS']
    spaceMatrix = request.spiralOrder(spaceMatrix, scanRadius, xMin, yMin)
    printRoom(spaceMatrix)


if __name__ == '__main__':
    main()
