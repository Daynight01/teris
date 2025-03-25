import time, random, os, math, pygame, sys
pygame.init()


SCREEN_HEIGHT=900
SCREEN_WIDTH=700

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
run = True
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
x=0
y=0

def grid():
    for i in range(5):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((x, y, 50, 50)))
        x+=1
        y+=1

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    grid()
    pygame.display.update()
    clock.tick(60)
