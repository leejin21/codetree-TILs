'''
하나의 이동 선에는 하나의 팀만이 존재한다.

<초기 작업>
1. DFS로 
머리사람의 경우 visit 
-> Player 생성 및 Team에 추가, 
  GRID는 이동선만으로 초기화
  visit flag = true

while: <라운드 진행, round = 1 ~ >

2.1 Team에 있는 playerList 모두 한칸씩 이동 진행. 
이때, 이동 시 row col dir 따지고 이동(모서리 조심)

2.2 공 던지기
round 별로 공 던지는 위치 다름
4n번째 라운드를 넘어가는 경우에는 다시 1번째 라운드의 방향으로 돌아갑니다.
최초에 만나는 사람 = 공 get

2.3 공 획득의 경우,
최초에 만나는 사람 -> 머리사람 기준 k번째 사람,
팀 점수 += k^2
팀.order *= -1

정방향 = 가장 처음 발견된 방향으로 취급, 
역방향 = 바뀐 방향


<예외케이스>
7 2 1
2 2 1 0 0 0 0
2 0 3 0 2 1 4
2 2 2 0 2 0 4
0 0 0 0 3 0 4
0 0 4 4 4 0 4
0 0 4 0 0 0 4
0 0 4 4 4 4 4

'''
import sys

read = sys.stdin.readline

directionDict = {0: "→", 1: "↑", 2: "←", 3: "↓"}

diList = [0, -1, 0, 1]
djList = [1, 0, -1, 0]

teamList = []

class Team:
    def __init__(self):
        self.playerList = []
        self.isReversed = False
        # 0: 0=HEADER, LAST=TAIL (정방향, 가장 처음 발견된 방향)
        # 1: LAST=HEADER, 0=TAIL (역방향)
        self.totalPoint = 0

    def __str__(self):
        s = "["
        for p in self.playerList:
            s += p.__str__() + ","
        s+= "]"
        return s

    def memoInGrid(self):
        for p in self.playerList:
            grid[p.row][p.col] = p

class Player:
    def __init__(self, row, col, order):
        self.row = row
        self.col = col
        # self.direction = direction
            # 0: →, 1: ↑, 2: ←, 3: ↓ (반시계 방향)
        self.order = order
            # 순서 when 정방향(가장 처음 발견된 머리사람 기준)
        self.reversedOrder = -1
            # 순서 when 역방향, 나중에 계산
        self.next_row = -1
        self.next_col = -1
        self.team = None

    def __str__(self):
        return "(" + str(self.row) + "," + str(self.col) + ") : " + "O(" + str(self.order) + ")R(" + str(self.reversedOrder) + ")"

    def realMove(self):
        self.row = self.next_row
        self.col = self.next_col

    def updateNextPos(self, team):
        # print("updateNextPos", self.row, self.col)
        if team.isReversed:
            next_i, next_j = self.reversedMove(team)
        else:
            next_i, next_j = self.forwardMove(team)
        
        self.next_row, self.next_col = next_i, next_j
    
    def forwardMove(self, team):
        # print("forward move")
        if self.order == 1:
            # when head player
            next_i, next_j = self.headForwardMove(team)
        else:
            curOrder = self.order-1
            prevPlayer = team.playerList[curOrder-1]
            next_i, next_j = prevPlayer.row, prevPlayer.col
        
        return next_i, next_j
                
    def headForwardMove(self, team):
        # print("head move")
        curOrder = self.order-1
        postPlayer = team.playerList[curOrder+1]
        exclude_i, exclude_j = postPlayer.row, postPlayer.col
        i, j = self.row, self.col

        for di, dj in zip(diList, djList):
            next_i = i + di
            next_j = j + dj
            if next_i < 0 or next_i >= N:
                continue
            if next_j < 0 or next_j >= N:
                continue

            if next_i == exclude_i and next_j == exclude_j:
                # 뒤 플레이어 자리
                continue
            
            if grid[next_i][next_j] == 0:
                # 빈칸
                continue
            # print("next_i: ", next_i, "next_j: ", next_j)
            return next_i, next_j

    def reversedMove(self, team):
        # print("REVERSED MOVE")
        if self.reversedOrder == 1:
            # when head player
            next_i, next_j = self.headReversedMove(team)
        else:
            curOrder = self.order-1
            prevPlayer = team.playerList[curOrder+1]
            next_i, next_j = prevPlayer.row, prevPlayer.col
                
        return next_i, next_j
    
    def headReversedMove(self, team):
        curOrder = self.order-1
        postPlayer = team.playerList[curOrder-1]
        exclude_i, exclude_j = postPlayer.row, postPlayer.col
        i, j = self.row, self.col
        
        for di, dj in zip(diList, djList):
            next_i = i + di
            next_j = j + dj
            if next_i < 0 or next_i >= N:
                continue
            if next_j < 0 or next_j >= N:
                continue

            if next_i == exclude_i and next_j == exclude_j:
                # 뒤 플레이어 자리
                continue
            
            if grid[next_i][next_j] == 0:
                # 빈칸
                continue

            return next_i, next_j
    
def printTeam():
    for team in teamList:
        print(team)
        print("reverse:", team.isReversed, "| totalPoint: ", team.totalPoint)

