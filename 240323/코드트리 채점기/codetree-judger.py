'''
1. 대기 큐에 삽입(각 task)
    단, 채점 대기 큐에 있는 task 중 정확히 u와 일치하는 url이 단 하나라도 존재한다면 큐에 추가하지 않고 넘어갑니다.
2. 대기 큐에 채점 시도
    [채점 가능한 조건]
    도메인/문제ID 형태 중 도메인 일치하는 게 채점 진행 중인 경우 불가
        DICT[도메인].(start + gap) < t인 경우에만 채점 큐 ㄱ 
    새 task 현재 시간 t가 가장 최근 task start+3*gap 보다 작다면, 불가
        t <= DICT[도메인].start + 3 * DICT[도메인].gap인 경우에만 채점 큐 ㄱ
    -> DICT[도메인] = (start, gap) 로 관리

    <<t초일 때>>
    if 해당하는 command 있으면

        if command = 채점 요청 (200)
            대기큐.push(우선순위 p, 요청시간 t, url u)

        if command = 채점 시도 (300)
            if 쉬고 있는 채점기 o,
                if 대기큐에 task 있음
                    **대기큐에서 [채점 가능한 조건] 만족하는 task 모으기**
                        여기서> 일단 뽑고 채점 가능한 지 확인, 불가하면 모아놓고, 가능하면 pop, 불가한 애들 다시 다 집어넣어주기
                        **시간 계산해야 함: 다른 연산 덜 걸리는 방법?**
                    sort 채점 우선순위, 대기 큐에 들어온 시간 (오름차순)
                    대기큐.pop(위 sort된 것에서 1위)
                    채점기 찾고 push
                    DICT[도메인].start 업데이트

        if command = 채점 종료 (400)
            채점기에서 task 빼기
            DICT[도메인].gap 업데이트(start랑 비교)


    t = t + 1

'''

import sys; sysRead = sys.stdin.readline
import heapq
from collections import defaultdict

MAX_TIME = 1000000

graderList = [] # starts with idx=1
countGrader = 0

domainDict = defaultdict(lambda: [-1,-1]) # 도메인: 가장 최신의 태스크 정보로 업데이트
candDomainDict = defaultdict(int) # domain: probId: startTime if 현재 진행 중인 태스크 (중복?)
urlInHeap = defaultdict(int)

class Node:
    # 우선순위큐 노드, lt 더 작성해도 좋을 듯
    def __init__(self, priority, requestTime, domain, probId):
        self.priority = priority
        self.requestTime = requestTime
        self.domain = domain
        self.probId = probId

    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        elif self.priority == other.priority:
            if self.requestTime < other.requestTime:
                return True
        else:
            return False


def prepare(heap, prepareCommand):
    global graderList, countGrader
    # when case == 100
    N = int(prepareCommand[1])
    graderList = [-1] + [None] * N
    countGrader = N
    u = prepareCommand[2]
    domain, probId = u.split('/')
    probId = int(probId)
    heapq.heappush(heap, Node(1,0, domain, probId))
    urlInHeap[u] += 1
    candDomainDict[domain] = -1


def isValid(node, curTime):
    '''
    [채점 가능한 조건]
    
    도메인/문제ID 형태 중 도메인 일치하는 게 채점 진행 중인 경우 불가
        -> TODO: 추가로 찾아야 함
    새 task 현재 시간 t가 가장 최근 task start+3*gap 보다 작다면, 불가
        t >= DICT[도메인].start + 3 * DICT[도메인].gap인 경우에만 채점 큐 ㄱ
    -> DICT[도메인] = (start, gap) 로 관리
    '''
    nodeStart = domainDict[node.domain][0]
    nodeGap = domainDict[node.domain][1]

    # 현재 진행 중이 아닌 도메인이어야 함

    if candDomainDict[node.domain] == -1 and curTime > nodeStart + 3 * nodeGap:
        return True
    
    return False

def findGrader():
    for i, grader in enumerate(graderList):
        if i != 0 and not grader:
            return i
    return -1


def printCurStatus(case, curTime, urlInHeap, heap):
    print("===============")
    print("case: ", case)
    print("current time: ", curTime)
    print("urlInHeap: ", urlInHeap)
    print("heap::")
    for i in heap:
        print("p:",  i.priority, "/ time: ",  i.requestTime, "/ url: ", i.domain + str(i.probId))

    print("Grader::")
    for gi, gv in enumerate(graderList):
        if gv and gi != 0:
            print("grader"+str(gi) + ": ", "p(" + str(gv.priority) + "), " + "t(" + str(gv.requestTime) + ")")
        else:
            print("grader"+str(gi) + ": None")

    print("domainDict::")
    print(domainDict)
    print("candDomainDict::")
    print(candDomainDict)
    print("===============")

def solution(commandList):
    global countGrader
    curTime = 0
    heap = [] # 대기 큐
    prepare(heap, commandList[0]) # curCommandId = 0에 대해 처리
    curCommandId = 1
    
    while(curTime <= MAX_TIME and curCommandId < len(commandList)):
        if curTime == int(commandList[curCommandId][1]):
            command = commandList[curCommandId]
            case = int(command[0]) # 200 300 400
            
            if case == 200:
                # 채점 요청
                t, p, u = command[1:]
                domain, probId = u.split('/')
                t = int(t); p = int(p); probId = int(probId)
                if (urlInHeap[u] == 0):
                    # 단, 채점 대기 큐에 있는 task 중 정확히 u와 일치하는 url이 단 하나라도 존재한다면 큐에 추가하지 않고 넘어갑니다.
                    heapq.heappush(heap, Node(p, t, domain, probId))
                    urlInHeap[u] += 1
            
            elif case == 300:
                # 채점 시도
                if countGrader != 0 and len(heap) != 0:
                    # 채점 가능한 애들만 모으기
                    failNodeList = []
                    while(True):
                        node = heapq.heappop(heap)
                        if (isValid(node, curTime)):
                            # 유효한 node 찾음, 채점 가능!
                            countGrader -= 1
                            graderIdx = findGrader()
                            if graderIdx != -1:
                                graderList[graderIdx] = node
                            # DICT[도메인].start 위해 업데이트
                            candDomainDict[node.domain] = curTime
                            urlInHeap[node.domain+'/'+str(node.probId)] -= 1
                            break
                        
                        failNodeList.append(node)
                        if (len(heap) == 0):
                            break

                    for node in failNodeList:
                        # 실패한 애들은 다 도로 넣기
                        heapq.heappush(heap, node)

                
            elif case == 400:
                # 채점 종료
                countGrader += 1
                graderIdx = int(command[2])
                graderList[graderIdx] = None
                # DICT[도메인] 업데이트
                start = candDomainDict[node.domain]
                domainDict[node.domain] = [start, curTime - start]
                candDomainDict[node.domain] = -1
                    # candDomainDict 현재 진행 중인 태스크 아닌 경우 -1 저장하기

            else:
                # when case == 500
                print(len(heap))
            
            # printCurStatus(case, curTime, urlInHeap, heap)


            curCommandId += 1

        curTime += 1
    

Q = int(sysRead().strip())
commandList = [sysRead().strip().split(" ") for i in range(Q)]
solution(commandList)