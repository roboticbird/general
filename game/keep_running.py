import pygame, random
from pygame import *
pygame.init()


WIN_WIDTH = 800
WIN_HEIGHT = 640

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 16
FLAGS = 0

MUTATELIFE = 300 #Active time
INFECTLIFE = 40 #infection time
MUTATECHANCE = 200 #higher it is, the less chance of growth


def main(levelName):
    #initialise
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    timer = pygame.time.Clock()
    random.seed()
    up = down = left = right = False

    #background
    bg = Surface((16, 16))
    bg.convert()
    bg.fill(Color("#444444"))

    #list of everything
    entities = pygame.sprite.Group()

    #map
    blocks = []
    x = y = 0
    level = readLevel(levelName)

    #storing map
    for row in level:
        for col in row:
            if col == "B":
                b = Block(x, y)
                blocks.append(b)
                entities.add(b)
            x += 16
        y += 16
        x = 0

    #add player
    player = Player(32, 32)
    entities.add(player)

    quit = False
    #game loop
    while not quit:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit, "ESCAPE"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYDOWN and e.key == K_r:
                #reinit(entities, blocks, player)
                entities.empty()
                del blocks
                blocks = []
                x = y = 0
                level = readLevel(levelName)

                #storing map
                for row in level:
                    for col in row:
                        if col == "B":
                            b = Block(x, y)
                            blocks.append(b)
                            entities.add(b)
                        x += 16
                    y += 16
                    x = 0

                #add player
                del player
                player = Player(32, 32)
                entities.add(player)

            if e.type == KEYDOWN and e.key == K_q:
                quit = True




        if player.getHealth() > 0:
            #draw screen
            for y in range(64):
                for x in range(64):
                    screen.blit(bg, (x*16, y*16))

            #update player
            player.update(up, down, left, right, blocks)

            #mutate
            chance = random.randint(1, 100)
            if chance <= 50:
                mutate1(blocks, entities)
            else:
                mutate2(blocks, entities)


            #draw and display everything
            entities.draw(screen)
            pygame.display.update()
        else:
            #game over
            pygame.draw.rect(screen, (Color("#DDDDDD")), Rect(16*16,10*16,20*16,8*16))
            myfont = pygame.font.SysFont("monospace", 40)
            label = myfont.render("Game Over", 1, (0,0,0))
            scoreStr = "Score: "
            scoreStr += str(player.getScore()/10 + len(blocks))
            score = myfont.render(scoreStr, 1, (0,0,0))
            screen.blit(label, (19*16, 10*16+2))
            screen.blit(score, (18*16, 15*16+2))
            pygame.display.update()


#entity (every object is this)
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

#player
class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((16,16))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x,y, 16, 16)
        self.health = 1020
        self.score = 0

    def getHealth(self):
        return self.health

    def getScore(self):
        return self.score

    def update(self, up, down, left, right, blocks):
        if up:
            if self.onBlock:
                self.yvel -= 5
                if self.yvel < -10: self.yvel = -4

        if down:
            pass
        if left:
            self.xvel = -3
        if right:
            self.xvel = 3
        if not self.onGround:
            self.yvel += 0.3
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0

        self.rect.left += self.xvel
        self.collide(self.xvel, 0, blocks)
        self.rect.top += self.yvel
        self.onGround = False
        self.onBlock = False
        self.collide(0, self.yvel, blocks)
        self.score += 1

    def collide(self, xvel, yvel, blocks):
        h = Hitbox(self)
        for b in blocks:
            if pygame.sprite.collide_rect(self, b):
                if xvel > 0:
                    self.rect.right = b.rect.left
                if xvel < 0:
                    self.rect.left = b.rect.right
                if yvel > 0:
                    self.rect.bottom = b.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = b.rect.bottom
                    self.yvel = 0

            if pygame.sprite.collide_rect(h, b):
                if b.testActive() == False and b.testInfected() == False:
                    b.infect(INFECTLIFE, MUTATELIFE)
                if b.testActive() == True:
                    b.react(MUTATELIFE)
                    if self.health > 0:
                        self.health -= 1
                        self.image.fill((255-(self.health/4),255-(self.health/4),255))
                self.onBlock = True

class Hitbox(Entity):
    def __init__(self, player):
        Entity.__init__(self)
        x = player.rect.left
        y = player.rect.top-8
        width = 16
        if player.xvel < 0:
            x -= 8
            width += 8
        elif player.xvel > 0:
            width += 8

        self.rect = Rect(x, player.rect.top-8, width, 32)

class Block(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((16,16))
        self.image.fill(Color("#DDDDDD"))
        self.image.convert()
        self.rect = Rect(x, y, 16, 16)
        self.infected = False
        self.active = False
        self.timer = 0
        self.wait = 0

    def infect(self, i, t):
        self.infected = True
        self.wait = i
        self.timer = t
        self.image.fill(Color("#994411"))

    def react(self, t):
        self.active = True
        self.timer = t
        self.image.fill(Color("#EE5500"))

    def testActive(self):
        if self.active == False:
            return False
        return True

    def testInfected(self):
        return self.infected

    def update(self):
        if self.active == True:
            if self.timer <= 0:
                self.timer = 0
                self.active = False
                self.image.fill(Color("#DDDDDD"))
            else:
                self.timer -= 1
        if self.infected == True:
            if self.wait <= 0:
                self.wait = 0
                self.infected = False
                self.active = True
                self.image.fill(Color("#EE5500"))
            else:
                self.wait -= 1


def readLevel(name):
    text_file = open(name,"r")
    lines = text_file.readlines()
    return lines


def mutate1(blocks, entities):
    for b in blocks:
        b.update()
        if b.testActive():
            chance = random.randint(1, MUTATECHANCE)
            if chance <= 2:
                xval = b.rect.left
                yval = b.rect.top-16
                newb = Block(xval, yval)
                newb.react(b.timer)
                exists = False
                for e in entities:
                    if pygame.sprite.collide_rect(newb, e):
                        exists = True

                if not(exists):
                    blocks.append(newb)
                    entities.add(newb)

def mutate2(blocks, entities):
    for b in blocks:
        b.update()
        if b.testActive():
            chance = random.randint(1, MUTATECHANCE)
            if chance <= 2:
                xval = b.rect.left
                yval = b.rect.top
                newb1 = Block(xval+16, yval)
                newb1.react(b.timer)
                newb2 = Block(xval-16, yval)
                newb2.react(b.timer)

                exists1 = False
                exists2 = False
                for e in entities:
                    if pygame.sprite.collide_rect(newb1, e):
                        exists1 = True
                    if pygame.sprite.collide_rect(newb2, e):
                        exists2 = True


                if not(exists1):
                    blocks.append(newb1)
                    entities.add(newb1)
                if not(exists2):
                    blocks.append(newb2)
                    entities.add(newb2)

if __name__ == '__main__':
    levelName = "level"
    main(levelName)
