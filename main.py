import pygame
import random

pygame.init()

# Download as a zip to make it easier to run.
BACKGROUND = pygame.image.load("maryo.jpg")
BACKGROUND = pygame.transform.scale(BACKGROUND, (900, 900))

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 900
TILE_SIZE = 45
GRID_WIDTH = 10
GRID_HEIGHT = 20

# I haven't added a score system yet, I just added a variable for it
SCORE = 0

# This might need to be changed if we want an actual level system
FALL_TIME = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()


skip1 = 1
tiles = []
new_tile = {"x": 1, "y": GRID_HEIGHT, "color": (255, 0, 0)}
active_tile = {"x": 1, "y": GRID_HEIGHT, "color": (255, 0, 0)}
last_fall_time = pygame.time.get_ticks()


def create_shape(relative_coords, base_x=GRID_WIDTH // 2, base_y=GRID_HEIGHT):
    return [{"x": base_x + coord[0], "y": base_y + coord[1]} for coord in relative_coords]


square_shape = create_shape([(0, 0), (1, 0), (0, -1), (1, -1)])
line_shape = create_shape([(0, 0), (1, 0), (2, 0), (3, 0)])
t_shape = create_shape([(0, 0), (1, 0), (2, 0), (1, -1)])
l_shape = create_shape([(0, 0), (0, -1), (0, -2), (1, 0)])
reverse_l_shape = create_shape([(1, 0), (1, -1), (1, -2), (0, 0)])
z_shape = create_shape([(0, 0), (1, 0), (1, -1), (2, -1)])
reverse_z_shape = create_shape([(2, 0), (1, 0), (1, -1), (0, -1)])

# Add more shapes as needed

shapes = random.choice([square_shape])
print(shapes)


# Add more shapes to the list as needed
def init_grid():
    global tiles
    tiles = []
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            tiles.append(
                {"x": x + 1, "y": y + 1, "color": (0, 0, 0), "space_filled": False})


def draw_active(shape):
    for piece in shape:
        screen.blit(pygame.image.load(f"tetristestpiece.bmp"),(
            (piece["x"] - 1) * TILE_SIZE + 225,
            (GRID_HEIGHT - piece["y"]) * TILE_SIZE))


def draw_grid():
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(pygame.image.load("tetristestpiece.bmp"), (0,0))
    for tile in tiles:
        x, y, color = tile["x"], tile["y"], tile["color"]
        # screen.blit(pygame.image.load(f"tetris-test-piece2.bmp"),(
        #     (x - 1) * TILE_SIZE + 225,
        #     (GRID_HEIGHT - y) * TILE_SIZE))
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(
            (x - 1) * TILE_SIZE + 225,
            (GRID_HEIGHT - y) * TILE_SIZE,
            TILE_SIZE, TILE_SIZE
        ), 2)
    # Draw active moving tile
    draw_active(shapes)


def get_tile_at(x, y):
    for tile in tiles:
        if tile["x"] == x and tile["y"] == y:
            return tile
    return None


def can_move(direction, shape):
    if direction == "left":
        for piece in shape:
            if piece["x"] == 1:
                return False
            tile = get_tile_at(piece["x"] - 1, piece["y"])
            if tile and tile["space_filled"]:
                return False
    elif direction == "right":
        for piece in shape:
            if piece["x"] == GRID_WIDTH:
                return False
            tile = get_tile_at(piece["x"] + 1, piece["y"])
            if tile and tile["space_filled"]:
                return False
    elif direction == "down":
        for piece in shape:
            if piece["y"] == 1:
                return False
            tile = get_tile_at(piece["x"], piece["y"] - 1)
            if tile and tile["space_filled"]:
                return False
    elif direction == "up":
        for piece in shape:
            if piece["y"] == GRID_HEIGHT:
                return False
    return True


