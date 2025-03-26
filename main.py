import pygame

pygame.init()

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 900
TILE_SIZE = 45
GRID_WIDTH = 10
GRID_HEIGHT = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

tiles = []

def init_grid():
    global tiles
    tiles = []
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            tiles.append({"x": x + 1, "y": y + 1, "color": (0, 0, 0)})

def draw_grid():
    screen.fill((0, 0, 0))
    for tile in tiles:
        x, y, color = tile["x"], tile["y"], tile["color"]
        pygame.draw.rect(screen, color, pygame.Rect(
            (x - 1) * TILE_SIZE + 225,
            (GRID_HEIGHT - y) * TILE_SIZE,
            TILE_SIZE, TILE_SIZE
        ))
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(
            (x - 1) * TILE_SIZE + 225,  
            (GRID_HEIGHT - y) * TILE_SIZE,  
            TILE_SIZE, TILE_SIZE
        ), 2)

def change_tile(x, y, color):
    for tile in tiles:
        if tile["x"] == x and tile["y"] == y:
            tile["color"] = color
            break

init_grid()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                change_tile(1, 1, (255, 0, 0))

    #Updates
    draw_grid()
    pygame.display.update()
    clock.tick(60)
