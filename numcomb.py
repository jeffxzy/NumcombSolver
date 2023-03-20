import random
import numpy as np
import math

# 依据给定的vars完成一整局
def gameTrain(vars):
    # 初始化
    comb, cardList, lines = init()
    # 放置每张牌
    for cid in range(0, 20):
        id, score = step(comb, lines, vars, cardList[cid])
        comb[id] = cardList[cid]
    # 计算总分
    score = expScore(comb, lines, vars)
    return score



def gamePlay(vars):
    # 初始化
    comb, cardList, lines = init()
    # 放置每张牌
    for cid in range(0, 20):
        num = input("")
        if len(num) == 3:
            cardList[cid] = [int(num[0]), int(num[1]), int(num[2])]
        elif len(num) == 5:
            cardList[cid] = [int(num[0]), int(num[2]), int(num[4])]
        elif len(num) == 6 or len(num) == 8:
            cardList[cid] = [10, 10, 10]
        else:
            print("Wrong Input!")
            return 0
        id, score = step(comb, lines, vars, cardList[cid], 1)
        comb[id] = cardList[cid]
        # 输出本轮放置位置
        print(id)
    
    # 计算总分
    score = expScore(comb, lines, vars)
    print(comb)
    print(score)

    return score


def gameEval(vars):
    # 初始化
    comb, cardList, lines = init()
    # 放置每张牌
    print("输入蜂巢：")
    for i in range(0, 20):
        num = input("")
        if len(num) == 3:
            comb[i] = [int(num[0]), int(num[1]), int(num[2])]
        elif len(num) == 5:
            comb[i] = [int(num[0]), int(num[2]), int(num[4])]
        elif len(num) == 6 or len(num) == 8:
            comb[i] = [10, 10, 10]
        else:
            print("Wrong Input!")
            return 0
    print(comb)
    while True:
        ok = 0
        for i in range(0, 20):
            if comb[i] == [0, 0, 0]:
                num = input("输入当前块：")
                if len(num) == 3:
                    cardList[0] = [int(num[0]), int(num[1]), int(num[2])]
                elif len(num) == 5:
                    cardList[0] = [int(num[0]), int(num[2]), int(num[4])]
                elif len(num) == 6 or len(num) == 8:
                    cardList[0] = [10, 10, 10]
                else:
                    print("Wrong Input!")
                    return
                id, score = step(comb, lines, vars, cardList[0], 1)
                comb[id] = [0, 0, 0]
                # 输入本轮放置位置
                id = int(input("实际放入："))
                if id >= 20 or id < 0:
                    print("Wrong Input!")
                    return
                comb[id] = cardList[0]
                ok = 1
                break
        if ok == 0:
            break
        
    return

def init():

    # 初始化蜂巢图
    comb = []
    for i in range(0, 20):
        comb.append([0, 0, 0])

    # 初始化发牌
    cardList = []
    for times in range(0, 2):
        for i in [3, 4, 8]:
            for j in [1, 5, 9]:
                for k in [2, 6, 7]:
                    cardList.append([i, j, k])
        cardList.append([10, 10, 10])
    ok = 0
    random.shuffle(cardList)
    for i in range(0, 20):
        if cardList[i] == [10, 10, 10]:
            ok = 1
    if ok == 0:
        for i in range(0, 20):
            cardList[i], cardList[i + 20] = cardList[i + 20], cardList[i]

    # 初始化每一“行”。lines中的每个元素意思为：该行长度 该行类别（左上右下 上下 右上左下） 后方是该行经过的格子
    lines = []
    lines.append([3, 0, 8, 13, 17])
    lines.append([4, 0, 4, 9, 14, 18])
    lines.append([5, 0, 1, 5, 10, 15, 19])
    lines.append([4, 0, 2, 6, 11, 16])
    lines.append([3, 0, 3, 7, 12])

    lines.append([3, 1, 1, 2, 3])
    lines.append([4, 1, 4, 5, 6, 7])
    lines.append([5, 1, 8, 9, 10, 11, 12])
    lines.append([4, 1, 13, 14, 15, 16])
    lines.append([3, 1, 17, 18, 19])

    lines.append([3, 2, 1, 4, 8])
    lines.append([4, 2, 2, 5, 9, 13])
    lines.append([5, 2, 3, 6, 10, 14, 17])
    lines.append([4, 2, 7, 11, 15, 18])
    lines.append([3, 2, 12, 16, 19])

    return comb, cardList, lines

