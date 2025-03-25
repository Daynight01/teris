import time, random, os, math, pygame, sys
pygame.init()

SCREEN_HEIGHT=900
SCREEN_WIDTH=900

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
run = True
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
tile = []

def grid():
    for x in range(10):
        for y in range(20):
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect((x*45 + 225, y*45, 45, 45)), 2)
            tile.append((x+1,y+1, False, (0, 0, 0, 255)))
    pygame.display.update()

grid()

def update(screen, square_list, size=45):
    for x, y, active, color in square_list:
        if active:
            pygame.draw.rect(screen, color, (x, y, size, size))


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    update(screen, tile)
    

    #Updates
    pygame.display.update()
    clock.tick(60)