def change_tile(shape):
    global shapes
    for piece in shape:
        for tile in tiles:
            if tile["x"] == piece["x"] and tile["y"] == piece["y"]:
                tile["color"]= screen.blit(pygame.image.load("tetristestpiece.bmp"),(tile["x"],tile["y"]))
                tile["space_filled"] = True
                print(tile, piece)
    # Reset the shape's position to the top after it is fixed to the grid
    while can_move("up", shape):
        move_tile(0, 1, shape)

    # Center the shape using the top-left tile as the origin point
    min_x = min(piece["x"] for piece in shape)
    offset_x = (GRID_WIDTH // 2) - min_x
    for _ in range(abs(offset_x)):
        move_tile(1 if offset_x > 0 else -1, 0, shape)
    shapes = random.choice([square_shape, line_shape, t_shape, l_shape, reverse_l_shape, z_shape, reverse_z_shape])
    print(shapes)


def move_tile(dx, dy, shape):
    for piece in shape:
        new_x = piece["x"] + dx
        new_y = piece["y"] + dy

        if 1 <= new_x <= GRID_WIDTH:
            piece["x"] = new_x
        if 1 <= new_y <= GRID_HEIGHT:
            piece["y"] = new_y
    # Update the active tile position


def hard_drop():
    while can_move("down", shapes):
        move_tile(0, -1, shapes)
    change_tile(shapes)
    last_fall_time = current_time


init_grid()
print(tiles)
print(active_tile)
run = True
while run:
    current_time = pygame.time.get_ticks()

    # Check if the shape spawns inside any tiles with "space_filled": True
    inside_fixed_space = any(
        get_tile_at(piece["x"], piece["y"])["space_filled"]
        for piece in shapes
        if get_tile_at(piece["x"], piece["y"])
    )
    if inside_fixed_space:
        font = pygame.font.Font(None, 74)
        sub_font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 0, 0))
        sub_text = sub_font.render(f"Current Time: {current_time}", True, (255, 0, 0))
        screen.fill((0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        screen.blit(sub_text,
                    (SCREEN_WIDTH // 2 - sub_text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        run = False
        print("Current Time:", current_time)

    # print(current_time,last_fall_time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("")
            pygame.quit()
            exit()

        # Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if can_move("left", shapes):
                    move_tile(-1, 0, shapes)
            if event.key == pygame.K_RIGHT:
                if can_move("right", shapes):
                    move_tile(1, 0, shapes)
            if event.key == pygame.K_DOWN:
                if can_move("down", shapes):
                    move_tile(0, -1, shapes)
                    last_fall_time = current_time
            if event.key == pygame.K_r:
                rotated_shape = []
                pivot = shapes[0]
                for piece in shapes:
                    new_x = pivot["x"] - (piece["y"] - pivot["y"])
                    new_y = pivot["y"] + (piece["x"] - pivot["x"])
                    rotated_shape.append({"x": new_x, "y": new_y, "color": piece["color"]})

                if all(1 <= piece["x"] <= GRID_WIDTH and 1 <= piece["y"] <= GRID_HEIGHT and
                       (not get_tile_at(piece["x"], piece["y"]) or not get_tile_at(piece["x"], piece["y"])[
                           "space_filled"])
                       for piece in rotated_shape):
                    shapes = rotated_shape

            if event.key == pygame.K_e:
                rotated_shape = []
                pivot = shapes[0]
                for piece in shapes:
                    new_x = pivot["x"] + (piece["y"] - pivot["y"])
                    new_y = pivot["y"] - (piece["x"] - pivot["x"])
                    rotated_shape.append({"x": new_x, "y": new_y, "color": piece["color"]})

                if all(1 <= piece["x"] <= GRID_WIDTH and 1 <= piece["y"] <= GRID_HEIGHT and
                       (not get_tile_at(piece["x"], piece["y"]) or not get_tile_at(piece["x"], piece["y"])[
                           "space_filled"])
                       for piece in rotated_shape):
                    shapes = rotated_shape

            # dev mod to move the tile up
            if event.key == pygame.K_UP:
                move_tile(0, 1, shapes)
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                hard_drop()

                # Shift Down
    if current_time - last_fall_time > FALL_TIME:
        print("")
        print("New Turn")
        # print(tiles[space_right])
        # height map has been made
        if can_move("down", shapes):
            move_tile(0, -1, shapes)
        else:
            # detects when a tile hits the floor and where, and fixes it to the grid map.
            if skip1 >= 0:
                change_tile(shapes)

                skip1 += 1
            else:
                skip1 -= 1
        last_fall_time = current_time

    # Check for full rows
    full_rows = []
    for y in range(1, GRID_HEIGHT + 1):
        if all(get_tile_at(x, y)["space_filled"] for x in range(1, GRID_WIDTH + 1)):
            full_rows.append(y)

    # Shift rows down when a full row is cleared
    for row in full_rows:
        for y in range(row, GRID_HEIGHT + 1):
            for tile in tiles:
                if tile["y"] == y:
                    tile_above = get_tile_at(tile["x"], y + 1)
                    if tile_above:
                        tile["color"] = tile_above["color"]
                        tile["space_filled"] = tile_above["space_filled"]
                    else:
                        tile["color"] = (0, 0, 0)
                        tile["space_filled"] = False

    # Updates
    draw_grid()
    pygame.display.update()
    clock.tick(60)