def findPlayers(player, team):
    '''
    머리사람 찾고
    머리사람 기준 nexti, nextj 찾았을 때 (diList, djList)
    (1) 2인 경우
        그냥 추가
    (2) 3인 경우
        마지막, 종료조건
    (3) 0, 4인 경우
    -> 무시
    '''
    i, j = player.row, player.col
    order = player.order
    team.append(player)
    visited[i][j] = 1

    if grid[i][j] == 3:
        # tail player
        return

    for di, dj in zip(diList, djList):
        next_i = i + di
        next_j = j + dj
        if next_i < 0 or next_i >= N:
            continue
        if next_j < 0 or next_j >= N:
            continue

        if grid[next_i][next_j] == 0:
            # 빈칸
            continue
        if grid[next_i][next_j] == 4:
            # 이동 선
            continue
        if visited[next_i][next_j] == 1:
            # already visited
            continue
        
        p = Player(next_i, next_j, order+1)
        findPlayers(p, team)

def findTeam(i, j):
    headPlayer = Player(i, j, 1)
    visited[i][j] = 1
    candPlayerList = [headPlayer]
    playerList = [headPlayer]
    
    for di, dj in zip(diList, djList):
        next_i = i + di
        next_j = j + dj

        if next_i < 0 or next_i >= N:
            continue
        if next_j < 0 or next_j >= N:
            continue
        
        if visited[next_i][next_j] == 1:
            continue

        if grid[next_i][next_j] == 2:
            # 나머지 사람
            p = Player(next_i, next_j, 2)
            findPlayers(p, playerList)
            candPlayerList = None
            break

        if grid[next_i][next_j] == 3:
            # 꼬리
            p = Player(next_i, next_j, 2)
            candPlayerList.append(p)
        
    team = Team()
    if candPlayerList:
        # 예외 케이스) 4 4 1 3 4 4
        tail = candPlayerList[-1]
        i,j = tail.row, tail.col 
        visited[i][j] = 1
        team.playerList = candPlayerList
    else:
        team.playerList = playerList

    return team

def fillInfoForPlayer():
    #  4 3 2 1
    #  1 2 3 4
    for team in teamList:
        playerList = team.playerList
        for player in playerList:
            player.reversedOrder = len(playerList) - player.order + 1
            player.team = team

def clearGrid():
    # 2. clean grid with only 0 and 4
    for i in range(N):
        for j in range(N):
            if grid[i][j] != 0:
                grid[i][j] = 4

def init():
    # 1. collect teams to teamlist
    for i in range(N):
        for j in range(N):
            if grid[i][j] == 1 and not visited[i][j]:
                team = findTeam(i, j)
                teamList.append(team)
                # print(team)

    # 2. clean grid with only 0 and 4
    clearGrid()
    fillInfoForPlayer()

def game():
    rnd = 1
    while(rnd <= K):
        roundProgress(rnd)
        rnd += 1

def roundProgress(rnd):
    move()
    # print("====", rnd, "MOVE")
    # printTeam()
    gotBallPlayer = throwBall(rnd)
    # print("got ball player: ", gotBallPlayer)

    if gotBallPlayer: 
        rewardTeam(gotBallPlayer)
        changeTeamHeadTail(gotBallPlayer.team)
    
def move():
    clearGrid()
    for team in teamList:
        # when forward
        for p in team.playerList:
            p.updateNextPos(team)

        for p in team.playerList:
            p.realMove()
        team.memoInGrid()

def decideInitialPosition(d, pos):
    # 0: "→", 1: "↑", 2: "←", 3: "↓"
    init_i, init_j = 0, 0
    
    if d == 0:
        init_i += pos
    elif d == 1:
        init_i = N-1
        init_j += pos
    elif d == 2:
        init_i = N-1
        init_j = N-1
        init_i -= pos
    else:
        init_j = N-1
        init_j -= pos

    return init_i, init_j

def throwBall(rnd):
    # print("throwBall")
    rnd = rnd % (4 * N) - 1
    direction = rnd // N
    pos = rnd % N
    
    init_i, init_j = decideInitialPosition(direction, pos)
    # print("init: ", init_i, init_j)

    di, dj = diList[direction], djList[direction]
    for n in range(N):
        next_i = init_i + di * n
        next_j = init_j + dj * n
        # print(next_i, next_j)

        if grid[next_i][next_j] != 0 and grid[next_i][next_j] != 4:
            gotBallPlayer = grid[next_i][next_j]
            return gotBallPlayer

    return None

def rewardTeam(player):
    team = player.team
    playerOrder = player.reversedOrder if team.isReversed else player.order
    team.totalPoint += pow(playerOrder, 2)

def changeTeamHeadTail(team):
    team.isReversed = not team.isReversed

def printGameResult():
    tot = 0
    for team in teamList:
        tot += team.totalPoint

    print(tot)

def main():
    init()
    game()
    printGameResult()
    

N, M, K = [int(x) for x in read().split()]
grid = [[int(x) for x in read().split()] for _ in range(N)]
# 0: 빈칸, 1: 머리사람, 2:나머지사람, 3: 꼬리사람, 4:이동 선
visited = [[0]*N for _ in range(N)]
# 0: not visited, 1: yes visited

main()


'''
0 1
0 2
1 2

'''