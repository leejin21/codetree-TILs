'''
1. 공격자 선정, 목표물 선정
    공격자 선정
    목표물 - 공격자 제외

3. 레이저 공격 시도
최단 경로 확인 및 선택(*막힌 방향 진행에서 반대편으로 나옴, 부서진 포탑에서 stop)
    선택: 최단 경로 기억할 수 있게 하기
(1) 최단 경로 있으면
    경로대로 공격
    레이저 경로에 있는 포탑: 공격자 공격력의 절반만큼 피해
    목표물: 공격자 공격력만큼.


최단 경로 없으면
4. 포탄 공격
    주위8개 방향도 피해 받음
    가장자리에 포탄 떨어지면 추가 피해가 반대편 격자에도 미침

5. 포탄 정비

'''
from collections import deque

MAX_STRENGTH = 5001

class Turret: 
    def __init__(self, strength, row, column, attackedTurn):
        self.strength = strength
        self.attackedTurn = attackedTurn
        self.row = row
        self.column = column

        self.minPath = 100
        self.prevTurret = None
        self.bombAttacked = False

def pickAttacker():
    pickTurret = Turret(50001, 10, 10, -1)

    for ri, rv in enumerate(locationMap):
        for ci, turret in enumerate(rv):
            if turret.strength == 0:
                continue

            if pickTurret.strength > turret.strength:
                pickTurret = turret
            elif pickTurret.strength == turret.strength:
                if pickTurret.attackedTurn < turret.attackedTurn:
                    pickTurret = turret
                elif pickTurret.attackedTurn == turret.attackedTurn:
                    if (pickTurret.row + pickTurret.column) < (turret.row + turret.column):
                        pickTurret = turret
                    elif (pickTurret.row + pickTurret.column) == (turret.row + turret.column):
                        if (pickTurret.column < turret.column):
                            pickTurret = turret

    return pickTurret
            
def pickDefender(attacker):
    pickTurret = Turret(0, -1, -1, 0)

    for ri, rv in enumerate(locationMap):
        for ci, turret in enumerate(rv):
            if turret.strength == 0:
                continue
            if attacker.row == ri and attacker.column == ci:
                continue

            if pickTurret.strength < turret.strength:
                pickTurret = turret
            elif pickTurret.strength == turret.strength:
                if pickTurret.attackedTurn > turret.attackedTurn:
                    pickTurret = turret
                elif pickTurret.attackedTurn == turret.attackedTurn:
                    if (pickTurret.row + pickTurret.column) > (turret.row + turret.column):
                        pickTurret = turret
                    elif (pickTurret.row + pickTurret.column) == (turret.row + turret.column):
                        if (pickTurret.column > turret.column):
                            pickTurret = turret
            
    return pickTurret

def initTurrets():
    for row in locationMap:
        for turret in row:
            turret.minPath = 100
            turret.prevTurret = None
            turret.bombAttacked = False

def findMinPath(attacker, defender):
    # set defender, and turrets prev turrets and set path
    # print("find minimum path")
    # 우(0,1) 하(1,0) 좌(0,-1) 상(-1,0)
    drList = [0,1,0,-1]
    dcList = [1,0,-1,0]

    
    # find path by bfs
    bfsQ = deque()
    bfsQ.append(attacker)

    while(len(bfsQ)>0):
        turret = bfsQ.popleft()

        if turret == defender:
            # 최소 거리로 발견
            break

        cur_r = turret.row
        cur_c = turret.column
        # print("cur_r: ", cur_r, "cur_c: ", cur_c)

        for dr, dc in zip(drList, dcList):
            next_r = cur_r + dr
            next_c = cur_c + dc

            # 반대편으로 보내기
            if next_r < 0:
                next_r = N-1
            if next_r > N-1:
                next_r = 0
            if next_c < 0:
                next_c = M-1
            if next_c > M-1:
                next_c = 0

            # print("next_r: ", next_r, "next_c: ", next_c)
            
            # 고르기
            candTurret = locationMap[next_r][next_c]
            
            if candTurret.strength == 0:
                # 부서진 포탑에 도달
                # print("부서진 포탑")
                continue
            # print("candTurret.minPath: ", candTurret.minPath, "turret.minPath: ", turret.minPath)
            if candTurret.minPath > turret.minPath + 1:
                # 최소의 경우에만
                candTurret.minPath = turret.minPath + 1
                candTurret.prevTurret = turret

                bfsQ.append(candTurret)