# 执行一步蜂巢
def step(comb, lines, vars, now, small = 0, depth = 0):
    exp = []
    for x in range(0, 20):
        # 计算将该块放到每个位置的期望分数
        if comb[x] == [0, 0, 0]:
            comb[x] = now
            # 递归求解。条件：不是最后一块（有后续块且没到最大深度）
            if comb.count([0, 0, 0]) > 1 and depth < 1:
                cases = 0
                scoreSum = 0
                # 对所有还没有出现的方块
                for i in [3, 4, 8]:
                    for j in [1, 5, 9]:
                        for k in [2, 6, 7]:
                            c = comb.count([i, j, k])
                            cases += 2 - c
                            if 2 - c != 0:
                                id, score = step(comb, lines, vars, [i, j, k], depth = depth + 1)
                                scoreSum += score * (2 - c)
                c = comb.count([10, 10, 10])
                for times in range(0, 2 - c):
                    cases += 2 - c
                    if 2 - c != 0:
                        id, score = step(comb, lines, vars, [10, 10, 10], depth = depth + 1)
                        scoreSum += score * (2 - c)
                
                exp.append(scoreSum / cases)
            # 已经超过迭代次数
            else:
                exp.append(expScore(comb, lines, vars))
            
            comb[x] = [0, 0, 0]
        else:
            exp.append(-1)
    # 放到期望分数最大的位置
    # print(exp)
    mx = max(exp)
    for i in range(0, 20):
        if exp[i] == mx:
            break

    z = i

    # 小样本时提供分析数据
    if small == 1:
        # 获取下标从大到小的索引
        sorted_idx = np.argsort(exp)[::-1]
        # 取前三个
        top_3_idx = sorted_idx[:3]
        # 输出前三大的数和下标
        for i, idx in enumerate(top_3_idx):
            print(f"建议位置：{idx} 得分:{(int(exp[idx] * 100)) / 100}")

    return z, mx


# 计算某个局面的最终期望得分
def expScore(comb, lines, vars):

    sum = 0
    # 当前已经放下几块
    blockCount = 0
    for i in range(0, 20):
        if comb[i] != [0, 0, 0]:
            blockCount = blockCount + 1

    lastnum = 0
    lastscore = 0
    selected = [0] * 11
    desired = [0] * 10
    waiting = [0] * 10
    decide = []
    for i in range(0, 20):
        decide.append([0, 0])
    needs = [0] * 10


    # 计算0方块的分数
    if comb[0] == [0, 0, 0]:
        sum = sum + vars[10]
    else:
        sum = sum + (comb[0][0] + comb[0][1] + comb[0][2]) * 1

    # 对于每一行
    for i in range(0, 15):
        status, length, type, score, num, filled = rowStatus(comb, lines[i])
        scale = vars[length - filled]

        sum = sum + scale * score

        # 越后期，已连通的价值越高。
        if status != 'full':
            sum = sum - scale * (1 - math.pow(0.993, blockCount)) * score

        # 尽可能使得游戏开局没有相邻元素，变量var[7]。
        if blockCount < 10:
            if status == 'partial':
                if num == lastnum and num != 0 and num != 10:
                    sum = sum - lastscore * vars[7]
                    sum = sum - math.pow(lastnum / 2, 0.5)
                lastnum = num
                lastscore = scale * score
            else:
                lastnum = 0
                lastscore = 0
        # 尽可能使得游戏开局不破坏行。
        if blockCount < 10:
            if status == 'broken':
                sum = sum - math.pow(num, 0.5)
        # 尽可能使得游戏开局不一次开太多行，变量var[6]。
        if num != 0 and num != 10 and status == 'partial':
            desired[num] = desired[num] + length - filled
            waiting[num] = waiting[num] + scale * score
        # 降低交错点的期望得分，变量var[8], var[9]。
        if status == 'partial':
            for j in range(2, 2 + length):
                if comb[lines[i][j]] == [0, 0, 0]:
                    decide[lines[i][j]][0] = decide[lines[i][j]][0] + 1
                    decide[lines[i][j]][1] = decide[lines[i][j]][1] + scale * score
        # 计算每个数字有多少行
        if num != 0 and num != 10:
            needs[num] = needs[num] + 1

    # 降低多排得分比例
    for i in range(1, 10):
        scale = math.pow(desired[i] * vars[6] / 10, 2)
        if desired[i] < 5 or needs[i] < 3:
            scale = 0
        sum = sum - scale * waiting[i]
    # 降低交点牌得分概率
    scale = math.pow(blockCount / 20, 2)
    times = 0.4
    for i in range(0, 20):
        if comb[i] == [10, 10, 10]:
            times = 1
    scale = scale * times
    for i in range(0, 20):
        if decide[i][0] == 2:
            sum = sum - scale * vars[8] * decide[i][1]
        if decide[i][0] == 3:
            sum = sum - scale * vars[9] * decide[i][1]

    return sum


def rowStatus(comb, line):

    # 该行状态：full partial empty damaged
    status = ''
    # 该行长度
    length = line[0]
    # 该行种类
    type = line[1]
    # 该行已经填了几个
    filled = 0
    # 该行对应的数字
    num = 0
    # 该行得分
    score = 0

    for i in range(2, 2 + length):
        now = comb[line[i]][line[1]]
        if now != 0:
            filled = filled + 1
        if now != 0 and now != 10:
            # 损坏行
            if num != 0 and num != now:
                status = 'broken'
                score = 0
                return status, length, type, score, num, filled
            # 该行数字
            num = now

    # 已经填满的行
    if filled == length:
        status = 'full'
        score = num * length
    # 全空的行
    elif filled == 0:
        status = 'empty'
        score = 10 * length
    # 填满部分的行
    else:
        status = 'partial'
        score = num * length
        if num == 0:
            score = 10 * length
            num = 10

    return status, length, type, score, num, filled