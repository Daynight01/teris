import time, random, os, math, pygame, sys
pygame.init()


SCREEN_HEIGHT=900
SCREEN_WIDTH=900

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
run = True
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

def grid():
    for x in range(10):
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect((x*45 + 225, 0, 45, 45)), 2)
        
        for y in range(20):
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect((x*45 + 225, y*45 + 45, 45, 45)), 2)

    pygame.display.update()

grid()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #Updates
    pygame.display.update()
    clock.tick(60)
