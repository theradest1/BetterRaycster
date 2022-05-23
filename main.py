import pygame
import math

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
maxDist = 25
speed = 1
rotSpeed = 3
raySpacing = 2  # the distance between two points on a ray (not between rays)


pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption('Raycaster')

# dvd = pygame.image.load('img_3.png')
# dvd.convert()
# rect = dvd.get_rect()

red = (255, 0, 0)
black = (0, 0, 0)

clock = pygame.time.Clock()


def cast(x, y):
    for angle in range(playerRot - int(FOV/2), playerRot + int(FOV/2) + 1, quality):
        rayX = x
        rayY = y
        dist = 0
        xStep = math.cos(math.radians(angle))
        yStep = math.sin(math.radians(angle))
        hit = False
        # print(f"Angle: {angle}, X step: {xStep}, Y step: {yStep} ---------------------------")

        while dist <= maxDist and not hit:
            rayX += xStep
            rayY += yStep
            dist += 1
            # print(f"X: {rayX}, Y: {rayY}")
            screen.set_at((int(rayX), int(rayY)), red)


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
        playerX += math.cos(math.radians(playerRot)) * speed
        playerY += math.sin(math.radians(playerRot)) * speed
    if keys[pygame.K_DOWN]:
        playerX -= math.cos(math.radians(playerRot)) * speed
        playerY -= math.sin(math.radians(playerRot)) * speed
    if keys[pygame.K_RIGHT]:
        playerRot += rotSpeed
    if keys[pygame.K_LEFT]:
        playerRot -= rotSpeed

    pygame.display.flip()
