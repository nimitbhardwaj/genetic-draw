from triangle import Triangle
from screen import Screen
from PIL import Image

import genetics
import os
import sys



class Main():
    def main(self, baseImg, nPopulation=10, nGen=1000, pCross=0.4, pMut=0.1):
        baseImg = Image.open(baseImg).convert('RGB')
        baseImg.show()
        w, h = baseImg.size
        # t = [Triangle.getRandomTriangle(w, h) for i in range(25)]
        # for x in t:
        #     scr.draw(x)
        # scr.show()
        # return
        k = 0
        for topper in genetics.Genetic(baseImg, nPopulation, nGen, pCross, pMut):
            print(k)
            scr = Screen(w, h)
            for tri in sorted(topper, key=lambda x: x.h):
                scr.draw(tri)
            # if k % 100 == 0:
            #     scr.show()
            scr.store(str(os.path.join('.', 'out', '{num:05d}.png').format(num=k)))
            k += 1

if __name__ == '__main__':
    Main().main(str(os.path.join('.','images', sys.argv[1]+'.png')), nGen=100000, nPopulation=10, pMut=0.3)
