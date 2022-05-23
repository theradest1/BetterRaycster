import pygame
import math
import numpy as np

# variables
screenWidth = 1000
screenHeight = 500

mapHeight = 100
mapWidth = 100

playerX = mapWidth/2
playerY = mapHeight/2
playerRot = 0

FOV = 90
quality = 1  # higher for lower quality
maxDist = 100
speed = .1
rotSpeed = .1
raySpacing = .5  # the distance between two points on a ray (not between rays)

map = np.array([])
map.resize(mapWidth, mapHeight)

print(map)
print(map.size)

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption('Raycaster')

# dvd = pygame.image.load('img_3.png')
# dvd.convert()
# rect = dvd.get_rect()

red = (255, 0, 0)
black = (0, 0, 0)

clock = pygame.time.Clock()


def clamp(value, lower, upper):
    return lower if value < lower else upper if value > upper else value
  

def cast(x, y):
    for angle in range(int(playerRot - FOV/2), int(playerRot + FOV/2 + 1), quality):
        print(ray(x, y, angle))

def ray(x, y, angle):
  rayX = x
  rayY = y
  dist = 0
  xStep = math.cos(math.radians(angle)) * raySpacing
  yStep = math.sin(math.radians(angle)) * raySpacing
  for dist in range(maxDist):
      rayX += xStep
      rayY += yStep
      if not(0 <= rayX < mapWidth and 0 <= rayY < mapHeight):
        return False
      #if np.zip(*map):
      #  return map[rayX, rayY]
      screen.set_at((int(rayX), int(rayY)), red)
      
  return False


keys = []
while True:
    dt = clock.tick(60)

    screen.fill(black)
    # pygame.draw.rect(screen, red, pygame.Rect(30, 30, 60, 60))
    cast(playerX, playerY)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.VIDEORESIZE:
            screenWidth = screen.get_height()
            screenHeight = screen.get_width()

    # keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        playerX = clamp(playerX + math.cos(math.radians(playerRot)) * speed * dt, 0, mapWidth)
        playerY = clamp(playerY + math.sin(math.radians(playerRot)) * speed * dt, 0, mapHeight)
    if keys[pygame.K_DOWN]:
        playerX = clamp(playerX - math.cos(math.radians(playerRot)) * speed * dt, 0, mapWidth)
        playerY = clamp(playerY - math.sin(math.radians(playerRot)) * speed * dt, 0, mapHeight)
    if keys[pygame.K_RIGHT]:
        playerRot += rotSpeed * dt
    if keys[pygame.K_LEFT]:
        playerRot -= rotSpeed * dt

    pygame.display.flip()
