import pygame

pygame.init()

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 900
TILE_SIZE = 45
GRID_WIDTH = 10
GRID_HEIGHT = 20

# This might need to be changed if we want an actual level system
FALL_TIME = 1000




screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

skip1=1
tiles = []
new_tile = {"x": 1, "y": GRID_HEIGHT, "color": (255, 0, 0)}
active_tile = {"x": 1, "y": GRID_HEIGHT, "color": (255, 0, 0)}
last_fall_time = pygame.time.get_ticks()

def init_grid():
    global tiles
    tiles = []
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            tiles.append({"x": x + 1, "y": y + 1, "color": (0, 0, 0), "space_bellow_filled": False, "space_filled": False})

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

def get_tile_at(x, y):
    for tile in tiles:
        if tile["x"] == x and tile["y"] == y:
            return tile
    return None

def change_tile(x, y, color):
    for tile in tiles:
        if tile["x"] == x and tile["y"] == y:
            tile["color"] = color
            tile["space_filled"] = True
            print(tile)

        if tile["x"] == x and tile["y"] == y+1:
            tile["space_bellow_filled"] = True
            print(tile)
            break
            

def move_tile(dx, dy):
    new_x = active_tile["x"] + dx
    new_y = active_tile["y"] + dy

    if 1 <= new_x <= GRID_WIDTH:
        active_tile["x"] = new_x
    if 1 <= new_y <= GRID_HEIGHT:
        active_tile["y"] = new_y

def hard_drop():
    while active_tile["y"] > 1:
        below_tile = get_tile_at(active_tile["x"], active_tile["y"] - 1)
        if below_tile and below_tile["space_filled"]:
            break
        active_tile["y"] -= 1

init_grid()
print(tiles)
print(active_tile)
run = True
while run:
    current_time = pygame.time.get_ticks()
    current_space = (active_tile["x"]*20)-20 + (active_tile["y"])-1
    space_right = (active_tile["x"]*20) + (active_tile["y"])-1
    space_left = (active_tile["x"]*20)-40 + (active_tile["y"])-1
    
    # print(current_time,last_fall_time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("")
            print(tiles)
            pygame.quit()
            exit()

        #Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if tiles[space_left]["space_filled"]==False:
                    move_tile(-1, 0)
            if event.key == pygame.K_RIGHT:
                # This is here because the right wall is outside the tiles index, so it would crash without this.
                try:
                    right_wall_exception_catch = tiles[space_right]["space_filled"]
                except:
                    right_wall_exception_catch = True
                if right_wall_exception_catch==False: 
                    move_tile(1, 0)
            if event.key == pygame.K_DOWN: 
                if tiles[current_space]["space_bellow_filled"]==False and active_tile["y"]!=1:
                    move_tile(0, -1)
                    last_fall_time = current_time
            if event.key == pygame.K_SPACE:
                if tiles[current_space]["space_bellow_filled"]==False and active_tile["y"]!=1:
                    hard_drop()
                    last_fall_time = current_time
        
    #Shift Down
    if current_time - last_fall_time > FALL_TIME:
        # height map has been made
        # print(tiles[space_right])
        print(tiles[current_space])
        print(tiles[space_left])
        if tiles[current_space]["space_bellow_filled"]==False:
            move_tile(0, -1)
        last_fall_time = current_time
        # detects when a tile hits the floor and where, and fixes it to the grid map.
        if active_tile["y"]==1 or tiles[current_space]["space_bellow_filled"]==True:
            if skip1==0:
                change_tile(active_tile["x"],active_tile["y"],active_tile["color"])
                active_tile = {"x": 1, "y": GRID_HEIGHT, "color": (255, 0, 0)}
                skip1+=1
            else:
                skip1-=1
    
    

    #Updates
    draw_grid()
    pygame.display.update()
    clock.tick(60)