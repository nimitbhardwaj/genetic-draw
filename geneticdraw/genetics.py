from triangle import Triangle
from screen import Screen
import numpy as np
import copy

NTRI=50

class Genetic(object):
    def __init__(self, baseImg, nPopulation, nGen, pCross, pMut):
        self.baseImg = np.asarray(baseImg, dtype='int64')
        # print(self.baseImg.shape)
        self.nPop = nPopulation
        self.nGen = nGen
        self.pCross = pCross
        # self.pMut = pMut
        self.pMut = pMut

        self.colMut = 0.4
        self.shapeMut = 0.4
        self.stackMut = 0.2

        self.critical = 0.1
        self.w, self.h = baseImg.size

        self.counter = 0
        self.population = []

    def __iter__(self):
        return self
    
    def __next__(self):

        if self.counter > self.nGen:
            self.counter = 0
            raise StopIteration
        elif self.counter == 0:
            self.population = [[Triangle.getRandomTriangle(self.w, self.h) for i in range(NTRI)] for j in range(self.nPop)]
            self.population = sorted(self.population, key=self.cost)
            self.counter += 1
            return self.population[0]
        else:
            self.counter += 1
            # par = copy.deepcopy(self.population[0])
            # son = self.mutate(copy.deepcopy(par))
            # c1 = self.cost(par)
            # c2 = self.cost(son)
            # if c1 > c2:
            #     print(c2)
            #     self.population[0] = son
            #     return son
            # else:
            #     print(c1)
            #     return par
            L = []
            L.append(self.population[0])
            # L.append(self.population[1])
            # for i in range(len(self.population)//3):
            #     L.append(self.population[i])
            while len(L) < len(self.population):
                # print("hello")
                p1, p2 = self.selection()
                p1 = copy.deepcopy(p1)
                p2 = copy.deepcopy(p2)
                # print(L)
                p1 = self.crossover(p1, p2)
                # print("hello")
                L.append(self.mutate(p1))
                # L.append(self.mutate(self.crossover(p1, p2)))
            costPop = list(map(self.cost, L))
            # self.population = sorted(L, key=self.cost)
            self.population = [x for _, x in sorted(zip(costPop, L), key=lambda kapa: kapa[0])]
            # Z = [x for _,x in sorted(zip(Y,X))]
            while len(self.population) != self.nPop:
                self.population.pop()
            print(sorted(costPop))
            return self.population[0]

    def cost(self, t):
        dummy = Screen(self.w, self.h)
        for tri in sorted(t, key=lambda x: x.h):
            dummy.draw(tri)
        dummy = np.asarray(dummy.getImg().convert('RGB'), dtype='int64')
        # print(dummy.shape)
        x =  sum(sum(sum(abs(dummy-self.baseImg))))
        return x
        # delta = 0
        # for x in range(self.h-1):
        #     for y in range(self.w-1):
        #         delta += abs(dummy[x][y][0] - self.baseImg[x][y][0]) + abs(dummy[x][y][1] - self.baseImg[x][y][1]) + abs(dummy[x][y][2] - self.baseImg[x][y][2])
        # return delta

    
    def selection(self):
        L = self.population
        prob = np.array([i for i in range(len(L), 0, -1)])
        prob = prob/sum(prob)
        x = np.random.choice(list(range(len(L))), size=2, p=prob)
        return L[x[0]], L[x[1]]

    def crossover(self, p1, p2):
        # return p1
        ret = []
        for i in range(len(p1)):
            if np.random.choice([True, False], size=1, p=[self.pCross, 1-self.pCross])[0]:
                t1 = p1[i]
                t2 = p2[i]
                x = np.random.choice([0, 1])
                if x == 0:
                    if np.random.choice([True, False]):
                        t1.color = list(t1.color)
                        t2.color = list(t2.color)
                        t1.color[0], t2.color[0] = t2.color[0], t1.color[0]
                        t1.color = tuple(t1.color)
                        t2.color = tuple(t2.color)
                    if np.random.choice([True, False]):
                        t1.color = list(t1.color)
                        t2.color = list(t2.color)
                        t1.color[1], t2.color[1] = t2.color[1], t1.color[1]
                        t1.color = tuple(t1.color)
                        t2.color = tuple(t2.color)
                    if np.random.choice([True, False]):
                        t1.color = list(t1.color)
                        t2.color = list(t2.color)
                        t1.color[2], t2.color[2] = t2.color[2], t1.color[2]
                        t1.color = tuple(t1.color)
                        t2.color = tuple(t2.color)
                    if np.random.choice([True, False]):
                        t1.color = list(t1.color)
                        t2.color = list(t2.color)
                        t1.color[3], t2.color[3] = t2.color[3], t1.color[3]
                        t1.color = tuple(t1.color)
                        t2.color = tuple(t2.color)
                else:
                    if np.random.choice([True, False]):
                        t1.p1, t2.p1 = t2.p1, t1.p1
                    if np.random.choice([True, False]):
                        t1.p2, t2.p2 = t2.p2, t1.p2
                    if np.random.choice([True, False]):
                        t1.p3, t2.p3 = t2.p3, t1.p3

                ret.append(t1)
            else:
                ret.append(p1[i])
        # print(ret, ret2)
        return ret
    
    def mutate(self, p):
        tri = p[np.random.randint(0, len(p))]
        if not np.random.choice([True, False], size=1, p=[self.pMut, 1-self.pMut])[0]:
            return p

        x = np.random.choice([0, 1, 2],size=1,p=[self.colMut, self.shapeMut, self.stackMut])[0]
        critical = np.random.choice([True, False], size=1, p=[self.critical, 1-self.critical])[0]
        # color mutation
        if x == 0:
            if  critical:
                y = np.random.choice(['R', 'G', 'B', 'A'])
                col = tri.color
                if y == 'R':
                    tri.color = (np.random.randint(0, 256), col[1], col[2], col[3])
                elif y == 'G':
                    tri.color = (col[0], np.random.randint(0, 256), col[2], col[3])
                elif y == 'B':
                    tri.color = (col[0], col[1], np.random.randint(0, 256), col[3])
                elif y == 'A':
                    tri.color = (col[0], col[1], col[2], np.random.randint(0, 256))
            else:
                y = np.random.choice(['R', 'G', 'B', 'A'])
                col = tri.color
                zeta = np.random.randint(0, 10)
                if y == 'R':
                    tri.color = ((col[0]+zeta)%256, col[1], col[2], col[3])
                elif y == 'G':
                    tri.color = (col[0], (col[1]+zeta)%256, col[2], col[3])
                elif y == 'B':
                    tri.color = (col[0], col[1], (col[2]+zeta)%256, col[3])
                elif y == 'A':
                    tri.color = (col[0], col[1], col[2], (col[3]+zeta)%256)

        elif x == 1:
            if critical:
                y = np.random.choice([1, 2, 3])
                if y == 1:
                    tri.p1 = (np.random.randint(0, self.w+1), np.random.randint(0, self.h+1))
                elif y == 2:
                    tri.p2 = (np.random.randint(0, self.w+1), np.random.randint(0, self.h+1))
                elif y == 3:
                    tri.p2 = (np.random.randint(0, self.w+1), np.random.randint(0, self.h+1))
            else:
                zeta = int(np.random.random() * self.w)
                peta = int(np.random.random() * self.h)
                y = np.random.choice([1, 2, 3])
                if y == 1:
                    tri.p1 = ((tri.p1[0]+zeta)%self.w, (tri.p1[1]+peta)%self.h)
                elif y == 2:
                    tri.p2 = ((tri.p2[0]+zeta)%self.w, (tri.p2[1]+peta)%self.h)
                elif y == 3:
                    tri.p3 = ((tri.p3[0]+zeta)%self.w, (tri.p3[1]+peta)%self.h)
        elif x == 2:
            alpha = np.random.randint(0, len(p))
            beta = np.random.randint(0, len(p))
            p[alpha].h, p[beta].h = p[beta].h, p[alpha].h

        return p

