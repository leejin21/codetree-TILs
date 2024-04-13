'''
<<코드트리 빵>>

t분일 때

1. 사람 이동 (격자에 사람 있을 경우만)

방식) 최단 거리를 모두가, 매 턴마다 찾아서 1칸씩만 가야 함(bfs)
사람.r, 사람.c 갱신

유의1) 이동 중인 사람 격자는 중복 가능
유의2) 제한구역 고려(이미 사람이 들렀던 편의점, 베이스캠프) 구역.restricted로 찾기
유의3) 편의점에 도착했다면 
    1) 해당 편의점은 다음 턴부터 제한 구역으로 설정. 구역.willberestricted = True
    2) 해당 사람은 앞으로 움직이지 않음. 사람.stop = True

2. 베이스캠프로 사람 데려오기

방식) t분에 t번째 사람 알맞는 베이스 캠프로 데려오기(bfs)

사람.r, 사람.c 갱신

유의1) t<=M인 경우에만 해당
유의2) 제한된 베이스캠프 고려에서 제외 if 구역.restricted == True: 제외.
유의3) 제한 구역 설정. 구역.restricted = True

3. 유의3) 도착한 편의점들 찾고: 제한 구역으로 설정
1) 구역.willberestricted = True인 경우 구역.restricted = True

4. 종료조건
모든 편의점에 도달한 경우

'''

from collections import deque

MAX_NUM = 15*15 + 100

areaTypeDict = {"EMPTY": 0, "BASECAMP": 1, "STORE": 2}
baseCampList = []
storeList = []
personList = []

# ↑, ←, →, ↓ 의 우선 순위
drList = [-1, 0, 0, 1]
dcList = [0, -1, 1, 0]

restrictedStoreCnt = 0

class Area:
    def __init__(self, row, col, areaType):
        self.empty = True
        self.row = row
        self.col = col
        self.areaType = areaType # EMPTY = 0 | BASECAMP = 1 | STORE = 2
        self.willBeRestricted = False
        self.restricted = False
        self.cnt = MAX_NUM
        self.startedWay = -1 # -1: init, 0: ↑, 1: ←, 2: →, 3: ↓

class Person:
    def __init__(self, num, storeNum):
        self.row = -1
        self.col = -1
        self.stop = False
        self.num = num # 0 is personList(0)
        self.storeNum = storeNum # 0 is storeList[0]

def prettyPrintMap():
    print("\n===print map===")
    print("0: empty, 1: basecamp, 2: store, 3: willBeRestricted, 4: restricted")
    for r in range(len(mapList)):
        for c in range(len(mapList[r])):
            area = mapList[r][c]
            if area.restricted:
                print(4, end = " ")
            elif area.willBeRestricted:
                print(3, end = " ")
            else:
                print(area.areaType, end = " ")

        print("")

def prettyPrintPeople():
    print("\n===print people===")
    for pnum in range(len(personList)):
        person = personList[pnum]
        print(pnum, ": (r,c) = ", person.row, person.col, end = ", ")
        print("// stopped: ", person.stop)

def findWayForMinimumPath(startArea, arriveArea):
    startedWay = -1 # 0: ↑, 1: ←, 2: →, 3: ↓
    
    q = deque()
    q.append(startArea)
    tempCount = 0
    initCntMap()
    startArea.cnt = 0

    while(len(q) > 0):
        area = q.popleft()
        cur_r = area.row; cur_c = area.col

        if (area == arriveArea):
            tempCount = area.cnt
            break

        for way, v in enumerate(zip(drList, dcList)):
            dr, dc = v
            next_r = cur_r + dr
            next_c = cur_c + dc
                
            if (next_r < 0 or next_r > N-1):
                continue
            if (next_c < 0 or next_c > N-1):
                continue
                
            nextArea = mapList[next_r][next_c]
            if nextArea.cnt > area.cnt + 1:
                nextArea.cnt = area.cnt + 1

                if area == startArea:
                    nextArea.startedWay = way
                else: 
                    nextArea.startedWay = area.startedWay
                q.append(nextArea)

    return arriveArea.startedWay

def movePeople():
    '''
    1. 사람 이동 (격자에 사람 있을 경우만)

    방식) 최단 거리를 모두가, 매 턴마다 찾아서 1칸씩만 가야 함(bfs)
    ↑, ←, →, ↓ 의 우선 순위
    1칸을 어떻게 기억? =>  bfs 할 때 출발의 dr, dc를 매번 기억하도록

    사람.r, 사람.c 갱신

    유의1) 이동 중인 사람 격자는 중복 가능
    유의2) 제한구역 고려(이미 사람이 들렀던 편의점, 베이스캠프) 구역.restricted로 찾기
    유의3) 편의점에 도착했다면 
        1) 해당 편의점은 다음 턴부터 제한 구역으로 설정. 구역.willberestricted = True
        2) 해당 사람은 앞으로 움직이지 않음. 사람.stop = True, 
    '''
    # print("move people")
    for person in personList:
        if person.stop:
            continue
        if person.row == -1 and person.col == -1:
            # not in mapList yet
            continue
        
        startArea = mapList[person.row][person.col]
        store = storeList[person.storeNum]
        startedWay = findWayForMinimumPath(startArea, store)
        dr = drList[startedWay]; dc = dcList[startedWay]

        person.row += dr
        person.col += dc

        # print("person: ", person.row, person.col, "store: ", store.row, store.col)

        if person.row == store.row and person.col == store.col:
            store.willBeRestricted = True
            person.stop = True

    initCntMap()
        
