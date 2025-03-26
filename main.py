import pygame
# I'm going to make a heightmap for the tiles. - Dwyn
pygame.init()

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 900
TILE_SIZE = 45
GRID_WIDTH = 10
GRID_HEIGHT = 20
FALL_TIME = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

tiles = []
active_tile = {"x": 1, "y": GRID_HEIGHT, "color": (255, 0, 0)}
last_fall_time = pygame.time.get_ticks()

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
    # Draw active moving tile
    pygame.draw.rect(screen, active_tile["color"], pygame.Rect(
        (active_tile["x"] - 1) * TILE_SIZE + 225,  
        (GRID_HEIGHT - active_tile["y"]) * TILE_SIZE,  
        TILE_SIZE, TILE_SIZE
    ))

def change_tile(x, y, color):
    for tile in tiles:
        if tile["x"] == x and tile["y"] == y:
            tile["color"] = color
            break

def move_tile(dx, dy):
    new_x = active_tile["x"] + dx
    new_y = active_tile["y"] + dy

    if 1 <= new_x <= GRID_WIDTH:
        active_tile["x"] = new_x
    if 1 <= new_y <= GRID_HEIGHT:
        active_tile["y"] = new_y

init_grid()

run = True
while run:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_tile(-1, 0)
            if event.key == pygame.K_RIGHT: 
                move_tile(1, 0)
            if event.key == pygame.K_DOWN: 
                move_tile(0, -1)
                last_fall_time = current_time
        
    #Shift Down
    if current_time - last_fall_time > FALL_TIME:
        move_tile(0, -1)
        last_fall_time = current_time
                

    #Updates
    draw_grid()
    pygame.display.update()
    clock.tick(60)
