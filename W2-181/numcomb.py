import random
import numpy as np
import math


# 依据给定的vars完成一整局
def gameTrain(vars):
    # 初始化
    comb, cardList, lines = init()
    # 放置每张牌
    for cid in range(0, 20):
        comb, id = step(comb, lines, vars, cardList[cid])
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
            now = [int(num[0]), int(num[1]), int(num[2])]
        elif len(num) == 5:
            now = [int(num[0]), int(num[2]), int(num[4])]
        elif len(num) == 6 or len(num) == 8:
            now = [10, 10, 10]
        else:
            print("Wrong Input!")
            return 0
        comb, id, advice = step(comb, lines, vars, now, 1)
        print(advice)
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
                comb, id, advice = step(comb, lines, vars, cardList[0], 1)
                print(advice)
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


def gameBot(comb, vars, now):
    combNotUsed, cardList, lines = init()
    comb, id, advice = step(comb, lines, vars, now, 1)
    return id, advice


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
        random.shuffle(cardList)

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
def step(comb, lines, vars, now, advice=0):
    finScore = []
    vals = []
    for i in range(0, 20):
        # 计算将该块放到每个位置的期望分数
        if comb[i] == [0, 0, 0]:
            comb[i] = now

            exp = expScore(comb, lines, vars)
            conf = confAnalysis(comb, lines, vars)
            scar = scarAnalysis(comb, lines, vars)

            comb[i] = [0, 0, 0]
        else:
            exp = -1
            scar = 1
            conf = 1
        fins = exp * conf * scar
        vals.append([exp, conf, scar, fins])
        finScore.append(fins)
    # 放到期望分数最大的位置
    mx = max(finScore)
    for i in range(0, 20):
        if finScore[i] == mx:
            break
    comb[i] = now
    z = i
    # 小样本时提供分析数据
    if advice == 1:
        info = []
        # 获取下标从大到小的索引
        sorted_idx = np.argsort(finScore)[::-1]
        # 取前三个
        top_3_idx = sorted_idx[:3]
        # 输出前三大的数和下标
        for i, idx in enumerate(top_3_idx):
            info.append([idx, vals[idx]])
            print(vals[idx])
        adviceR = getAdvice(info)
        return comb, z, adviceR

    return comb, z


def getAdvice(info):
    advice = ''
    n = []
    v = []
    for i in range(0, 3):
        n.append(str(info[i][0]))
        v.append(info[i][1])
    for i in range(0, 3):
        advice += '建议：' + n[i]
        if int(n[i]) < 10:
            advice += '  '
        advice += ' 期望:' + str(int(v[i][3] * 100) / 100) + '\n'
    advice += '\n'
    if v[0][0] >= v[1][0] - 0.001 and v[0][1] >= v[1][1] - 0.001 and v[0][2] >= v[1][2] - 0.001:
        if v[0][3] > v[1][3] + 5:
            advice += '显然， ' + n[0] + ' 是最好的选择。'
        elif v[0][3] > v[1][3] + 2:
            advice += n[0] + ' 比起 ' + n[1] + ' 要更好。'
        elif v[0][3] > v[1][3] + 0.5:
            advice += n[0] + ' 和 ' + n[1] + ' 都是很好的选择，可能 ' + n[0] + ' 略好一点点。'
        else:
            advice += n[0] + ' 和 ' + n[1] + ' 都是很好的选择。'
    else:
        if v[0][0] < v[1][0]:
            advice += '虽然 ' + n[0] + ' 的 期望分数 不如 ' + n[1] + ' ，'
        elif v[0][1] < v[1][1]:
            advice += '虽然 ' + n[0] + ' 的 构型 不如 ' + n[1] + ' 更合理，'
        elif v[0][2] < v[1][2]:
            advice += '虽然 ' + n[0] + ' 的 交点数量 比 ' + n[1] + ' 多，'
        else:
            advice += '虽然 ' + n[0] + ' 与 ' + n[1] + ' 相比不是完美的，'
        if v[0][0] > v[1][0]:
            advice += '但是 ' + n[0] + ' 的 期望分数 要更高。'
        elif v[0][1] > v[1][1]:
            advice += '但是 ' + n[0] + ' 的 构型 更合理。'
        elif v[0][2] > v[1][2]:
            advice += '但是 ' + n[0] + ' 的 交点数量 要更少。'
        else:
            advice += '但是 ' + n[0] + ' 的综合分数更高。'
    return advice



# 获得某局面所有行的数据
def getLineInfo(comb, lines, vars):
    lineInfo = []
    for i in range(0, 15):
        status, length, type, score, num, filled = lineStatus(comb, lines[i])
        lineInfo.append({
            'status': status,
            'length': length,
            'type': type,
            'score': score,
            'scale': vars[length - filled],
            'finalScore': vars[length - filled] * score,
            'num': num,
            'filled': filled,
            'need': length - filled,
        })
    return lineInfo


# 计算某个局面的最终期望得分
def expScore(comb, lines, vars):
    sum = 0
    # 计算0方块的分数
    if comb[0] == [0, 0, 0]:
        sum = sum + 18
    else:
        sum = sum + (comb[0][0] + comb[0][1] + comb[0][2]) * 1

    lineInfo = getLineInfo(comb, lines, vars)
    for i in range(0, 15):
        sum = sum + lineInfo[i]['finalScore']

    return sum

# 构型分析
def confAnalysis(comb, lines, vars):
    blockCount = 0
    for i in range(0, 20):
        if comb[i] != [0, 0, 0]:
            blockCount = blockCount + 1

    lineInfo = getLineInfo(comb, lines, vars)

    numCount = [0] * 11

    badness = 0

    for i in range(0, 15):
        if lineInfo[i]['status'] == 'broken':
            badness += vars[6]

    for i in range(0, 15):
        if lineInfo[i]['status'] == 'partial':
            numCount[lineInfo[i]['num']] = numCount[lineInfo[i]['num']] + 1
    for i in range(1, 10):
        if numCount[i] == 3:
            badness += vars[7]
        if numCount[i] == 4:
            badness += vars[8]

    goodness = 1 - math.pow(badness, (1 + blockCount / 20))
    if goodness < 0:
        goodness = 0

    return goodness



# 交点惩罚
def scarAnalysis(comb, lines, vars):
    lineInfo = getLineInfo(comb, lines, vars)
    blockExpect = []
    for i in range(0, 20):
        blockExpect.append([0, 0, 0])

    for i in range(0, 15):
        if lineInfo[i]['status'] == 'partial' and lineInfo[i]['num'] != 0 and lineInfo[i]['num'] != 10:
            for j in range(2, 2 + lineInfo[i]['length']):
                blockExpect[lines[i][j]][lineInfo[i]['type']] = lineInfo[i]['num']
    for i in range(0, 20):
        if comb[i] != [0, 0, 0]:
            blockExpect[i] = [0, 0, 0]
        for j in range(0, 3):
            if blockExpect[i][j] == 0:
                blockExpect[i][j] = -i
    same = [0, 0, 0, 0]
    for i in range(0, 20):
        for j in range(0, 20):
            if i != j:
                ns = 0
                for k in range(0, 3):
                    if blockExpect[i][k] == blockExpect[j][k]:
                        ns = ns + 1
                same[ns] = same[ns] + 1
    score = 1 - 0.0002 * same[1] - vars[9] * same[2] - vars[10] * same[3]
    if score < 0:
        score = 0
    return score



def lineStatus(comb, line):
    # 该行状态：full partial empty broken
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