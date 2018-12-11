import random

class Triangle(object):
    def __init__(self, p1, p2, p3, col, h):
        '''
        p1, p2, p3: The 2-D tuples denoting the position of three points of 
                    triangle in the image.
        col: A 4-D tuple, denoting the color of triangle, in the form
             (R, G, B, Alpha)
        '''
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.color = col
        self.h = h

    @staticmethod
    def getRandomTriangle(w, h):
        '''
        A factory to generate random triangles which are in the region (0, 0) to (w, h)
        '''
        p1 = (random.randint(0, w), random.randint(0, h))
        p2 = (random.randint(0, w), random.randint(0, h))
        p3 = (random.randint(0, w), random.randint(0, h))
        col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        h = random.random()
        return Triangle(p1, p2, p3, col, h)

    def draw(self, dr):
        '''
        A Method to draw the triangle on screen
        '''
        dr.polygon([self.p1, self.p2, self.p3], fill=self.color)
        return True
    def __repr__(self):
        return 'T'
