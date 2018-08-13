from PIL import Image, ImageDraw

class Screen(object):
    def __init__(self, w, h, color=(255, 255, 255, 255)):
        '''
        Generate the screen to draw the objects
        '''
        self.w = w
        self.h = h
        self.img = Image.new('RGBA', size=(w, h), color=color)
    def draw(self, t):
        '''
        Draw the shape `t`
        '''
        dummy = Image.new('RGBA', size=self.img.size, color=(255,255,255,0))
        dr = ImageDraw.Draw(dummy)
        t.draw(dr)
        self.img = Image.alpha_composite(self.img, dummy)
    def show(self):
        '''
        Show the contents of screen
        '''
        self.img.show()

    def store(self, name):
        self.img.save(name, "PNG")
    def getImg(self):
        return self.img
