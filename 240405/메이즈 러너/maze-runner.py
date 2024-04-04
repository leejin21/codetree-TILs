'''
N = 격자의 변길이, M = 참가자
i초일 때(i<K)

이동
움직인 칸은 현재 머물러 있는 칸보다 출구까지의 최단 거리가 가까워야 함(출구와 가까워지는 거리)
상하 > 좌우
한칸에 두명 이상 있을 수 있음.
<출구 찾는 경우>
-1 -1으로 처리

미로 회전 범위 선택
- 한명 이상의 참가자, 출구 포함 가장 작은 정사각형
- (참가자, 출구): |참가자r - 출구r| + |참가자c - 출구c|
- 가장 작은 크기 갖는 정사각형 2개 이상 -> 좌상단 r좌표 작 > 좌상단 c좌표 작
: 비교는 1순위 - min<참가자r, 출구r>, 2순위 - min<참가자c, 출구c>

미로 회전
- 잡힌 곳 내구도 1씩 깎음(>0 인 경우만 1씩 깎아)
- 시계 방향으로 90도 회전

<방법>
r,c, R,C
인덱스 기반 [r][c] 값-> [C-c+1][r]의 자리로 가게 됨
<주의>
참가자도 옮기기(해당하는)
출구도 옮기기

(r,c)

1 2 3
4 5 6
7 8 9

(1,1) (1,2) (1,3)
(2,1) (2,2) (2,3)
(3,1) (3,2) (3,3)

(0,0) (0,1) (0,2) 
(1,0) (1,1) (1,2) 
(2,0) (2,1) (2,2) 

7 4 1
8 5 2
9 6 3

[0,2] = [0,0]
[1,2] = [0,1]
[2,2] = [0,2]


'''
import sys; read = sys.stdin.readline
maze = []
participants = []
partCntExited = 0
exit = []

def isEmptyRoad(r,c):
    if maze[r][c] == 0:
        return True
    return False
    
def checkIfArriveExit(pInfo, eInfo):
    global partCntExited
    p_r, p_c = pInfo
    e_r, e_c = eInfo
    if p_r == e_r and p_c == e_c:
        partCntExited += 1
        return True
    return False

def alreadyExited(pInfo):
    return pInfo[0] == -1 and pInfo[1] == -1

def moveParticipants(pInfo, eInfo):
    # pInfo = participant info = [r,c]
    # eInfo = exit info = [r,c]
    np_r, np_c = pInfo # new location for participants
    p_r, p_c = pInfo
    e_r, e_c = eInfo
    upDownDetermin = False

    # 상하 결정
    if p_r < e_r: # 참가자가 더 위에 있는 경우
        if isEmptyRoad(p_r+1, p_c):
            np_r = p_r + 1
            upDownDetermin = True
    elif p_r > e_r: # 참가자가 더 아래에 있는 경우
        if isEmptyRoad(p_r-1, p_c):
            np_r = p_r - 1
            upDownDetermin = True
    
    # 좌우 결정
    if not upDownDetermin:
        if p_c < e_c: #참가자가 더 왼쪽에 있는 경우
            if isEmptyRoad(p_r, p_c+1):
                np_c = p_c + 1
        elif p_c > e_c: #참가자가 더 오른쪽에 있는 경우
            if isEmptyRoad(p_r, p_c-1):
                np_c = p_c - 1
    
    return np_r, np_c    

def prettyPrint(pList):
    for p in pList:
        for i in p:
            print(i, end = ' ')
        print()

def getRangeForCase(eInfo, pInfo, height, width):
    
    r1 = 0; c1 = 0 # 좌상단
    r2 = 0; c2 = 0 # 우하단

    e_r, e_c = eInfo
    p_r, p_c = pInfo

    if p_r <= e_r and p_c <= e_c:
        if width >= height:
            r1 = e_r - width
            c1 = e_c - width
            r2 = r1 + width
            c2 = c1 + width
        elif width < height:
            r1 = e_r - height
            c1 = e_c - height
            r2 = r1 + height
            c2 = c1 + height
    elif p_r <= e_r and p_c > e_c:
        if width >= height:
            r1 = e_r - width
            c1 = e_c
            r2 = r1 + width
            c2 = c1 + width
        elif width < height:
            r1 = e_r - height
            c1 = e_c
            r2 = r1 + height
            c2 = c1 + height
    elif p_r > e_r and p_c <= e_c:
        if width >= height:
            r1 = e_r
            c1 = e_c - width
            r2 = r1 + width
            c2 = c1 + width
        elif width < height:
            r1 = e_r
            c1 = e_c - height
            r2 = r1 + height
            c2 = c1 + height
    elif p_r > e_r and p_c > e_c:
        if width >= height:
            r1 = e_r
            c1 = e_c
            r2 = r1 + width
            c2 = c1 + width
        elif width < height:
            r1 = e_r
            c1 = e_c
            r2 = r1 + height
            c2 = c1 + height

    # 예외처리
    if r1 < 0:
        r1 = 0
        if width >= height:
            r2 = r1 + width
            c2 = c1 + width
        elif width < height:
            r2 = r1 + height
            c2 = c1 + height
    if c1 < 0:
        c1 = 0
        if width >= height:
            r2 = r1 + width
            c2 = c1 + width
        elif width < height:
            r2 = r1 + height
            c2 = c1 + height
    if r2 > len(maze)-1:
        r2 = len(maze)-1
        if width >= height:
            r1 = r2 - width
            c1 = c2 - width
        elif width < height:
            r1 = r2 - height
            c1 = c2 - height
    if c2 > len(maze)-1:
        c2 = len(maze)-1
        if width >= height:
            r1 = r2 - width
            c1 = c2 - width
        elif width < height:
            r1 = r2 - height
            c1 = c2 - height

    slength = abs(r2 - r1) + 1

    return r1, c1, r2, c2, slength

