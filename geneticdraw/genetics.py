from triangle import Triangle
from screen import Screen
import numpy as np

NTRI=25

class Genetic(object):
    def __init__(self, baseImg, nPopulation, nGen, pCross, pMut):
        self.baseImg = np.asarray(baseImg)
        self.nPop = nPopulation
        self.nGen = nGen
        self.pCross = pCross
        self.pMut = pMut
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
            L = []
            for i in range(len(self.population)//3):
                L.append(self.population[i])
            while len(self.population) != len(L):
                p1 = self.selection()
                p1 = self.selection()
                L.append(self.mutate(self.crossover(p1, p2)))
            self.population = sorted(L, key=self.cost)
            return self.population[0]

    def cost(self, t):
        dummmy = Screen(self.w, self.h)
        for tri in t:
            dummy.draw(tri)
        dummy = np.asarray(dummy.getImg().convert('RGB'))
        delta = 0
        for x in range(self.w):
            for y in range(self.h):
                delta += abs(dummy[x, y] - self.baseImg[x, y])
        return delta

    
    def selection(self, L):
        pass

    def crossover(self, p1, p2):
        pass
    
    def mutate(self, p):
        pass
