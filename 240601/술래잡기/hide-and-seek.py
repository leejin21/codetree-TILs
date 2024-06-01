'''
TODO: self.targetList에서 dict으로 변경

'''
dirDict = {0: "→", 1: "↓", 2: "←", 3: "↑"}
drList = [0, 1, 0, -1]
dcList = [1, 0, -1, 0]

targets = []
grid = []
taggerDirGrid = []

class Person:
    def __init__(self, i, r, c, d):
        self.i = i
        self.r = r
        self.c = c
        self.d = d # dirDict
        self.abandon = False

    def __str__(self):
        return str(self.i) + ": " + dirDict[self.d]

    def setOppDir(self):
        self.d = (self.d + 2) % 4

    def getNextPosition(self):
        dr, dc = drList[self.d], dcList[self.d]
        next_r, next_c = self.r + dr, self.c + dc
        return next_r, next_c

    def setNextPosition(self, r, c):
        self.r = r
        self.c = c


class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.targetList = []
        self.isTree = False

    def __str__(self):
        return "1" if self.isTree else "0"

class Tagger:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.d = 3
        self.dirGrid = []
        self.oppDirGrid = []
        self.isFineDir = True   # False = use opposite dir grid
        self.isFirst = True
        self.initDirGrid();
    
    def initDirGrid(self):
        self.visit = [[False]*N for i in range(N)]
        self.dirGrid = [[-1]*N for _ in range(N)]
        self.oppDirGrid = [[-1]*N for _ in range(N)]
        
        init_r, init_c, init_d = N//2, N//2, 3
        self.visit[init_r][init_c] = True
        self.dirGrid[init_r][init_c] = init_d
        self.oppDirGrid[init_r][init_c] = init_d

        dr, dc = drList[init_d], dcList[init_d]
        next_r, next_c = init_r + dr, init_c + dc
        self.oppDirGrid[next_r][next_c] = self.getOppDir(init_d)

        self._initDirGrid(next_r, next_c, init_d)

        # self.printDirGrid()
        # self.printOppDirGrid()

    def _initDirGrid(self, r, c, d):
        # self.printOppDirGrid()
        if r == 0 and c == 0:
            self.dirGrid[r][c] = self.oppDirGrid[r][c]
            return 
        next_r, next_c, next_d = self.getNext(r, c, d)
        self.visit[r][c] = True
        self.dirGrid[r][c] = next_d
        self.oppDirGrid[next_r][next_c] = self.getOppDir(next_d)

        self._initDirGrid(next_r, next_c, next_d)

    def getNext(self, r, c, d):
        next_d = (d + 1) % 4
        dr, dc = drList[next_d], dcList[next_d]
        next_r = r + dr
        next_c = c + dc
        if self.visit[next_r][next_c]:
            dr, dc = drList[d], dcList[d]
            return r+dr, c+dc, d
        return next_r, next_c, next_d 

    def printDirGrid(self):
        for r in range(N):
            print(self.dirGrid[r])
        print()

    def printOppDirGrid(self):
        for r in range(N):
            print(self.oppDirGrid[r])
        print()

    def getOppDir(self, d):
        return (d+2)%4

    def getDir(self):
        if self.isFineDir:
            d = self.dirGrid[self.r][self.c]
        else:
            d = self.oppDirGrid[self.r][self.c]
        return d

    def setNextPos(self):
        # self.
        d = self.getDir()

        if (self.isFineDir and self.r == 0 and self.c == 0) or (not self.isFineDir and self.r == N//2 and self.c == N//2):
            self.isFineDir = not self.isFineDir
            d = self.getDir()
            
            dr, dc = drList[d], dcList[d]

            self.r, self.c = self.r + dr, self.c + dc
            self.d = self.getDir()
        
        else:
            dr, dc = drList[d], dcList[d]
            self.r, self.c = self.r + dr, self.c + dc
            self.d = self.getDir()
    
    def __str__(self):
        str_d = dirDict[self.d] if self.d != -1 else str(self.d)
        return "r, c, d: "  +  str(self.r) + ", " + str(self.c)+ ", " + str_d

def init():
    for i in range(M):
        r, c, d = [int(x) for x in input().split()]
        r, c = r-1, c-1
        d = 0 if d == 1 else 1
        target = Person(i, r, c, d)
        targets.append(target)

    for _ in range(H):
        r, c = [int(x) for x in input().split()]
        r, c = r-1, c-1
        grid[r][c].isTree = True

    for target in targets:
        r, c = target.r, target.c
        grid[r][c].targetList.append(target)

    tagger = Tagger(N//2, N//2)
    return tagger

def printGrid():
    for r in range(N):
        for c in range(N):
            print(grid[r][c], end = " ")
        print()
    
def printTargets(tagger):
    print("===PRINT===")
    print("tagger", tagger)
    print("target")
    for r in range(N):
        for c in range(N):
            cell = grid[r][c]
            if len(cell.targetList) > 0:
                print("r, c: ", r, c, "| ", [str(target) for target in grid[r][c].targetList if not target.abandon])

def turn(num, tagger):
    point = 0
    targetsRun(tagger)
    # print("turn: ", num)
    # printTargets(tagger)
    point += taggerTurn(num, tagger)
    # printTargets(tagger)
    return point

def targetsRun(tagger):
    for target in targets:
        if target.abandon:
            continue
        if getDistance(target, tagger) <= 3:
            next_r, next_c = target.getNextPosition()
            if isOutOfGrid(next_r, next_c):
                target.setOppDir()
                next_r, next_c = target.getNextPosition()

            if tagger.r == next_r and tagger.c == next_c:
                # not move
                pass
            else:
                # move
                grid[target.r][target.c].targetList.remove(target)
                grid[next_r][next_c].targetList.append(target)
                target.setNextPosition(next_r, next_c)

def isOutOfGrid(r, c):
    if r < 0 or r >= N:
        return True
    if c < 0 or c >= N:
        return True
    return False

def getDistance(target, tagger):
    # calculate distance
    return abs(target.r - tagger.r) + abs(target.c - tagger.c)

def taggerTurn(num, tagger):
    point = 0
    tagger.setNextPos()
    # print("taggerTurn, tagger: ", tagger)
    for i in range(3):
        dr, dc = drList[tagger.d], dcList[tagger.d]
        next_r = tagger.r + dr*i
        next_c = tagger.c + dc*i
        if isOutOfGrid(next_r, next_c):
            continue
        
        # print(next_r, next_c)
        cnt = len(grid[next_r][next_c].targetList)
        while(cnt > 0):
            target = grid[next_r][next_c].targetList.pop()
            if grid[target.r][target.c].isTree:
                # tree, can not catch
                # print("tree")
                grid[next_r][next_c].targetList.append(target)
            else:
                target.abandon = True
                point += num
            cnt -= 1
    
    return point

def main():
    tagger = init()
    # printGrid()
    # printTargets(tagger)
    num = 1
    tot = 0
    while(num <= K):
        tot += turn(num, tagger)
        num += 1

    print(tot)

N, M, H, K = [int(x) for x in input().split()]
targets = []
grid = [[Cell(r,c) for c in range(N)] for r in range(N)]

main()