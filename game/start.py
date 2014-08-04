import pygame, keep_running
from pygame import *


WIN_WIDTH = 800
WIN_HEIGHT = 640

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 16
FLAGS = 0

MUTATELIFE = 300 #Active time
INFECTLIFE = 40 #infection time
MUTATECHANCE = 200 #higher it is, the less chance of growth


def main():
    #initialise
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    timer = pygame.time.Clock()
    up = down = left = right = False

    #background
    bg = Surface((16, 16))
    bg.convert()
    bg.fill(Color("#DDDDDD"))

    select = Selector(14*16,14*16)

    myfont = pygame.font.SysFont("monospace", 50)
    title = myfont.render("KEEP RUNNING", 1, (0,0,0))
    myfont = pygame.font.SysFont("monospace", 20)
    label1 = myfont.render("Level 1", 1, (0,0,0))
    label2 = myfont.render("Level 2", 1, (0,0,0))
    label3 = myfont.render("Level 3", 1, (0,0,0))
    label4 = myfont.render("Level 4", 1, (0,0,0))
    label5 = myfont.render("Sam's Level", 1, (0,0,0))
    myfont = pygame.font.SysFont("monospace", 15)
    signed = myfont.render("tom did this.", 1, (0,0,0))




    #list of everything
    entities = pygame.sprite.Group()
    entities.add(select)
    #game loop
    while 1:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit, "ESCAPE"
            if e.type == KEYDOWN and e.key == K_UP:
                select.up()
            if e.type == KEYDOWN and e.key == K_DOWN:
                select.down()
            if e.type == KEYDOWN and e.key == K_RETURN:
                keep_running.main(select.getLevel())

            #draw screen
            for y in range(64):
                for x in range(64):
                    screen.blit(bg, (x*16, y*16))

            #draw and display everything
            entities.draw(screen)

            screen.blit(title, (14*16, 5*16))
            screen.blit(label1, (16*16, 14*16))
            screen.blit(label2, (16*16, 16*16))
            screen.blit(label3, (16*16, 18*16))
            screen.blit(label4, (16*16, 20*16))
            screen.blit(label5, (16*16, 22*16))
            screen.blit(signed, (42*16, 38*16))
            pygame.display.update()


#entity (every object is this)
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Selector(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.num = 0
        self.start = y+4
        self.image = Surface((16,16))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x,y+4,16,16)

    def up(self):
        self.num = (self.num - 1) % 5
        self.rect.top = self.start+(self.num*32)

    def down(self):
        self.num = (self.num + 1) % 5
        self.rect.top = self.start+(self.num*32)

    def getLevel(self):
        if self.num == 0:
            return "level1"
        elif self.num == 1:
            return "level2"
        elif self.num == 2:
            return "level3"
        elif self.num == 3:
            return "level4"
        elif self.num == 4:
            return "level6"

main()
