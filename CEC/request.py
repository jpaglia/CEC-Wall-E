import requests
import json
import math

headers = {
    'token': 'dedinsky-Tcwr6DhhoEgvifh8NpYwaBKa5fkartbiVkvVU82LR9YvPPkLYunGfHaues6xPtwZ'
}

# url = 'http://cec2019.ca'
url = ''
# 0 for error found, 1 for error not found
def checkerror(result):
    result_j = result.json()
    type_info = str(result_j['type'])
    print("type: <" + type_info + ">")
    if (type_info != "SUCCESS"):
        print("Command failed. Data: \n=============\n" + result.text + "\n=============")
        return 0
    else:
        return 1

# CREATE INSTANCE
def createinstance():
    if (checkerror(getinstance()) == 1):
        deleteinstance()

    r = requests.post('http://localhost:8081/instance', headers=headers)
    if (checkerror(r) == 1):
        result = r.json()
        return result
    return 'ERROR'

# DELETE INSTANCE
def deleteinstance():
    r = requests.delete('http://localhost:8081/instance', headers=headers)
    checkerror(r)
    return r

def getinstance():
    r = requests.get('http://localhost:8081/instance', headers=headers)
    return r

# FINISH
def finish():
    r = requests.post('http://localhost:8081/finish', headers=headers)
    return r

# MOVE THE ROBOT IN A GIVEN DIRECTION
# move(direction of movement, number of times to move)
def move(direction, amount):
    r = getinstance()
    rjson = r.json()
    facing = str(rjson['payload']['direction'])

    print("facing: {} direction: {}".format(facing, direction))
    if (facing != direction):
        facing = direction
        url = 'http://localhost:8081/turn/' + str(direction)
        r = requests.post(url, headers=headers)
        checkerror(r)
        # facing_new = getinstance().json()['payload']['direction']
        # print("Now facing: " + str(facing_new))

    # now facing correct direction
    for i in range(amount):
        r = requests.post('http://localhost:8081/move', headers=headers)
        print("moving for the " + str(i) + "th time in direction " + facing)
        # inst = getinstance().json()
        # print("Where we are: " + str(inst['payload']['location']))
        if (checkerror(r) == 0):
            break

# SCAN
# scan(instance)
def scan():
    r = requests.post('http://localhost:8081/scanArea', headers=headers)
    rj = r.json()
    return rj

# COLLECT ITEM
# collect(item id)
def collect(id):
    r = requests.post('http://localhost:8081/collectItem/' + str(id), headers=headers)
    rj = r.json()
    return rj

# UNLOAD
# unload(item id)
def unload(id):
    r = requests.post('http://localhost:8081/unloadItem/' + str(id), headers=headers)
    rj = r.json()
    return rj

def goto(row, column):
    r = getinstance()
    posx = int(r.json()['payload']['location']['x'])
    posy = int(r.json()['payload']['location']['y'])
    t_posx = int(column)
    t_posy = int(row)

    # === MOVE X ===
    if (t_posx < posx):
        move('W', posx - t_posx)
    elif(t_posx > posx):
        move('E', t_posx - posx)
    else:
        print("target pos: " + str(t_posx) + ", pos: " + str(posx))

    # === MOVE Y ===
    if (t_posy < posy):
        move('S', posy - t_posy)
    elif(t_posy > posy):
        move('N', t_posy - posy)
    else:
        print("target pos: " + str(t_posy) + ", pos: " + str(posy))

def goToNearestCorner():
    radius = getinstance().json()['payload']['constants']['SCAN_RADIUS']
    currentLoc = getinstance().json()['payload']['location']
    xPos = currentLoc['x']
    yPos = currentLoc['y']
    ROOM_DIMENSIONS = getinstance().json()['payload']['constants']['ROOM_DIMENSIONS']
    xMin = ROOM_DIMENSIONS['X_MIN']
    xMax = ROOM_DIMENSIONS['X_MAX']
    yMin = ROOM_DIMENSIONS['Y_MIN']
    yMax = ROOM_DIMENSIONS['Y_MAX']
    if (xPos >= xMax/2 and yPos >= yMax/2):
        goToX = xMax - radius
        goToY = yMax
    elif (xPos <= xMax/2 and yPos >= yMax/2):
        goToY = yMax - radius
        goToX = xMin
    elif (xPos >= xMax/2 and yPos <= yMax/2):
        goToY = yMin + radius
        goToX = xMax
    else:
        goToX = xMin + radius
        goToY = yMin
    goto(goToY, goToX)

