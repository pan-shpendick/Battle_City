import pygame
import assets

TILE = 50
SIDEBAR_W = 110

# # - кирпич
# S - сталь
# . - пусто
level_map = [
    "...................",
    ".##.##.##.##.##.##.",
    ".##.##.##.##.##.##.",
    ".##.##.##.##.##.##.",
    ".##.##.##.##.##.##.",
    ".##.##.##.##.##.##.",
    ".......##.##.......",
    "S.####.......####.S",
    ".......##.##.......",
    ".##.##.#####.##.##.",
    ".##.##.##.##.##.##.",
    ".##.##.##.##.##.##.",
    ".##.##.......##.##.",
    ".##.##.#####.##.##.",
    ".##.##.#...#.##.##.",
    ".......#...#.......",
]

FIELD_ROWS = len(level_map)
FIELD_COLS = len(level_map[0])

FIELD_W = FIELD_COLS * TILE
FIELD_H = FIELD_ROWS * TILE

# здоровье блоков
brick_health = {}
steel_health = {}


def init_level():
    brick_health.clear()
    steel_health.clear()

    for row_index, row in enumerate(level_map):
        for col_index, cell in enumerate(row):
            if cell == "#":
                brick_health[(col_index, row_index)] = 2
            elif cell == "S":
                steel_health[(col_index, row_index)] = 4


def scaled(img, w, h):
    return pygame.transform.scale(img, (w, h))


def get_game_area(screen_width, screen_height):
    game_h = screen_height
    game_w = int(game_h * 4 / 3)

    if game_w > screen_width:
        game_w = screen_width
        game_h = int(game_w * 3 / 4)

    game_x = (screen_width - game_w) // 2
    game_y = (screen_height - game_h) // 2
    return game_x, game_y, game_w, game_h


def draw_sidebar(screen, panel_x, game_y, game_h):
    pygame.draw.rect(screen, (140, 140, 140), (panel_x, game_y, SIDEBAR_W, game_h))

    enemy_icon = scaled(assets.enemy_icon_img, 28, 28)
    player_icon = scaled(assets.player_icon_img, 34, 34)
    flag_img = scaled(assets.flag_img, 42, 42)

    start_x = panel_x + 18
    start_y = game_y + 30

    for i in range(18):
        col = i % 2
        row = i // 2
        x = start_x + col * 30
        y = start_y + row * 32
        screen.blit(enemy_icon, (x, y))

    font_ui = pygame.font.SysFont("Courier New", 34, bold=True)

    text_ig = font_ui.render("ІГ", True, (0, 0, 0))
    text_2 = font_ui.render("2", True, (0, 0, 0))
    text_1 = font_ui.render("1", True, (0, 0, 0))

    screen.blit(text_ig, (panel_x + 18, game_y + 420))
    screen.blit(player_icon, (panel_x + 18, game_y + 470))
    screen.blit(text_2, (panel_x + 62, game_y + 480))

    screen.blit(flag_img, (panel_x + 18, game_y + 650))
    screen.blit(text_1, (panel_x + 62, game_y + 720))


def draw_tiles(screen, field_x, field_y):
    brick = scaled(assets.brick_img, TILE, TILE)
    steel = scaled(assets.steel_img, TILE, TILE)

    for (col_index, row_index), hp in brick_health.items():
        if hp > 0:
            x = field_x + col_index * TILE
            y = field_y + row_index * TILE
            screen.blit(brick, (x, y))

    for (col_index, row_index), hp in steel_health.items():
        if hp > 0:
            x = field_x + col_index * TILE
            y = field_y + row_index * TILE
            screen.blit(steel, (x, y))


def draw_eagle(screen, field_x, field_y):
    eagle_size = TILE * 2
    eagle = scaled(assets.eagle_img, eagle_size, eagle_size)

    offset_x = 75
    offset_y = 0

    eagle_x = field_x + 7 * TILE + offset_x
    eagle_y = field_y + 14 * TILE + offset_y

    screen.blit(eagle, (eagle_x, eagle_y))


def eagle_rect(field_x, field_y):
    offset_x = 75
    offset_y = 0

    return pygame.Rect(
        field_x + 7 * TILE + offset_x,
        field_y + 14 * TILE + offset_y,
        TILE * 2,
        TILE * 2
    )


def draw_level(screen, WIDTH, HEIGHT):
    game_x, game_y, game_w, game_h = get_game_area(WIDTH, HEIGHT)

    total_w = FIELD_W + SIDEBAR_W
    field_x = game_x + (game_w - total_w) // 2
    field_y = game_y + (game_h - FIELD_H) // 2
    panel_x = field_x + FIELD_W

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (140, 140, 140), (game_x, game_y, game_w, game_h))
    pygame.draw.rect(screen, (0, 0, 0), (field_x, field_y, FIELD_W, FIELD_H))

    draw_sidebar(screen, panel_x, game_y, game_h)
    draw_tiles(screen, field_x, field_y)
    draw_eagle(screen, field_x, field_y)

    return field_x, field_y


def is_blocking_cell(col, row):
    if brick_health.get((col, row), 0) > 0:
        return True
    if steel_health.get((col, row), 0) > 0:
        return True
    return False


def is_blocking(cell):
    return cell in ("#", "S")


def can_move_to(px, py, size, field_x, field_y):
    if px < field_x:
        return False
    if py < field_y:
        return False
    if px + size > field_x + FIELD_W:
        return False
    if py + size > field_y + FIELD_H:
        return False

    left_col = (px - field_x) // TILE
    right_col = (px - field_x + size - 1) // TILE
    top_row = (py - field_y) // TILE
    bottom_row = (py - field_y + size - 1) // TILE

    for row in range(top_row, bottom_row + 1):
        for col in range(left_col, right_col + 1):
            if is_blocking_cell(col, row):
                return False

    tank_rect = pygame.Rect(px, py, size, size)

    if tank_rect.colliderect(eagle_rect(field_x, field_y)):
        return False

    return True


def hit_block_at_pixel(px, py, bullet_w, bullet_h, field_x, field_y):
    left_col = (px - field_x) // TILE
    right_col = (px + bullet_w - 1 - field_x) // TILE
    top_row = (py - field_y) // TILE
    bottom_row = (py + bullet_h - 1 - field_y) // TILE

    for row in range(top_row, bottom_row + 1):
        for col in range(left_col, right_col + 1):
            if brick_health.get((col, row), 0) > 0:
                brick_health[(col, row)] -= 1
                return True, col, row

            if steel_health.get((col, row), 0) > 0:
                steel_health[(col, row)] -= 1
                return True, col, row

    return False, None, None