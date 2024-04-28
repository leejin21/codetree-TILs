'''
싸움땅


'''
from collections import deque


drList = [-1, 0, 1, 0]
dcList = [0, 1, 0, -1]

dirDict = {0: '↑', 1: '→', 2: '↓', 3: '←'}

class GameResult:
    def __init__(self, winner, loser, point):
        self.winner = winner
        self.loser = loser
        self.point = point

class Player:
    def __init__(self, num, row, column, direction, baseStrength):
        self.num = num
        self.row = row                     # 위치 x 좌표
        self.column = column               # 위치 y 좌표
        self.direction = direction         # 플레이어 방향
                                            # 0: ↑, 1: →, 2: ↓, 3: ←
        self.baseStrength = baseStrength   # 초기 능력치
        self.gunStrength = 0  # 총 능력치는 우선 초기 능력치로 초기화
        self.point = 0

class Area:
    def __init__(self, row, column, gunQueue):
        self.row = row
        self.column = column
        self.gunQueue = gunQueue
        self.stationedPlayer = []

def prettyPrintGunGrid():
    print("===gun grid===")
    for r in range(N):
        for c in range(N):
            # if grid[r][c].gunList:
            gunListString = ""
            for gun in grid[r][c].gunQueue:
                gunListString += str(gun) + ' '
            print(f'[{gunListString: <4}]', end = " ")
        print(" ")

def prettyPrintPlayerGrid():
    print("===player grid===")
    for r in range(N):
        for c in range(N):
            _str = ""
            for player in grid[r][c].stationedPlayer:
                _str += str(player.num) + ", "
            print(f'[{_str[:-2] :<4}]', end = " ")
        print("")

def prettyPrintPlayer():
    print("===player info===")
    for p in playerList:
        print(p.num, ":  dir=", dirDict[p.direction], ", baseStrength= ", p.baseStrength, ", gunStrength= ", p.gunStrength, ", point= ", p.point )
    
def getOppositeDirection(direction):
    return (direction+2)%4

def getNextRowCol(player):
    dr = drList[player.direction]
    dc = dcList[player.direction]

    next_r = player.row + dr
    next_c = player.column + dc

    if 0 <= next_r < N and 0 <= next_c < N:
        return next_r, next_c

    player.direction = getOppositeDirection(player.direction)
    return getNextRowCol(player)

def changeToBestGun(gunQ, player):
    for i in range(len(gunQ)):
        candGun = gunQ.popleft()
        if candGun > player.gunStrength:
            if player.gunStrength != 0: # only when player have gun
                gunQ.append(player.gunStrength)
            player.gunStrength = candGun
        else:
            gunQ.append(candGun)
    
def normalMove(nextArea, player):
    '''   
    2-1 when no player:
            when yes gun: 
                when new gun > old gun: 
                    get new gun
                    dump old gun at the area
    '''
    cur_r, cur_c = player.row, player.column
    curArea = grid[cur_r][cur_c]
    
    curArea.stationedPlayer = []
    nextArea.stationedPlayer.append(player)
    
    player.row = nextArea.row
    player.column = nextArea.column

def getGameResult(player1, player2):
    player1Tot = player1.gunStrength + player1.baseStrength
    player2Tot = player2.gunStrength + player2.baseStrength

    point = abs(player1Tot - player2Tot)

    if player1Tot > player2Tot:
        return GameResult(player1, player2, point)
    elif player2Tot > player1Tot:
        return GameResult(player2, player1, point)
    else:
        if player1.baseStrength > player2.baseStrength:
            return GameResult(player1, player2, point)
        else:
            return GameResult(player2, player1, point)

def getNextRowColWhenLose(player):
    dr = drList[player.direction]
    dc = dcList[player.direction]

    next_r = player.row + dr
    next_c = player.column + dc
    
    
    if 0 <= next_r < N and 0 <= next_c < N:
        nextArea = grid[next_r][next_c]
        if len(nextArea.stationedPlayer) == 0:
            return next_r, next_c

    player.direction = (player.direction + 1) % 4
    return getNextRowColWhenLose(player)

def movePlayerAfterLose(player):
    '''
        원래 방향대로 이동
        while 다른 플레이어 or 격자 밖
            90도씩 회전
        이동
        총 획득
    '''
    cur_r, cur_c = player.row, player.column
    curArea = grid[cur_r][cur_c]

    curArea.stationedPlayer.remove(player)
    
    next_r, next_c = getNextRowColWhenLose(player)
    nextArea = grid[next_r][next_c]
    nextArea.stationedPlayer.append(player)

    player.row = nextArea.row
    player.column = nextArea.column

    return nextArea

def movePlayer(player):
    '''
    방향대로 한칸만큼 이동
    1-1 이동의 의미
        현 Area.stationedPlayer = None
        next Area.stationedPlayer = player로
        격자를 벗어나는 경우: 정반대 방향으로 방향을 바꾸어서 1만큼 이동 (((현 방향)+2)%4)
        0: ↑, 1: →, 2: ↓, 3: ←
    '''
    next_r, next_c = getNextRowCol(player)
    nextArea = grid[next_r][next_c]

    if not nextArea.stationedPlayer: # no player
        # print("++", player.num, " NORMAL MOVE")
        normalMove(nextArea, player)
        if nextArea.gunQueue:
            changeToBestGun(nextArea.gunQueue, player)
        
    else:                            # yes player
        # print("++", player.num, " NOT NORMAL MOVE")
        oldPlayer = nextArea.stationedPlayer[0]
        newPlayer = player

        # firstly move newPlayer
        normalMove(nextArea, newPlayer)

        gameResult = getGameResult(oldPlayer, newPlayer)
        winner = gameResult.winner
        loser = gameResult.loser

        # winner get point
        winner.point += gameResult.point
        # loser dump gun only when has the gun
        if (loser.gunStrength != 0):
            nextArea.gunQueue.append(loser.gunStrength)
        loser.gunStrength = 0
        # winner can get gun
        changeToBestGun(nextArea.gunQueue, winner)
        # loser move to other place
        loserNextArea = movePlayerAfterLose(loser)
        # loser can get a gun
        changeToBestGun(loserNextArea.gunQueue, loser)
       
def getPoint():
    for player in playerList:
        print(player.point, end = " ")
    print("")


def solution():
    '''
    0: ↑, 1: →, 2: ↓, 3: ←
    '''
    turn = 1
    # test get next row col
    # player = Player(0,0, 3, 0)
    # print(player.row, player.column, player.direction)
    # print(getNextRowCol(player), player.direction)

    while(turn<=K):
        # prettyPrintGunGrid()
        # prettyPrintPlayerGrid()
        # 이동
        # print("====", turn , ". 이동====")
        for player in playerList:
            movePlayer(player)
            # prettyPrintGunGrid()
            # prettyPrintPlayerGrid()
            # prettyPrintPlayer()
        turn += 1

    getPoint()

    
N, M, K = [int(i) for i in input().split()]

grid = []
playerList = []

for r in range(N):
    temp = []
    for c, gun in enumerate(input().split()):
        gun = int(gun)
        q = deque()
        if gun != 0:
            q.append(gun)
        area = Area(r,c,q)
        temp.append(area)
    grid.append(temp)

    # 숫자 0은 빈 칸, 0보다 큰 값은 총의 공격력을 의미

for m in range(M):
    x, y, d, s = [int(i) for i in input().split()]
    player = Player(m, x-1, y-1, d, s)
    playerList.append(player)
    grid[x-1][y-1].stationedPlayer.append(player)

solution()