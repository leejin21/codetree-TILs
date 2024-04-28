'''
제초제

1. 성장

인접 4개 칸만큼 나무가 성장
제초제 뿌려진 칸은 나무 성장 X (제초제 수명 = 0 이면 나무 성장 가능)

2. 번식

인접 4개 칸에 번식을 진행(총 번식이 가능한 칸의 개수만큼 나눠서.)
단, 벽, 다른 나무, 제초제 모두 없는 칸

* 기존 나무 -> 인접 다른 칸으로 번식 지행, 다른 칸 개수 카운트해서.
* 단, 벽, 다른 나무, 제초제 모두 없는 칸 (제초제 수명 = 0 이면 나무 성장 가능)
* 제초제 뿌려진 칸은 나무 번식 X

3. 제초제 뿌리기

각 칸 중 제초제를 뿌렸을 때 나무가 가장 많이 박멸되는 칸 선정

1. 제초제 뿌릴 칸 선정 (브루트포스?)
    최대 연산 40 * 400
    나무가 있는 칸에 뿌려야 함, 전파 도중 벽이 있거나 나무가 아예 없는 칸이 있으면 그 후로는 전파X
2. 제초제 뿌리기 작업
    성장, 번식 process에도 영향감
    제초제 수명 = c

4. 년도 +1 
제초제 수명 -1

'''

grid = []
nextGrid = []

nearDrList = [-1, 0, 0, 1] # 인접 4칸
nearDcList = [0, -1, 1, 0]

diDrList = [-1, 1, -1, 1] # 대각선
diDcList = [-1, -1, 1, 1]

class Area:
    def __init__(self, num, row, col):
        self.num = num
        self.row = row
        self.col = col
        self.remainToxic = 0

def prettyPrintGrid():
    # print("<<normal grid>>")
    for tl in grid:
        for area in tl:
            print(f'[{area.num: <3}|{area.remainToxic: <2}]', end = "")
        print("")

def prettyPrintToxicGrid(maxkill, tgrid):
    print("<<toxic grid>>")
    print("max kill: ", maxkill)
    for tl in tgrid:
        for area in tl:
            print(area, end = " ")
        print("")

def isTree(area):
    if area.num <= 0:
        # empty or wall
        return False
    if area.remainToxic > 0:
        # toxic remains
        return False
    return True

def growTree():
    '''
    인접 4개 칸만큼 나무가 성장
    제초제 뿌려진 칸은 나무 성장 X (제초제 수명 = 0 이면 나무 성장 가능)
    '''
    # print("--grow tree--")
    for r in range(N):
        for c in range(N):
            curArea = grid[r][c]
            if not isTree(curArea):
                continue
            cnt = 0
            for dr, dc in zip(nearDrList, nearDcList):
                next_r = r + dr; next_c = c + dc
                if next_r < 0 or next_r >= N:
                    continue
                if next_c < 0 or next_c >= N:
                    continue
                nextArea = grid[next_r][next_c]
                if isTree(nextArea):
                    cnt += 1
            curArea.num += cnt

def canBornTree(area):
    '''
    벽, 다른 나무, 제초제 모두 없는 칸
    '''
    if area.num < 0:            # wall
        return False
    if area.num > 0:            # other tree
        return False
    if area.remainToxic > 0:    # 제초제 잔여
        return False
    return True

def initNextGrid():
    for r in range(N):
        for c in range(N):
            nextGrid[r][c] = 0

def makeTree():
    '''
    인접 4개 칸에 번식을 진행(총 번식이 가능한 칸의 개수만큼 나눠서.)
    단, 벽, 다른 나무, 제초제 모두 없는 칸

    * 기존 나무 -> 인접 다른 칸으로 번식 지행, 다른 칸 개수 카운트해서.
    * 단, 벽, 다른 나무, 제초제 모두 없는 칸 (제초제 수명 = 0 이면 나무 성장 가능)
    * 제초제 뿌려진 칸은 나무 번식 X
    '''
    # print("--make tree--")
    initNextGrid()
    for r in range(N):
        for c in range(N):
            area = grid[r][c]
            if not isTree(area):
                continue
            
            bornAreaList = []
            for dr, dc in zip(nearDrList, nearDcList):
                next_r = r + dr; next_c = c + dc
                if next_r < 0 or next_r >= N:
                    continue
                if next_c < 0 or next_c >= N:
                    continue

                nextArea = grid[next_r][next_c]
                if canBornTree(nextArea):
                    bornAreaList.append(nextArea)

            bornPerArea = len(bornAreaList)
            for bornArea in bornAreaList:
                next_r, next_c = bornArea.row, bornArea.col
                nextGrid[next_r][next_c] += area.num // bornPerArea
                # use nextGrid for independent result

    for r in range(N):
        for c in range(N):
            grid[r][c].num += nextGrid[r][c]

