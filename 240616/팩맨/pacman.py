'''


'''

import sys; read = sys.stdin.readline

dirList = ['↑', '↖', '←', '↙', '↓', '↘', '→', '↗']
drList = [-1, -1, 0, 1, 1, 1, 0, -1]
dcList = [0, -1, -1, -1, 0, 1, 1, 1]

packManDirList = ['↑', '←', '↓', '→']
packManDrList = [-1, 0, 1, 0]
packManDCList = [0, -1, 0, 1]

GRID_LENGTH = 4
packMan = None
monsterList = []
monsterEggList = []
grid = [[None]*GRID_LENGTH for _ in range(GRID_LENGTH)]


class PackMan:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.maxEatNum = -1
        self.maxEatingPath = [] # (r, c)
        self.visited = [[0]*GRID_LENGTH for _ in range(GRID_LENGTH)]

    def __str__(self):
        return "r: " + str(self.r) + ", c: " + str(self.c)

    def clearVisited(self):
        self.maxEatNum = -1
        self.maxEatingPath = []

    def isValidPath(self, grid, r, c):
        if r < 0 or r >= len(grid):
            return False
        if c < 0 or c >= len(grid):
            return False

        return True

    def calculateEatNum(self, grid, tempPath):
        num = 0
        for loc in tempPath:
            r, c = loc
            if (self.visited[r][c] == 1):
                continue
            else:
                self.visited[r][c] = 1
                num += len(grid[r][c].existMonsterList)
        
        # clear visited
        for loc in tempPath:
            r, c = loc
            self.visited[r][c] = 0
        
        return num

    def _move(self, grid, depth, tempPath):
        r, c = tempPath[depth-1]

        if depth == 3:
            num = self.calculateEatNum(grid, tempPath)
            if (self.maxEatNum < num):
                self.maxEatNum = num
                self.maxEatingPath = [_ for _ in tempPath]
                # print("EAT CAND: ", self.maxEatNum, self.maxEatingPath)
            return

        for dr, dc in zip(packManDrList, packManDCList):
            next_r, next_c = r + dr, c + dc
            
            if not self.isValidPath(grid, next_r, next_c):
                continue

            tempPath[depth] = (next_r, next_c)
            self._move(grid, depth+1, tempPath)
        

    def move(self, grid):
        self.clearVisited()
        tempPath = [(-1, -1), (-1, -1), (-1, -1)]

        # print("BEFORE PACKMAN MOVE")
        # printGrid()
        # printMonsters()

        for dr, dc in zip(packManDrList, packManDCList):
            next_r, next_c = self.r + dr, self.c + dc
            
            if not self.isValidPath(grid, next_r, next_c):
                continue
            
            tempPath[0] = (next_r, next_c)
            self._move(grid, 1, tempPath)
        
        final_loc = [-1, -1]
        # move to the chosen path
        for loc in self.maxEatingPath:
            r, c = loc
            while(grid[r][c].existMonsterList):
                monster = grid[r][c].existMonsterList.pop()
                monster.isDead = True
                grid[r][c].hasDeadMonster = 2

            final_loc[0], final_loc[1] = r, c

        self.r, self.c = final_loc[0], final_loc[1]

        

class Monster:
    def __init__(self, i, r, c, d):
        self.i = i
        self.r = r
        self.c = c
        self.d = d

        self.isDead = False

    def __str__(self):
        # pos = ", r: " + str(self.r) + ", c: " + str(self.c)
        return "i: " + str(self.i) + ", d: " + dirList[self.d]

    @staticmethod
    def copy(monster):
        return Monster(monster.i, monster.r, monster.c, monster.d)

    def turnFor45Degree(self):
        self.d = (self.d + 1)%(len(dirList))

    def move(self, grid, packMan):
        # printGrid()
        # printMonsters()
        # print("MOVE: ", self.r, self.c, self.d)
        original_d = self.d

        def checkIfNextCellValid(next_r, next_c):
            if next_r < 0 or next_r >= len(grid):
                return False

            if next_c < 0 or next_c >= len(grid):
                return False

            if packMan.r == next_r and packMan.c == next_c:
                return False

            if grid[next_r][next_c].hasDeadMonster > 0:
                return False

            return True

        while(True):
            # print("WHILE d:", self.d)
            next_r = self.r + drList[self.d]
            next_c = self.c + dcList[self.d]

            if not checkIfNextCellValid(next_r, next_c):
                self.turnFor45Degree()
            else:
                # try:
                grid[self.r][self.c].deleteMonster(self)
                    
                # except Exception as e:
                #     print(e)
                #     print("MOB: ", self.r, self.c)
                #     print("while d: ", self.d)
                #     printGrid()
                #     printMonsters()
                
                self.r = next_r
                self.c = next_c
                # print("FIND VALID: ", self.r, self.c)
                grid[self.r][self.c].addMonster(self)
                break
            
            if self.d == original_d:
                break


class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.existMonsterList = []
        self.hasDeadMonster = 0

    def addMonster(self, monster):
        self.existMonsterList.append(monster)
    
    def deleteMonster(self, monster):
        self.existMonsterList.remove(monster)

    def __str__(self):
        return str(len(self.existMonsterList))

########## UTILS ############
def printGrid():
    print("==PRINT GRID==")
    for r in range(GRID_LENGTH):
        for c in range(GRID_LENGTH):
            print(grid[r][c], end = " ")
        print()

def printMonsters():
    print("==PRINT MONSTERS==")
    for r in range(GRID_LENGTH):
        for c in range(GRID_LENGTH):
            cell = grid[r][c]
            if cell.existMonsterList:
                print("r, c: ", r, c)
            for monster in cell.existMonsterList:
                print(monster)


########## LOGIC FUNCTIONS ############

def init():
    global packMan
    packMan = PackMan(R-1, C-1)

    for r in range(GRID_LENGTH):
        for c in range(GRID_LENGTH):
            grid[r][c] = Cell(r, c)

    for m in range(M):
        r, c, d = [int(i) for i in read().split()]
        monster = Monster(m, r-1, c-1, d-1)
        monsterList.append(monster)
        grid[r-1][c-1].addMonster(monster)

def turn():
    startCopyMonsters()
    moveMonsters()
    movePackMan()
    removeDeadMonsters()
    endCopyMonsters()

def startCopyMonsters():
    for monster in monsterList:
        if monster.isDead:
            continue
        egg = Monster.copy(monster)
        monsterEggList.append(egg)

def moveMonsters():
    for monster in monsterList:
        if monster.isDead:
            continue
        monster.move(grid, packMan)

def movePackMan():
    packMan.move(grid)

def removeDeadMonsters():
    for row in grid:
        for cell in row:
            if cell.hasDeadMonster > 0:
                cell.hasDeadMonster -= 1


def endCopyMonsters():
    global monsterEggList, monsterList

    monsterList += monsterEggList
    for monster in monsterEggList:
        r, c = monster.r, monster.c
        grid[r][c].addMonster(monster)

    # clear monster egg list
    monsterEggList = []

def checkAliveMonsterNum():
    cnt = 0
    for row in grid:
        for cell in row:
            cnt += len(cell.existMonsterList)
    return cnt

def main():
    init()

    for t in range(T):
        turn()
        
    print(checkAliveMonsterNum())
    
M, T = [int(i) for i in read().split()]
R, C = [int(i) for i in read().split()]

main()