def getRangeToRotate(eInfo):
    '''
    포함한: 가장 작은 정사각형 범위 정하기 -> 좌상단, 우하단 좌표
    1우) 포함으므로 max(세로길이, 가로길이) 중 골라서
        세로인 경우: abs(세로길이)
        가로인 경우: abs(가로길이)
        <minSquareLen>
    2우) 좌상단 r좌표 더 작은 것 <minSquareR>
    3우) 좌상단 c좌표 더 작은 것 <minSquareC>

    가로=|p_r-e_r|, 세로=|p_c-e_c|
        (1) e_c > p_c && 세로 >= 가로
            좌상단 r = e_r - |p_c - e_c|
            좌상단 c = p_c
            우하단 r = e_r
            우하단 c = e_c
        (2) e_r > p_r && 세로 <= 가로
            좌상단 r = p_r
            좌상단 c = e_c - |p_r - e_r|
            우하단 r = e_r
            우하단 c = e_c
        (3) e_c < p_c && 세로 >= 가로
            좌상단 r = e_r
            좌상단 c = e_c
            우하단 r = e_r + |p_c - e_c|
            우하단 c = p_c
        (4) e_r < p_r && 세로 <= 가로
            좌상단 r = e_r
            좌상단 c = e_c
            우하단 r = p_r
            우하단 c = e_c + |p_r - e_r|    
    '''
    e_r, e_c = eInfo
    minSquareR1 = 20; minSquareC1 = 20
    minSquareR2 = 0; minSquareC2 = 0
    minSquareLen = 20
    for pIdx, part in enumerate(participants):
        p_r, p_c = part

        if alreadyExited(part):
            # participant already exit
            continue

        # print("PART NOT EXITED: ", p_r, p_c)

        width = abs(p_r - e_r)
        height = abs(p_c - e_c)

        r1, c1, r2, c2, slength = getRangeForCase(eInfo, part, height, width)

        if (minSquareLen > slength):
            minSquareLen = slength
            minSquareR1 = r1; minSquareC1 = c1
            minSquareR2 = r2; minSquareC2 = c2
        elif (minSquareLen == slength):
            if (minSquareR1 > r1):
                minSquareR1 = r1; minSquareC1 = c1
                minSquareR2 = r2; minSquareC2 = c2
            elif (minSquareR1 == r1):
                if (minSquareC1 > c1):
                    minSquareR1 = r1; minSquareC1 = c1
                    minSquareR2 = r2; minSquareC2 = c2
    
    return minSquareR1, minSquareC1, minSquareR2, minSquareC2, minSquareLen

def solution(K):
    global partCntExited
    time = 1
    totalMoved = 0
    # print(temp)
    while(time <= K):
        temp = [[-1]*len(maze) for i in range(len(maze))]
        # print("TIME: ", time)
        # print("EXIT: ", exit)
        # 1. 이동
        for pInfo in participants:
            p_r, p_c = pInfo
            if alreadyExited(pInfo):
                # participant already exit
                continue
            np_r, np_c = moveParticipants(pInfo, exit)
            if p_r != np_r or p_c != np_c:
                totalMoved += 1            
            pInfo[0] = np_r; pInfo[1] = np_c

            if checkIfArriveExit(pInfo, exit):
                pInfo[0] = -1; pInfo[1] = -1
        
        if partCntExited == len(participants):
            break
        
        # print("participants")
        # prettyPrint(participants)
        
        # 2.1 미로 선택
        # print("MAZE")
        # prettyPrint(maze)

        r1, c1, r2, c2, squareLen = getRangeToRotate(exit)
        # print("좌상단: ", r1, c1, "/ 우하단: ", r2, c2, "/ 변: ", squareLen)

        # r1 = 1; c1 = 1; r2 = 3; c2 = 3

        # 2.2 미로 회전
        # 다른 곳에 저장
        for r in range(squareLen):
            for c in range(squareLen):
                # 내구도 깎고 회전
                temp[r+r1][c+c1] = maze[squareLen-1-c+r1][r+c1] - 1 if maze[squareLen-1-c+r1][r+c1] > 0 else 0

        # print("TEMP")
        # prettyPrint(temp)
        # 다시 덮어쓰기(실 이동)
        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                maze[r][c] = temp[r][c]

        # 참가자도 회전
        for pInfo in participants:
            if alreadyExited(pInfo):
                # participant already exit
                continue
            p_r, p_c =  pInfo
            if r1 <= p_r <= r2 and c1 <= p_c <= c2:
                # only when in range
                r = p_r - r1; c = p_c - c1
                pInfo[0] = c+ r1; pInfo[1] = squareLen - r - 1 + c1
            # print("참가자 회전: p_r, p_c: ", p_r, p_c, "-> TO:", pInfo)
            
        # 출구도 회전
        e_r, e_c = exit
        r = e_r - r1; c = e_c - c1
        exit[0] = c + r1; exit[1] = squareLen - r - 1 + c1
        
        time += 1

    return totalMoved

N, M, K = [int(i) for i in read().split()]
for i in range(N):
    maze.append([int(i) for i in read().split()])

for i in range(M):
    participants.append([int(i)-1 for i in read().split()])

exit = [int(i)-1 for i in read().split()]

# print(maze)
# print(participants)
# print(exit)

print(solution(K))
print(exit[0]+1, exit[1]+1)