def getTreeCnt(dn, k, r, c):
    # dr = direction number, k = radius, r = row, c = column
    area = grid[r][c]
    nextGrid[r][c] = 1
    if area.num == -1:
        return 0
    if area.num == 0:
        return 0
    if k >= K:
        return area.num
    
    dr, dc = diDrList[dn], diDcList[dn]
    next_r = r + dr; next_c = c + dc
    if next_r < 0 or next_r >= N:
        return area.num
    if next_c < 0 or next_c >= N:
        return area.num

    return area.num + getTreeCnt(dn, k+1, next_r, next_c)

def getKillTreeCnt(area):
    cnt = area.num
    r, c = area.row, area.col
    initNextGrid()
    nextGrid[r][c] = 1

    for dn in range(len(diDrList)):
        dr, dc = diDrList[dn], diDcList[dn]
        next_r = r + dr; next_c = c + dc
        if next_r < 0 or next_r >= N:
            continue
        if next_c < 0 or next_c >= N:
            continue
        cnt += getTreeCnt(dn, 1, next_r, next_c)

    return cnt

def deepCopyGrid(fromGrid, toGrid):
    for r in range(N):
        for c in range(N):
            toGrid[r][c] = fromGrid[r][c]

def selectAreaToGetToxic():
    # 제초제 뿌릴 칸 고르기
    '''
    1. 제초제 뿌릴 칸 선정 (브루트포스?)
        최대 연산 40 * 400
        나무가 있는 칸에 뿌려야 함, 전파 도중 벽이 있거나 나무가 아예 없는 칸이 있으면 그 후로는 전파X
    '''
    maxKillTreeCnt = 0
    saveGridForKill = [[0 for _ in range(N)] for __ in range(N)]
    target = None

    # print("== select area ==")
    for r in range(N):
        for c in range(N):
            area = grid[r][c]
            if not isTree(area):
                # print('[   ]', end = "")
                continue
            killTreeCnt = getKillTreeCnt(area)
            # print(f'[{killTreeCnt:<3}]', end = "")
            if maxKillTreeCnt < killTreeCnt:
                maxKillTreeCnt = killTreeCnt
                deepCopyGrid(nextGrid, saveGridForKill)
                target = area
            elif maxKillTreeCnt == killTreeCnt:
                if target.row > area.row:
                    deepCopyGrid(nextGrid, saveGridForKill)
                    target = area
                elif target.row == area.row:
                    if target.col > area.col:
                        deepCopyGrid(nextGrid, saveGridForKill)
                        target = area
        # print("")

    # prettyPrintToxicGrid(maxKillTreeCnt, saveGridForKill)        
    return maxKillTreeCnt, saveGridForKill

def killTree():
    '''
    1. 제초제 뿌릴 칸 선정 (브루트포스?)
    2. 제초제 뿌리기 작업
        성장, 번식 process에도 영향감
        제초제 수명 = c
    '''

    maxKillTreeCnt, saveGridForKill = selectAreaToGetToxic()

    applyNewYear()
    # prettyPrintGrid()
    # print("--kill tree--")    
    # kill tree
    for r in range(N):
        for c in range(N):
            if saveGridForKill[r][c] == 0:
                continue
            
            area = grid[r][c]
            if area.num != -1:
                area.num = 0
            area.remainToxic = C

    return maxKillTreeCnt

def applyNewYear():
    # print("--apply New Year--")
    for r in range(N):
        for c in range(N):
            area = grid[r][c]
            if area.remainToxic > 0:
                area.remainToxic -= 1

def solution():
    turn = 1
    totalKilled = 0
    # prettyPrintGrid()
    while(turn <= M):
        # print("=======TURN: ", turn, "=======")
        growTree()
        # prettyPrintGrid()
        makeTree()
        # prettyPrintGrid()

        killedNum = killTree()
        turn += 1
        totalKilled += killedNum
        # prettyPrintGrid()

    print(totalKilled)
        

N, M, K, C = [int(i) for i in input().split()]

for r in range(N):
    grid.append([Area(int(num), r, c) for c, num in enumerate(input().split())])
    nextGrid.append([0 for _ in range(N)])

solution()