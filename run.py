from scipy.optimize import minimize
import numcomb
import numpy as np
import copy
import math

def f(x, times = 1000):
    score = 0
    for i in range(0, times):
        score = score + numcomb.gameTrain(x)
        if (i + 1) % 1 == 0:
            print('Trained finished for ' + str(i + 1) + ' tests: avescore = ', score / (i + 1))
    print('\n--------------------\nTrained finished for ' + str(times) + ' tests: avescore = ', score/times, '\n')
    return score/times


def print_x0(x):
    print("x0:", x)


def main():

    while True:
        type = input("input: train / bf / test / eval / play / quit\n")

        # x0 = np.array([1.00, 0.65, 0.30, 0.10, 0.07, 0.03])
        x0 = np.array([1.00, 0.721, 0.3993, 0.1947, 0.069, 0.0312,
                       0.75, 0.03, 0.08465, 0.08164, 18])
        # x0: [1, 0.66068835, 0.30203273, 0.100673, 0.07100848, 0.03095212]

        if type == 'train':
            bounds = [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)]

            res = minimize(lambda vars: -f(vars),
                           x0,
                           method='Nelder-Mead',
                           bounds=bounds,
                           callback=print_x0,
                           options={'xatol': 1e-3, 'fatol': 1e-3})
            print("Optimized values: ", res.x)
            print("Optimized result: ", -res.fun) # res.fun is the negative of the optimized result

        elif type == 'bf':
            tt = int(input('input times:'))
            if tt <= 0:
                print('Wrong times input')
                return
            best, bestx0 = 0, []
            for item in range(0, 100):
                for times in range(1, 3):
                    for i in range(10, 11):
                        best = 0
                        now = x0[i]
                        step = now
                        for j in range(0, times):
                            step = step / 10
                        for j in range(-2, 3):
                            x0[i] = now + j * step
                            score = f(x0, tt)
                            # print(score, ' --> ', x0)
                            if score > best:
                                best, bestx0 = score, copy.deepcopy(x0)
                                # print('Update New Best!')
                            # print(x0)
                        print('\nOK remember best update:',best, ' --> ', bestx0)
                        x0 = copy.deepcopy(bestx0)

        elif type == 'test':
            times = int(input('input times:'))
            if times <= 0:
                print('Wrong times input')
                return
            f(x0, times)
        elif type == 'eval':
            numcomb.gameEval(x0)
        elif type == 'play':
            numcomb.gamePlay(x0)
        elif type =='quit':
            return



if __name__ == '__main__':
    main()