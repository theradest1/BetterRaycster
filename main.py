import pygame
import math
import numpy as np
from PIL import ImageEnhance, Image

# variables
screenWidth = 670
screenHeight = 350

mapHeight = 200
map_width = 200

playerX = map_width / 2
playerY = mapHeight / 2
playerRot = 0

FOV = 90
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

mapMatrix = np.array([])
mapMatrix.resize((map_width, mapHeight))

for x in range(0, map_width):
    for y in range(0, mapHeight):
        if y == 0 or y == mapHeight - 1 or x == 0 or x == map_width - 1:
            mapMatrix[x, y] = 1

# print(mapMatrix)
# print(mapMatrix.size)

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption('Ray caster')

screenWidth = screen.get_width()
screenHeight = screen.get_height()
pixelSpacing = int(screenWidth/(FOV/quality))  # for printing walls

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


def print_map():
    for _x in range(0, map_width):
        for _y in range(0, mapHeight):
            if mapMatrix[_x, _y]:
                screen.set_at((int(_x), int(_y)), white)


def cast(map_x, map_y):
    # print("___________")
    tAngle = -45
    for angle in range(int(playerRot - FOV / 2), int(playerRot + FOV / 2 + 1), quality):
        dist, locX, locY = ray(map_x, map_y, angle)
        # print(dist)
        unFish = math.cos(math.radians(tAngle))
        # print(f"{unFish}, {_angle}")
        tAngle += 1
        dist *= unFish
        
        scale = maxDist - dist*2 + 200
        # print(f"{dist * 2 + 150} < {maxDist}")
        if dist and scale > 0:
            # pygame.draw.rect(screen, wall_color(locX, locY), pygame.Rect((playerRot - angle)
            # * pixelSpacing + 180, dist, pixelSpacing, maxDist - dist * 2 + 150))
            printWall = wall_color(locX, locY)
            if printWall:
                scaledWall = pygame.transform.scale(printWall, (pixelSpacing, scale))
                locWall = ((playerRot - angle) * pixelSpacing + 180, dist - 50)
                screen.blit(scaledWall, locWall)
            # print(screenHeight - dist * 2)


def ray(ray_x, ray_y, angle):
    _dist = 0
    _xStep = math.cos(math.radians(angle)) * raySpacing
    _yStep = math.sin(math.radians(angle)) * raySpacing
    for _dist in range(maxDist):
        ray_x += _xStep
        ray_y += _yStep
        if not (0 <= ray_x < map_width and 0 <= ray_y < mapHeight) or mapMatrix[int(ray_x), int(ray_y)]:
            return _dist, int(ray_x), int(ray_y)
        # screen.set_at((int(ray_x), int(ray_y)), red)
    return False, False, False


def wall_color(map_x, map_y):
    # print(f"map_x: {clamp(map_x + 1, 0, map_width - 1)}, map_y: {map_y}")
    if mapMatrix[clamp(map_x + 1, 0, map_width - 1), clamp(map_y, 0, map_width - 1)] and mapMatrix[clamp(map_x - 1, 0, map_width - 1), clamp(map_y, 0, map_width - 1)]:
        return lightWall
    elif mapMatrix[clamp(map_x, 0, map_width - 1), clamp(map_y + 1, 0, mapHeight - 1)] and mapMatrix[clamp(map_x, 0, map_width - 1), clamp(map_y - 1, 0, mapHeight - 1)]:
        return darkWall
    return False


keys = []
while True:
    dt = clock.tick(60)

    screen.fill(black)
    cast(playerX, playerY)
    # print_map()

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.VIDEORESIZE:
            screenWidth = screen.get_width()
            screenHeight = screen.get_height()
            pixelSpacing = int(screenWidth/(FOV/quality))

    # key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        playerX = clamp(playerX + math.cos(math.radians(playerRot)) * speed * dt, 0, map_width)
        playerY = clamp(playerY + math.sin(math.radians(playerRot)) * speed * dt, 0, mapHeight)
    if keys[pygame.K_DOWN]:
        playerX = clamp(playerX - math.cos(math.radians(playerRot)) * speed * dt, 0, map_width)
        playerY = clamp(playerY - math.sin(math.radians(playerRot)) * speed * dt, 0, mapHeight)
    if keys[pygame.K_RIGHT]:
        playerRot -= rotSpeed * dt
    if keys[pygame.K_LEFT]:
        playerRot += rotSpeed * dt

    pygame.display.flip()
    