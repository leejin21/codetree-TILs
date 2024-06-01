'''


'''
dirDict = {0: "→", 1: "↓", 2: "←", 3: "↑"}
targets = []
grid = []

class Target:
    def __init__(self, r, c, d):
        self.r = r
        self.c = c
        self.d = d # dirDict

    def __str__(self):
        return dirDict[self.d]

class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.targetList = []
        self.isTree = False

    def __str__(self):
        return "1" if self.isTree else "0"

def init():
    for _ in range(M):
        r, c, d = [int(x) for x in input().split()]
        r, c = r-1, c-1
        d = 0 if d == 1 else 1
        target = Target(r, c, d)
        targets.append(target)

    for _ in range(H):
        r, c = [int(x) for x in input().split()]
        r, c = r-1, c-1
        grid[r][c].isTree = True

    for target in targets:
        r, c = target.r, target.c
        grid[r][c].targetList.append(target)

def printGrid():
    for r in range(N):
        for c in range(N):
            print(grid[r][c], end = " ")
        print()
    
def printTargets():
    for r in range(N):
        for c in range(N):
            cell = grid[r][c]
            if len(cell.targetList) > 0:
                print("r, c: ", r, c, "| ", [str(target) for target in grid[r][c].targetList])

def main():
    init()
    printGrid()
    printTargets()


N, M, H, K = [int(x) for x in input().split()]
targets = []
grid = [[Cell(r,c) for c in range(N)] for r in range(N)]

main()