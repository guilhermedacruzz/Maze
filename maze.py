import pygame
import random
import math
import sys
import time

error = pygame.init()
if error[1] > 0:
    print("Erro ao iniciar o PyGame!")
    format(error[1])
    sys.exit(-1)
else:
    print("Inicialializado com Sucesso!")

class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None

    def addNeighbors(self, grid, cell):
        x = self.x
        y = self.y

        if x > 0 and not cell[x][y].wall[3]:
            self.neighbors.append(grid[x - 1][y])

        if x < COLS - 1 and not cell[x][y].wall[1]:
            self.neighbors.append(grid[x + 1][y])

        if y > 0 and not cell[x][y].wall[0]:
            self.neighbors.append(grid[x][y - 1])

        if y < ROWS - 1 and not cell[x][y].wall[2]:
            self.neighbors.append(grid[x][y + 1])


    def show(self, color):
        pygame.draw.rect(window, color, (self.x * W, self.y * H, W, H))


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = [True, True, True, True]
        self.visit = False

    def show(self, color):
        x = self.x * W
        y = self.y * W

        if self.wall[0]:
            pygame.draw.line(window, color, (x, y), (x + W, y))
        if self.wall[1]:    
            pygame.draw.line(window, color, (x + W, y), (x + W, y + W))
        if self.wall[2]:
            pygame.draw.line(window, color, (x + W, y + W), (x, y + W))
        if self.wall[3]:
            pygame.draw.line(window, color, (x, y + W), (x, y))
    
    def showVisit(self):
        x = self.x * W
        y = self.y * W

        if self.visit:
            pygame.draw.rect(window, (79, 93, 117), (x, y, W, W))

    def highlight(self):
        pygame.draw.rect(window, (239, 131, 84), (self.x * W, self.y * W, W, H))


    def checkNeighBors(self, grid):
        neighbors = []

        if self.y > 0:
            top   = grid[self.x][self.y - 1]
            if not top.visit:
                neighbors.append(top)

        if self.x < ROWS - 1:
            right = grid[self.x + 1][self.y]
            if not right.visit:
                neighbors.append(right)
        
        if self.y < COLS - 1:
            down  = grid[self.x][self.y + 1]
            if not down.visit:
                neighbors.append(down)
        
        if self. x > 0:
            left  = grid[self.x - 1][self.y]
            if not left.visit:
                neighbors.append(left)

        if len(neighbors) > 0:
            r = math.floor(random.randint(0, len(neighbors) - 1))
            return neighbors[r]
        else:
            return None

COLS = 30
ROWS = 30


WIDTH = 600
HEIGHT = 600

W = WIDTH / COLS
H = HEIGHT / ROWS

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

current = Cell(0, 0)
isPathFinder = False

def main():

    grid = [[Cell(x, y) for y in range(COLS)] for x in range(ROWS)]

    global current
    current = grid[0][0]

    stack = []

    block = [[Spot(x, y) for y in range(COLS)] for x in range(ROWS)]

    openSet = []
    closedSet = []
    path = []

    start = block[0][0]
    end = block[COLS - 1][ROWS - 1]

    openSet.append(start)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
    
        window.fill((45, 49, 66))
        
        if isPathFinder:
            run(block, openSet, closedSet, path, end, grid)
        else:
            draw(grid, stack, block)

        pygame.display.flip()  
        clock.tick(60)

def run(block, openSet, closedSet, path, end, grid):

    if len(openSet) > 0:

        winner = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[winner].f:
                winner = i
        
        current = openSet[winner]

        if current == end:
            openSet = []
            openSet.append(current)

        closedSet.append(current)
        openSet.remove(current)

        neighbors = current.neighbors

        for i in range(len(neighbors)):
            newPath = False
            neighbor = neighbors[i]

            if neighbor not in closedSet:
                tempG =  current.g + 1

                if neighbor in openSet:
                    if tempG < neighbor.g:
                        neighbor.g = tempG
                        newPath =  True
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)
                    newPath = True

                if newPath:
                    neighbor.f = neighbor.g + heuristic(neighbor, end)
                    neighbor.previous = current

    else:
        current = end

    for i in grid:
        for f in i:
            f.showVisit()

    path = []
    temp = current
    path.append(temp)
    while temp.previous != None:
        path.append(temp.previous)
        temp = temp.previous

    for i in path:
        i.show((112, 128, 144))

    for i in grid:
        for f in i:
            f.show((255, 255, 255))

def draw(grid, stack, block):

    for i in grid:
        for f in i:
            f.showVisit()
            f.show((255, 255, 255))

    global current
    current.visit = True
    current.highlight()
    nexts = current.checkNeighBors(grid)

    if nexts != None:
        nexts.visit = True
        stack.append(current)
        removeWall(current, nexts)
        current = nexts
    elif len(stack) > 0:
        current = stack.pop()
    else:
        print("END")

        global isPathFinder
        isPathFinder = True

        for i in range(ROWS):
            for f in range(COLS):
                block[i][f].addNeighbors(block, grid)


def removeWall(c, n):

    x = c.x - n.x
    y = c.y - n.y

    if x == 1:
        c.wall[3] = n.wall[1] = False
    elif x == -1:
        c.wall[1] = n.wall[3] = False
    if y == 1:
        c.wall[0] = n.wall[2] = False
    elif y == -1:
        c.wall[2] = n.wall[0] = False

def heuristic(neighbor, end):
    
    n = [neighbor.x, neighbor.y]
    e = [end.x, end.y]
    return math.dist(n, e)
    #return abs(neighbor.x - end.x) + abs(neighbor.y - end.y)

main()