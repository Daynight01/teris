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

two_by_two = [{"x": 1, "y": GRID_HEIGHT, "color": (255, 0, 0)}, {"x": 2, "y": GRID_HEIGHT, "color": (255, 0, 0)}, {"x": 1, "y": GRID_HEIGHT-1, "color": (255, 0, 0)}, {"x": 2, "y": GRID_HEIGHT-1, "color": (255, 0, 0)}]
print(two_by_two[0])
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
    for piece in range(len(two_by_two)):
        pygame.draw.rect(screen, two_by_two[piece]["color"], pygame.Rect(
            (two_by_two[piece]["x"] - 1) * TILE_SIZE + 225,  
            (GRID_HEIGHT - two_by_two[piece]["y"]) * TILE_SIZE,  
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
    for piece in range(len(two_by_two)):
        new_x = two_by_two[piece]["x"] + dx
        new_y = two_by_two[piece]["y"] + dy

        if 1 <= new_x <= GRID_WIDTH:
            two_by_two[piece]["x"] = new_x
        if 1 <= new_y <= GRID_HEIGHT:
            two_by_two[piece]["y"] = new_y
    print(two_by_two)

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
                    last_fall_time = current_time-FALL_TIME
        
    #Shift Down
    if current_time - last_fall_time > FALL_TIME:
        can_move_shape=[True,True,True,True]
        for piece in range(len(two_by_two)):
            current_space = (two_by_two[piece]["x"]*20)-20 + (two_by_two[piece]["y"])-1
            space_right = (two_by_two[piece]["x"]*20) + (two_by_two[piece]["y"])-1
            space_left = (two_by_two[piece]["x"]*20)-40 + (two_by_two[piece]["y"])-1
            # height map has been made
            # print(tiles[space_right])
            print(tiles[current_space])
            print(tiles[space_left])
            if tiles[current_space]["space_bellow_filled"]==False:
                can_move_shape[piece] = True
            # detects when a tile hits the floor and where, and fixes it to the grid map.
    
            if active_tile["y"]==1 or tiles[current_space]["space_bellow_filled"]==True:
                if skip1==0:
                    for piece in range(len(two_by_two)):
                        change_tile(two_by_two[piece]["x"],two_by_two[piece]["y"],two_by_two[piece]["color"])
                    two_by_two = [{"x": 1, "y": GRID_HEIGHT, "color": (255, 0, 0)}, {"x": 2, "y": GRID_HEIGHT, "color": (255, 0, 0)}, {"x": 1, "y": GRID_HEIGHT-1, "color": (255, 0, 0)}, {"x": 2, "y": GRID_HEIGHT-1, "color": (255, 0, 0)}]
                    skip1+=1
                else:
                    skip1-=1
        if can_move_shape==[True,True,True,True]:
            move_tile(0, -1)
            last_fall_time = current_time

    #Updates
    draw_grid()
    pygame.display.update()
    clock.tick(60)
