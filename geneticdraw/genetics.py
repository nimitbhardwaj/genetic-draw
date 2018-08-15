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
        self.pCross=1
        self.nGen = nGen
        self.pCross = pCross
        self.pMut = pMut

        self.colMut = 0.6
        self.shapeMut = 0.3
        self.stackMut = 0.1

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
            z = copy.deepcopy(self.population[0])
            z = self.mutate(z)
            if self.cost(self.population[0]) < self.cost(z):
                print(self.cost(self.population[0]))
                return self.population[0]
            else:
                self.population[0] = z
                print(self.cost(z))
                return z

            L = []
            L.append(self.population[0])
            # L.append(self.population[1])
            # for i in range(len(self.population)//3):
            #     L.append(self.population[i])
            while len(self.population) != len(L):
                p1, p2 = self.selection()
                # print(L)
                L.append(self.mutate(self.crossover(p1, p2)))
            self.population = sorted(L, key=self.cost)
            print(list(map(self.cost, self.population)))
            return self.population[0]

    def cost(self, t):
        dummy = Screen(self.w, self.h)
        for tri in t:
            dummy.draw(tri)
        dummy = np.asarray(dummy.getImg().convert('RGB'), dtype='int64')
        # print(dummy.shape)
        x =  sum(sum(sum((dummy-self.baseImg)**2)))
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
        ret = []
        for i in range(len(p1)):
            if np.random.choice([True, False], size=1, p=[self.pCross, 1-self.pCross])[0]:
                ret.append(p2[i])
            else:
                ret.append(p1[i])
        return p1
    
    def mutate(self, p):
        for tri in p:
            if np.random.choice([True, False], size=1, p=[self.pMut, 1-self.pMut])[0]:
                x = np.random.choice([0, 1, 2],size=1,p=[self.colMut, self.shapeMut, self.stackMut])[0]
                critical = np.random.choice([True, False], size=1, p=[self.critical, 1-self.critical])[0]
                # color mutation
                if x == 0:
                    if not critical:
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
                        tri.color = (np.random.randint(0,256), np.random.randint(0,256),
                                np.random.randint(0,256), np.random.randint(0, 256))
                elif x == 1:
                    if not critical:
                        y = np.random.choice([1, 2, 3])
                        if y == 1:
                            tri.p1 = (np.random.randint(0, self.w+1), np.random.randint(0, self.h+1))
                        elif y == 2:
                            tri.p2 = (np.random.randint(0, self.w+1), np.random.randint(0, self.h+1))
                        elif y == 3:
                            tri.p2 = (np.random.randint(0, self.w+1), np.random.randint(0, self.h+1))
                    else:
                        tri.p1 = (np.random.randint(0, self.w+1), np.random.randint(0, self.h+1))
                        tri.p2 = (np.random.randint(0, self.w+1), np.random.randint(0, self.h+1))
                        tri.p3 = (np.random.randint(0, self.w+1), np.random.randint(0, self.h+1))
                elif x == 2:
                    alpha = np.random.randint(0, len(p))
                    beta = np.random.randint(0, len(p))
                    p[alpha], p[beta] = p[beta], p[alpha]

        return p

