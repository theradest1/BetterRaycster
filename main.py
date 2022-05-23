import pygame
import math

screenWidth = 1000
screenHeight = 500

mapHeight = 100
mapWidth = 100
playerX = mapWidth/2
playerY = mapHeight/2

FOV = 90
quality = 1 #higher for lower quality
maxDist = 25

pygame.init()

def text_to_screen(screen, text, x, y, size=50,
                   color=(200, 000, 000), font_type=pygame.font.get_default_font()):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption('Raycaster')

#dvd = pygame.image.load('img_3.png')
#dvd.convert()
#rect = dvd.get_rect()

red = (255, 0, 0)
black = (0, 0, 0)

clock = pygame.time.Clock()


def cast(x, y):
    for angle in range(0, FOV + 1, quality):
        rayX = x
        rayY = y
        dist = 0
        xStep = math.cos(math.radians(angle))
        yStep = math.sin(math.radians(angle))
        hit = False
        print(f"Angle: {angle}, X step: {xStep}, Y step: {yStep} ---------------------------")

        while dist <= maxDist and not hit:
            rayX += xStep
            rayY += yStep
            dist += 1
            print(f"X: {rayX}, Y: {rayY}")
            screen.set_at((int(rayX), int(rayY)), red)


while True:
    dt = clock.tick(60)

    screen.fill(black)
    #pygame.draw.rect(screen, red, pygame.Rect(30, 30, 60, 60))
    cast(playerX, playerY)

    #quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.VIDEORESIZE:
            screenWidth = screen.get_height()
            screenHeight = screen.get_width()
        elif

    pygame.display.flip()
