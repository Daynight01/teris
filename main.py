import pygame
import random
# I am Person 2.
pygame.init()

BACKGROUND = pygame.image.load("rat.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (900, 900))
BOARD = pygame.image.load("maryo.jpg")
BOARD2 = pygame.image.load("blue_piece.bmp")
ACTIVE = pygame.image.load("red_piece.bmp")

BOARD = pygame.transform.scale(BOARD, (45,45))
BOARD.set_alpha(100)


SCREEN_HEIGHT = 900
SCREEN_WIDTH = 900
TILE_SIZE = 45
GRID_WIDTH = 10
GRID_HEIGHT = 20

SCORE = 0

FALL_TIME = 1000 - SCORE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

move_hist_x = 0
move_hist_y = 0

skip1 = 1
tiles = []
new_tile = {"x": 1, "y": GRID_HEIGHT, "color": (255, 0, 0)}
active_tile = {"x": 1, "y": GRID_HEIGHT, "color": (255, 0, 0)}
last_fall_time = pygame.time.get_ticks()

# Person 1
def create_shape(relative_coords, color, base_x=GRID_WIDTH // 2, base_y=GRID_HEIGHT):
    return [{"x": base_x + coord[0], "y": base_y + coord[1], "color": color} for coord in relative_coords]


square_shape = create_shape([(0, 0), (1, 0), (0, -1), (1, -1)], "yellow_piece.jpg")
line_shape = create_shape([(0, 0), (1, 0), (2, 0), (3, 0)], "blue_piece.bmp")
t_shape = create_shape([(0, 0), (1, 0), (2, 0), (1, -1)], "pourple_piece.jpg")
l_shape = create_shape([(0, 0), (0, -1), (0, -2), (1, 0)], "orange_piece.jpg")
reverse_l_shape = create_shape([(1, 0), (1, -1), (1, -2), (0, 0)], "pink_piece.jpg")
z_shape = create_shape([(0, 0), (1, 0), (1, -1), (2, -1)], "green_piece.jpg")
reverse_z_shape = create_shape([(2, 0), (1, 0), (1, -1), (0, -1)], "red_piece.bmp")


shapes = random.choice([square_shape, line_shape, t_shape, l_shape, reverse_l_shape, z_shape, reverse_z_shape])
print(shapes)

# Person 2
def init_grid():
    global tiles
    tiles = []
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            tiles.append(
                {"x": x + 1, "y": y + 1, "color": BOARD, "space_filled": False})

# Person 2 and 1
def draw_active(shape):
    for piece in shape:
        screen.blit(pygame.image.load(piece["color"]), (
            (piece["x"] - 1) * TILE_SIZE + 225,
            (GRID_HEIGHT - piece["y"]) * TILE_SIZE))

# Person 2
def draw_grid():
    screen.blit(BACKGROUND, (0, 0))
    for tile in tiles:
        x, y, color = tile["x"], tile["y"], tile["color"]
        screen.blit(tile["color"], (
            (x - 1) * TILE_SIZE + 225,
            (GRID_HEIGHT - y) * TILE_SIZE))
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(
            (x - 1) * TILE_SIZE + 225,
            (GRID_HEIGHT - y) * TILE_SIZE,
            TILE_SIZE, TILE_SIZE
        ), 2)
    # Draw active moving tile
    draw_active(shapes)

# Person 2
def get_tile_at(x, y):
    for tile in tiles:
        if tile["x"] == x and tile["y"] == y:
            return tile
    return None

# Person 1
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

# Person 1 and 2
def move_tile(dx, dy, shape):
    global move_hist_x, move_hist_y
    for piece in shape:
        new_x = piece["x"] + dx
        new_y = piece["y"] + dy

        if 1 <= new_x <= GRID_WIDTH:
            piece["x"] = new_x
        if 1 <= new_y <= GRID_HEIGHT:
            piece["y"] = new_y
    move_hist_x += dx
    move_hist_y += dy
    # Update the active tile position

# Person 1
def rows():
    global SCORE, move_hist_y, shapes
    # Check for full rows
    full_rows = []

    for y in range(1, GRID_HEIGHT + 1):
        if all(get_tile_at(x, y)["space_filled"] for x in range(1, GRID_WIDTH + 1)):
            full_rows.append(y)
            SCORE += 10
    print(full_rows)
    move_hist_y -= len(full_rows)
    # Shift rows down when a full row is cleared
    for row in full_rows:
        if can_move("up", shapes):
            move_tile(0,1,shapes)

        for y in range(row, GRID_HEIGHT + 1):

            for tile in tiles:
                if tile["y"] == y:
                    tile_above = get_tile_at(tile["x"], y + 1)
                    if tile_above:
                        tile["color"] = tile_above["color"]
                        tile["space_filled"] = tile_above["space_filled"]
                    else:
                        tile["color"] = tile["color"]
                        tile["space_filled"] = False

# Person 2 and 1
def change_tile(shape):
    global shapes
    global SCORE
    global move_hist_x, move_hist_y, FALL_TIME
    for piece in shape:
        for tile in tiles:
            if tile["x"] == piece["x"] and tile["y"] == piece["y"]:
                tile["color"] = pygame.image.load(piece["color"])
                tile["space_filled"] = True
                print(tile, piece)
    # Reset the shape's position to the top after it is fixed to the grid
    rows()
    print(move_hist_x, move_hist_y)
    move_tile(-move_hist_x, -move_hist_y, shape)

    SCORE += 1
    move_hist_x = 0
    move_hist_y = 0
    shapes.clear()
    square_shape = create_shape([(0, 0), (1, 0), (0, -1), (1, -1)], "yellow_piece.jpg")
    line_shape = create_shape([(0, 0), (1, 0), (2, 0), (3, 0)], "blue_piece.bmp")
    t_shape = create_shape([(0, 0), (1, 0), (2, 0), (1, -1)], "pourple_piece.jpg")
    l_shape = create_shape([(0, 0), (0, -1), (0, -2), (1, 0)], "orange_piece.jpg")
    reverse_l_shape = create_shape([(1, 0), (1, -1), (1, -2), (0, 0)], "pink_piece.jpg")
    z_shape = create_shape([(0, 0), (1, 0), (1, -1), (2, -1)], "green_piece.jpg")
    reverse_z_shape = create_shape([(2, 0), (1, 0), (1, -1), (0, -1)], "red_piece.bmp")
    shapes = random.choice([square_shape, line_shape, t_shape, l_shape, reverse_l_shape, z_shape, reverse_z_shape])
    FALL_TIME = 1000 - SCORE
    print(shapes)

# Person 2
def hard_drop():
    global last_fall_time, move_hist_y
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
    # Person 1
    inside_fixed_space = any(
        get_tile_at(piece["x"], piece["y"])["space_filled"]
        for piece in shapes
        if get_tile_at(piece["x"], piece["y"])
    )
    # Person 1
    if inside_fixed_space:
        font = pygame.font.Font(None, 74)
        sub_font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 0, 0))
        sub_text = sub_font.render(f"Final Score: {SCORE}", True, (255, 0, 0))
        screen.fill((0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        screen.blit(sub_text,
                    (SCREEN_WIDTH // 2 - sub_text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        run = False
        print("Current Time:", current_time)

    # Person 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("")
            pygame.quit()
            exit()

        # Movement
        # Person 2 and 1
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
    # Person 2 and 1
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
    # Person 1
    full_rows = []
    for y in range(1, GRID_HEIGHT + 1):
        if all(get_tile_at(x, y)["space_filled"] for x in range(1, GRID_WIDTH + 1)):
            full_rows.append(y)
            SCORE += 10
    move_hist_y -= len(full_rows)
    # Shift rows down when a full row is cleared
    # Person 1
    for row in full_rows:
        if can_move("up", shapes):
            move_tile(0,1,shapes)
        for y in range(row, GRID_HEIGHT + 1):

            for tile in tiles:
                if tile["y"] == y:
                    tile_above = get_tile_at(tile["x"], y + 1)
                    if tile_above:
                        tile["color"] = tile_above["color"]
                        tile["space_filled"] = tile_above["space_filled"]
                    else:
                        tile["color"] = tile["color"]
                        tile["space_filled"] = False

    # Updates
    draw_grid()
    pygame.display.update()
    clock.tick(60)