def spiralOrder(matrix, radius, xMin, yMin):
    payload = getinstance().json()['payload']
    itemsBin = payload['itemsBin']
    itemsCollected = payload['itemsCollected']
    totalCount = payload['constants']['TOTAL_COUNT']
    scanRadius = payload['constants']['SCAN_RADIUS']
    scanRadius = math.floor(scanRadius/2)
    total = totalCount['ORGANIC'] + totalCount['RECYCLE'] + totalCount['GARBAGE']
    print(totalCount['ORGANIC'])
    print(totalCount)
    print(itemsCollected)
    print(itemsBin)
    count = radius + 1
    newone = matrix
    rows, columns = len(matrix), len(matrix[0])
    seen = [[False] * columns for _ in matrix]
    row_dir = [0, 1, 0, -1]
    col_dir = [1, 0, -1, 0]
    r = c = di = 0

    print(total)
    print(itemsCollected)
    print(itemsBin)
    print(scanRadius)
    for _ in range(rows * columns):
        if (count == (radius * 2 + 1)):
            print(di)
            print (r, c)
            if di == 0 and r%1 == 0:
                print('Hitting if', di);
                newone = scanAndClean(r, c, xMin, yMin, newone)
            elif di == 2 and r%1 == 0:
                print('Hitting if', di);
                newone = scanAndClean(r, c, xMin, yMin, newone)
            elif di == 1 and c%1 == 0:
                print('Hitting if', di);
                newone = scanAndClean(r, c, xMin, yMin, newone)
            elif di == 3 and c%1 == 0:
                print('Hitting if', di);
                newone = scanAndClean(r, c, xMin, yMin, newone)
            count = 0
        seen[r][c] = True
        cr, cc = r + row_dir[di], c + col_dir[di]
        if 0 <= cr < rows and 0 <= cc < columns and not seen[cr][cc]:
            r, c = cr, cc
        else:
            di = (di + 1) % 4
            r, c = r + row_dir[di], c + col_dir[di]
        count += 1
    itemsHeld = getinstance().json()['payload']['itemsHeld']
    itemsBin =  getinstance().json()['payload']['itemsBin']
    # while len(itemsHeld) != 0 or len(itemsBin) != 0:
    #     checkBins(True)
    #     itemsHeld = getinstance().json()['payload']['itemsHeld']
    #     itemsBin =  getinstance().json()['payload']['itemsBin']
    # finish()
    return newone

def scanAndClean(r, c, xMin, yMin, newone):
    newone[r][c] = 1
    print(r, c)
    goto(yMin+r, xMin+c)
    shouldReRun = scanSpot()
    while (shouldReRun):
        goto(yMin+r, xMin+c)
        shouldReRun = scanSpot()
    checkBins(False)
    return newone

def checkBins(isLast):
    payload = getinstance().json()['payload']
    instance = getinstance().json()
    bins = payload['constants']['BIN_LOCATION']
    organicBin = bins['ORGANIC']
    organicX = organicBin['X']
    organicY = organicBin['Y']
    recycleBin = bins['RECYCLE']
    recycleX = recycleBin['X']
    recycleY = recycleBin['Y']
    garbageBin = bins['GARBAGE']
    garbageX = garbageBin['X']
    garbageY = garbageBin['Y']
    location = payload['location']
    x = location['x']
    y = location['y']
    radius = payload['constants']['SCAN_RADIUS']
    itemsHeld = instance['payload']['itemsHeld']
    if (abs(x - organicX) <= 3*radius and abs(y - organicY) <= 3* radius  and (len(itemsHeld) > 20 or isLast)):
        goto(organicY, organicX)
        unload_tobin(instance, 'ORGANIC')
        goto(recycleY, recycleX)
        unload_tobin(instance, 'RECYCLE')
        goto(garbageY, garbageX)
        unload_tobin(instance, 'GARBAGE')
    # if (abs(x - recycleX) <= radius and abs(y - recycleY) <= radius):
    #
    # if (abs(x - garbageX) <= radius and abs(y - garbageY) <= radius):

#inst = createinstance()['payload']
def printRoom(roomMatrix):
    for row in roomMatrix:
        print(row)

def scanSpot():
    shouldReRun = False
    instanceInfo = scan()
    currentLoc = instanceInfo['payload']['location']
    scannedInfo = instanceInfo['payload']['itemsLocated']
    for elements in scannedInfo:
        shouldReRun = True
        goto(elements['y'], elements['x'])
        collect(elements['id'])
    return shouldReRun

def unload_tobin(instancejson, type):
    # get current bin type

    items_held = instancejson['payload']['itemsHeld']
    #print(items_held)

    if (type == 'ORGANIC'):
        print('hit org')
        for e in items_held:
                print(e)
                print(e['id'])
                unload(e['id'])
    elif(type == 'RECYCLE'):
        print('hit rec')
        for e in items_held:
                    print(e)
                    print(e['id'])
                    unload(e['id'])
    elif(type == 'GARBAGE'):
        print('hit gar')
        for e in items_held:
                print(e)
                print(e['id'])
                unload(e['id'])

# print("maxes: " + str(inst['payload']['constants']['ROOM_DIMENSIONS']))
# print("Where we are: " + str(inst['payload']['location']))

# goToNearestCorner()

# inst = getinstance().json()
# print("Where we are: " + str(inst['payload']['location']))