def initCntMap():
    for r in range(N):
        for c in range(N):
            mapList[r][c].cnt = MAX_NUM
            mapList[r][c].cnt = MAX_NUM

def findMinimumPathCnt(startArea, arriveArea):
    q = deque()
    q.append(startArea)
    tempCount = 0
    startArea.cnt = 0

    while(len(q) > 0):
        area = q.popleft()
        cur_r = area.row; cur_c = area.col

        if (area == arriveArea):
            tempCount = area.cnt
            break

        for dr, dc in zip(drList, dcList):
            next_r = cur_r + dr
            next_c = cur_c + dc
                
            if (next_r < 0 or next_r > N-1):
                continue
            if (next_c < 0 or next_c > N-1):
                continue
                
            nextArea = mapList[next_r][next_c]
            if nextArea.cnt > area.cnt + 1:
                nextArea.cnt = area.cnt + 1
                q.append(nextArea)

    return tempCount

def findRightBaseCamp(store):
    # person -> store에 도달할 수 있는 최단거리에 위차한 basecamp 찾기
    minCount = N * N + 100
    rightBaseCamp = None

    for basecamp in baseCampList:
        
        if basecamp.restricted:
            continue

        initCntMap()

        tempCount = findMinimumPathCnt(basecamp, store)

        # 베이스캠프 선택
        if (minCount > tempCount):
            minCount = tempCount
            rightBaseCamp = basecamp
        elif (minCount == tempCount):
            # 행이 작은 베이스캠프, 행이 같다면 열이 작은 베이스 캠프로 들어갑니다.
            if (basecamp.row < rightBaseCamp.row):
                minCount = tempCount
                rightBaseCamp = basecamp
            elif (basecamp.row == rightBaseCamp.row):
                if (basecamp.col < basecamp.col):
                    minCount = tempCount
                    rightBaseCamp = basecamp
    
    initCntMap()    
    return rightBaseCamp

def startInBaseCamp(turn):
    '''
    2. 베이스캠프로 사람 데려오기

    방식) t분에 t번째 사람 알맞는 베이스 캠프로 데려오기(bfs)

    사람.r, 사람.c 갱신

    유의1) t<=M인 경우에만 해당
    유의2) 제한된 베이스캠프 고려에서 제외 if 구역.restricted == True: 제외.
    유의3) 제한 구역 설정. 구역.restricted = True
    '''

    if (turn >= len(personList)):
        return

    starter = personList[turn]
    store = storeList[turn]

    rightBaseCamp = findRightBaseCamp(store)

    starter.row = rightBaseCamp.row
    starter.col = rightBaseCamp.col
    rightBaseCamp.willBeRestricted = True
    
    # 알맞는 베이스 캠프 찾기

def setToRestrictedArea():
    global restrictedStoreCnt
    '''
    3. 유의3) 도착한 편의점들 찾고: 제한 구역으로 설정
    1) 구역.willBeRestricted = True인 경우 구역.restricted = True
    '''
    for basecamp in baseCampList:
        if basecamp.willBeRestricted:
            basecamp.willBeRestricted = False
            basecamp.restricted = True
    
    for store in storeList:
        if store.willBeRestricted:
            store.willBeRestricted = False
            store.restricted = True
            restrictedStoreCnt += 1
    
def solution():
    global restrictedStoreCnt
    # TODO: TURN 개념 도입 (turn = 0 ~ ) -> 결과: turn + 1로 출력
    turn = 0
    # prettyPrintMap()

    while(True):
        # print("\nturn: ", turn)
        
        # 1. 이동
        # print("1. 이동\n")
        movePeople()
        # prettyPrintMap()
        # prettyPrintPeople()

        # 2. 베이스캠프로 사람 데려오기
        # print("\n2. 베이스캠프로 사람 데려오기\n")
        startInBaseCamp(turn)
        # prettyPrintPeople()

        # 3. 제한구역 설정
        # print("\n3. 제한구역 설정\n")
        setToRestrictedArea()
        # prettyPrintMap()
        # prettyPrintPeople()
    
        if (restrictedStoreCnt == len(storeList)):
            break

        turn += 1

    print(turn+1)
    

N, M = [int(i) for i in input().split()]
mapList = []
for i in range(N):
    mapList.append([Area(i, j, int(v)) for j, v in enumerate(input().split())])

# init store
for m in range(M):
    store_r, store_c = [int(i) for i in input().split()]
    personList.append(Person(m, m))
    storeArea = mapList[store_r-1][store_c-1]
    storeArea.areaType = areaTypeDict["STORE"]
    storeList.append(storeArea)

# init basecamp
for r in range(len(mapList)):
    for c in range(len(mapList[r])):
        if mapList[r][c].areaType == areaTypeDict["BASECAMP"]:
            basecamp = mapList[r][c]
            baseCampList.append(basecamp)

solution()