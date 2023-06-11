from typing import Tuple, List

import pygame as pg
import math

points = [(600, 200),
          (500, 400),
          (600, 400),
          (700, 400),
          (400, 600),
          (600, 600),
          (800, 600),
          (300, 800),
          (600, 800),
          (900, 800)
          ]
hor = 80
ver = 120
initial_points = []
initial_points.append((hor, ver))
ver = ver + 90
for i in range(6):
    initial_points.append((hor, ver))
    hor = hor + 80
    if (i == 2):
        ver = ver + 90
        hor = 80


def calculateDistance(X, Y):
    val = ((X[0] - Y[0]) ** 2) + ((X[1] - Y[1]) ** 2)
    dist = math.sqrt(val)
    return dist


EMPTY = 0
TIGER_TYPE = 1
FOX_TYPE = 2
ALIVE = 1
DEAD = 0
turn = TIGER_TYPE
count = 0


class Node(object):
    def __init__(self, hop1, hop2, type):
        self.hop1 = hop1
        self.hop2 = hop2
        self.type = type


nodes = []

nodes.append(Node([1, 2, 3], [4, 5, 6], EMPTY))
nodes.append(Node([0, 2, 4], [3, 7], EMPTY))
nodes.append(Node([0, 1, 3, 5], [8], EMPTY))
nodes.append(Node([0, 2, 6], [1, 9], EMPTY))
nodes.append(Node([1, 5, 7], [0, 6], EMPTY))
nodes.append(Node([2, 4, 6, 8], [0], EMPTY))
nodes.append(Node([3, 5, 9], [4], EMPTY))
nodes.append(Node([4, 8], [1, 9], EMPTY))
nodes.append(Node([5, 7, 9], [2], EMPTY))
nodes.append(Node([6, 8], [3, 7], EMPTY))

pg.init()
screen = pg.display.set_mode((1200, 1000))
pg.display.set_caption("Len Choa")
tiger_path = 'tiger.png'
fox_path = 'fox.png'


class Player(object):
    def __init__(self, pos, path, type):
        self.x = initial_points[pos][0]
        self.y = initial_points[pos][1]
        self.dx = 0
        self.dy = 0
        self.stepx = 0
        self.stepy = 0
        self.char = pg.image.load(path)
        self.action = False
        self.clock = pg.time.Clock()
        self.position = -1
        self.newPos = -1
        self.isValid = False
        self.type= type

    def draw(self):
        screen.blit(self.char, (self.x - 32, self.y - 32))

    def setParameters(self):
        if self.isValid and self.action == False:
            self.action = True
            axes = points[self.newPos]
            self.dx = axes[0] - self.x
            self.dy = axes[1] - self.y
            self.stepx = self.dx / 10
            self.stepy = self.dy / 10
            nodes[self.newPos].type = self.type
            print(self.newPos)
            print(nodes[self.newPos].type)
            if(self.position!=-1):
                nodes[self.position].type = EMPTY
            self.position = self.newPos
            self.isValid = False

        
        
    def check_if_valid_initial(self, axes):
        for i in range(10):
            dist = calculateDistance(points[i], axes)
            if dist < 32 and nodes[i].type == EMPTY:
                self.isValid = True
                self.newPos = i
                return True
        return False


class Tiger(Player):
    def __init__(self, pos, path,type):
        Tiger.stage_0 = True
        super().__init__(pos, path,type)

    def check_if_valid(self, axes):
        valids = []
        for i in nodes[self.position].hop1:
            if nodes[i].type == EMPTY:
                valids.append(i)
        for i in valids:
            dist = calculateDistance(points[i], axes)
            if dist <= 15:
                self.isValid = True
                self.newPos = i
                return True
        return False


class Fox(Player):
    def __init__(self, pos, path,type):
        self.state = ALIVE
        self.alpha = 255
        Fox.selected = False
        Fox.stage_0 = True
        super().__init__(pos, path,type)



    def check_if_valid(self, axes):
        valids = []
        for i in nodes[self.position].hop1:
            if nodes[i].type == EMPTY:
                valids.append(i)
        for i in valids:
            dist = calculateDistance(points[i], axes)
            if dist <= 32:
                self.isValid = True
                self.newPos = i
                return True
        return False

    @staticmethod
    def check_selected(axes):
        for i in range(10):
            dist = calculateDistance(points[i], axes)
            if dist <= 32 and nodes[i].type == FOX_TYPE:
                return True, i
        return False, -1





axes = ()
tiger = Tiger(0, tiger_path,TIGER_TYPE)
foxes = []

for i in range(1, 7):
    foxes.append(Fox(i, fox_path,FOX_TYPE))


def board():
    pg.draw.aaline(screen, (0, 0, 0), points[0], points[7])
    pg.draw.aaline(screen, (0, 0, 0), points[7], points[9])
    pg.draw.aaline(screen, (0, 0, 0), points[0], points[9])
    pg.draw.aaline(screen, (0, 0, 0), points[0], points[8])
    pg.draw.aaline(screen, (0, 0, 0), points[1], points[3])
    pg.draw.aaline(screen, (0, 0, 0), points[4], points[6])

def drawGame():
    screen.fill((255, 255, 255))
    board()
    for fox in foxes:
        if fox.state == ALIVE:
            fox.draw()
    tiger.draw()
    pg.display.update()


def move(agent):
    agent.setParameters()
    axes = points[agent.newPos]
    while agent.action:
        agent.x = agent.x + agent.stepx
        agent.y = agent.y + agent.stepy
        drawGame()
        if agent.x - axes[0] < .1 and agent.y - axes[1] < .1:
            agent.x = axes[0]
            agent.y = axes[1]
            agent.action = False

# game loop
running = True
while running:
    pg.time.delay(50)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        if event.type == pg.MOUSEBUTTONDOWN:
            xy = pg.mouse.get_pos()
            if (turn == TIGER_TYPE):
                if (Tiger.stage_0):
                    flag = tiger.check_if_valid_initial(xy)
                    if (flag):
                        move(tiger)
                        Tiger.stage_0 = False
                        turn = FOX_TYPE
                else:
                    flag = tiger.check_if_valid(xy)
                    if (flag):
                        move(tiger)
                        turn = FOX_TYPE
            elif (turn == FOX_TYPE):
                if (Fox.stage_0):
                    flag = foxes[count].check_if_valid_initial(xy)
                    if (flag):
                        move(foxes[count])
                        count = count + 1
                        turn = TIGER_TYPE
                    if count > 5:
                        Fox.stage_0 = False



    drawGame()
    pg.event.clear()