def fullAttack(attacker, target):
    target.strength -= attacker.strength
    if target.strength < 0:
        target.strength = 0

def halfAttack(attacker, target):
    target.strength -= attacker.strength // 2
    if target.strength < 0:
        target.strength = 0

def lazerAttack(attacker, defender):
    fullAttack(attacker, defender)
    turret = defender.prevTurret

    while(turret.prevTurret):
        halfAttack(attacker, turret)
        turret = turret.prevTurret

def bombAttack(attacker, defender):
    drList = [-1,1,0,0,-1,1,-1,1]
    dcList = [0,0,-1,1,1,-1,-1,1]

    fullAttack(attacker, defender)
    cur_r = defender.row; cur_c = defender.column
    attacker.bombAttacked = True; defender.bombAttacked = True
    
    for dr, dc in zip(drList, dcList):
        next_r = cur_r + dr
        next_c = cur_c + dc

        # 반대편으로 보내기
        if next_r < 0:
            next_r = N-1
        if next_r > N-1:
            next_r = 0
        if next_c < 0:
            next_c = M-1
        if next_c > M-1:
            next_c = 0

        turret = locationMap[next_r][next_c]
        if turret == attacker:
            continue

        turret.bombAttacked = True
        halfAttack(attacker, turret)

def attack(attacker, defender):
    if defender.prevTurret:
        # print("레이저")
        lazerAttack(attacker, defender)
        return "lazer"
    else:
        # print("bomb")
        bombAttack(attacker, defender)
        return "bomb"

def healWhenLazerAttack(attacker, defender):
    for row in locationMap:
        for turret in row:
            if turret.strength != 0:
                turret.strength += 1

    turret = defender
    while(turret):
        if turret.strength != 0:
                turret.strength -= 1
        turret = turret.prevTurret

def healWhenBombAttack(attacker, defender):
    for row in locationMap:
        for turret in row:
            if turret.strength != 0 and not turret.bombAttacked:
                turret.strength += 1

def prettyPrint():
    print("")
    for i in range(len(locationMap)):
        for j in range(len(locationMap[i])):
            print(locationMap[i][j].strength, end = " ")
        print("")

def solution():
    # print("초기 map")
    # prettyPrint()
    k = 1
    
    while(k<=K):
        initTurrets()
        # 1. 공격자, 타겟 선정
        attacker = pickAttacker()
        defender = pickDefender(attacker)

        attacker.strength += N + M
        attacker.minPath = 0
        attacker.attackedTurn = k
        defender.attackedTurn = k

        # print("공격자: ", attacker.row, attacker.column)
        # print("목표물: ", defender.row, defender.column)
        
        # 2. 공격
        findMinPath(attacker, defender)
        attackType = attack(attacker, defender)

        # print("공격 이후 map")
        # prettyPrint()

        # 3. 정비
        if attackType == "lazer":
            healWhenLazerAttack(attacker, defender)
        else:
            healWhenBombAttack(attacker, defender)
        
        # print("정비 이후 map")
        # prettyPrint()

        k += 1

    print(pickDefender(Turret(-1,-1,-1,0)).strength)


N, M, K = [int(i) for i in input().split()]
locationMap = []
for i in range(N):
    locationMap.append([Turret(int(v), i, j, 0) for j, v in enumerate(input().split())])

solution()