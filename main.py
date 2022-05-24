import pygame
import math
import numpy as np
from PIL import ImageEnhance, Image

# variables
screenWidth = 670
screenHeight = 350

mapHeight = 200
mapWidth = 200

playerX = mapWidth / 2
playerY = mapHeight / 2
playerRot = 0

FOV =90
quality = 3  # higher for lower quality
maxDist = 100000
speed = .1
rotSpeed = .1
raySpacing = 1  # the distance between two points on a ray (not between rays)

wall = Image.open("lightWall.png")
enhancer = ImageEnhance.Brightness(wall)
wall = enhancer.enhance(.5)
wall.save("darkWall.png")

lightWall = pygame.image.load("lightWall.png")
darkWall = pygame.image.load("darkWall.png")

map = np.array([])
map.resize(mapWidth, mapHeight)

for x in range(0, mapWidth):
    for y in range(0, mapHeight):
        if y == 0 or y == mapHeight - 1 or x == 0 or x == mapWidth - 1:
            map[x, y] = 1

#print(map)
#print(map.size)

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption('Raycaster')

screenWidth = screen.get_width()
screenHeight = screen.get_height()
pixelSpacing = int(screenWidth/(FOV/quality)) # for printing walls

# dvd = pygame.image.load('img_3.png')
# dvd.convert()
# rect = dvd.get_rect()

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()


def clamp(value, lower, upper):
    return lower if value < lower else upper if value > upper else value


def printMap():
    for _x in range(0, mapWidth):
        for _y in range(0, mapHeight):
            if map[_x, _y]:
                screen.set_at((int(_x), int(_y)), white)


def cast(x, y):
    #print("___________")
    tAngle = -45
    for angle in range(int(playerRot - FOV / 2), int(playerRot + FOV / 2 + 1), quality):
        dist, locX, locY = ray(x, y, angle)
        # print(dist)
        unFish = math.cos(math.radians(tAngle))
        #print(f"{unFish}, {_angle}")
        tAngle += 1
        dist *= unFish
        
        scale = maxDist - dist*2 + 200
        #print(f"{dist * 2 + 150} < {maxDist}")
        if dist and scale > 0:
            #pygame.draw.rect(screen, wallColor(locX, locY), pygame.Rect((playerRot - angle) * pixelSpacing + 180, dist, pixelSpacing, maxDist - dist * 2 + 150))
            printWall = wallColor(locX, locY)
            if printWall:
                
              scaledWall = pygame.transform.scale(printWall, (pixelSpacing, scale))
              locWall = ((playerRot - angle) * pixelSpacing + 180, dist - 50)
              screen.blit(scaledWall, locWall)
            #print(screenHeight - dist * 2)


def ray(x, y, angle):
    _rayX = x
    _rayY = y
    _dist = 0
    _xStep = math.cos(math.radians(angle)) * raySpacing
    _yStep = math.sin(math.radians(angle)) * raySpacing
    for _dist in range(maxDist):
        _rayX += _xStep
        _rayY += _yStep
        if not (0 <= _rayX < mapWidth and 0 <= _rayY < mapHeight) or map[int(_rayX), int(_rayY)]:
            return _dist, int(_rayX), int(_rayY)
        #screen.set_at((int(_rayX), int(_rayY)), red)
    return False, False, False


def wallColor(x, y):
    #print(f"X: {clamp(x + 1, 0, mapWidth - 1)}, Y: {y}")
    if map[clamp(x + 1, 0, mapWidth - 1), clamp(y, 0, mapWidth - 1)] and map[clamp(x - 1, 0, mapWidth - 1), clamp(y, 0, mapWidth - 1)]:
        return lightWall
    elif map[clamp(x, 0, mapWidth - 1), clamp(y + 1, 0, mapHeight - 1)] and map[clamp(x, 0, mapWidth - 1), clamp(y - 1, 0, mapHeight - 1)]:
        return darkWall
    return False


keys = []
while True:
    dt = clock.tick(60)

    screen.fill(black)
    cast(playerX, playerY)
    #printMap()

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.VIDEORESIZE:
            screenWidth = screen.get_width()
            screenHeight = screen.get_height()
            pixelSpacing = int(screenWidth/(FOV/quality))

    # keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        playerX = clamp(playerX + math.cos(math.radians(playerRot)) * speed * dt, 0, mapWidth)
        playerY = clamp(playerY + math.sin(math.radians(playerRot)) * speed * dt, 0, mapHeight)
    if keys[pygame.K_DOWN]:
        playerX = clamp(playerX - math.cos(math.radians(playerRot)) * speed * dt, 0, mapWidth)
        playerY = clamp(playerY - math.sin(math.radians(playerRot)) * speed * dt, 0, mapHeight)
    if keys[pygame.K_RIGHT]:
        playerRot -= rotSpeed * dt
    if keys[pygame.K_LEFT]:
        playerRot += rotSpeed * dt

    pygame.display.flip()