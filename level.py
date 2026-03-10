import pygame
import assets

TILE = 32
FIELD_COLS = 26
FIELD_ROWS = 26

FIELD_W = FIELD_COLS * TILE
FIELD_H = FIELD_ROWS * TILE
SIDEBAR_W = 160


def brick_rect(screen, field_x, field_y, tx, ty, w, h):
    for y in range(h):
        for x in range(w):
            screen.blit(
                assets.brick_img,
                (field_x + (tx + x) * TILE, field_y + (ty + y) * TILE)
            )


def steel_rect(screen, field_x, field_y, tx, ty, w, h):
    for y in range(h):
        for x in range(w):
            screen.blit(
                assets.steel_img,
                (field_x + (tx + x) * TILE, field_y + (ty + y) * TILE)
            )


def draw_sidebar(screen, panel_x, field_y, HEIGHT):
    pygame.draw.rect(screen, (140, 140, 140), (panel_x, 0, SIDEBAR_W, HEIGHT))

    # Иконки врагов справа
    start_x = panel_x + 42
    start_y = field_y + 36

    for i in range(16):
        col = i % 2
        row = i // 2
        x = start_x + col * 34
        y = start_y + row * 39
        screen.blit(assets.enemy_icon_img, (x, y))

    font_ui = pygame.font.SysFont("Courier New", 34, bold=True)

    text_ig = font_ui.render("ІГ", True, (0, 0, 0))
    text_2 = font_ui.render("2", True, (0, 0, 0))
    text_1 = font_ui.render("1", True, (0, 0, 0))

    screen.blit(text_ig, (panel_x + 55, field_y + 470))
    screen.blit(assets.player_icon_img, (panel_x + 50, field_y + 515))
    screen.blit(text_2, (panel_x + 96, field_y + 528))

    screen.blit(assets.flag_img, (panel_x + 48, field_y + 670))
    screen.blit(text_1, (panel_x + 96, field_y + 748))


def draw_level(screen, WIDTH, HEIGHT):

    FIELD_W = FIELD_COLS * TILE
    FIELD_H = FIELD_ROWS * TILE
    SIDEBAR_W = 160

    total_w = FIELD_W + SIDEBAR_W

    field_x = (WIDTH - total_w) // 2
    field_y = (HEIGHT - FIELD_H) // 2

    panel_x = field_x + FIELD_W
    border = 20

    # Сначала чёрный фон
    screen.fill((0, 0, 0))

    # Потом серая рамка вокруг карты
    pygame.draw.rect(
        screen,
        (140, 140, 140),
        (
            field_x - border,
            field_y - border,
            FIELD_W + border * 2,
            FIELD_H + border * 2
        )
    )

    # Потом чёрное игровое поле
    pygame.draw.rect(screen, (0, 0, 0), (field_x, field_y, FIELD_W, FIELD_H))

    # Правая панель
    draw_sidebar(screen, panel_x, field_y, HEIGHT)

    # ===== РИСУЕМ КАРТУ =====
    brick_rect(screen, field_x, field_y, 2, 1, 3, 10)
    brick_rect(screen, field_x, field_y, 7, 1, 3, 10)

    brick_rect(screen, field_x, field_y, 12, 1, 3, 4)
    brick_rect(screen, field_x, field_y, 12, 7, 3, 3)

    brick_rect(screen, field_x, field_y, 17, 1, 3, 10)
    brick_rect(screen, field_x, field_y, 22, 1, 3, 10)

    brick_rect(screen, field_x, field_y, 11, 1, 1, 7)
    brick_rect(screen, field_x, field_y, 15, 1, 1, 7)

    steel_rect(screen, field_x, field_y, 13, 5, 2, 2)

    brick_rect(screen, field_x, field_y, 11, 11, 3, 2)
    brick_rect(screen, field_x, field_y, 15, 11, 3, 2)

    brick_rect(screen, field_x, field_y, 4, 14, 4, 2)
    brick_rect(screen, field_x, field_y, 18, 14, 4, 2)

    steel_rect(screen, field_x, field_y, 0, 14, 2, 2)
    steel_rect(screen, field_x, field_y, 25, 14, 2, 2)

    brick_rect(screen, field_x, field_y, 2, 18, 3, 8)
    brick_rect(screen, field_x, field_y, 7, 18, 3, 8)
    brick_rect(screen, field_x, field_y, 18, 18, 3, 8)
    brick_rect(screen, field_x, field_y, 22, 18, 3, 8)

    brick_rect(screen, field_x, field_y, 11, 16, 2, 7)
    brick_rect(screen, field_x, field_y, 15, 16, 2, 7)
    brick_rect(screen, field_x, field_y, 12, 16, 3, 2)
    brick_rect(screen, field_x, field_y, 12, 22, 3, 1)

    # ===== ОРЁЛ =====
    eagle_x = field_x + 13 * TILE - assets.eagle_img.get_width() // 2
    eagle_y = field_y + 24 * TILE

    screen.blit(assets.eagle_img, (eagle_x, eagle_y))

    brick_rect(screen, field_x, field_y, 12, 23, 1, 2)
    brick_rect(screen, field_x, field_y, 14, 23, 1, 2)
    brick_rect(screen, field_x, field_y, 11, 25, 2, 1)
    brick_rect(screen, field_x, field_y, 14, 25, 2, 1)

    return field_x, field_y


def get_collision_rects(field_x, field_y):
    rects = []

    def add_rect(tx, ty, w, h):
        rects.append(
            pygame.Rect(
                field_x + tx * TILE,
                field_y + ty * TILE,
                w * TILE,
                h * TILE
            )
        )

    add_rect(2, 1, 3, 10)
    add_rect(7, 1, 3, 10)

    add_rect(12, 1, 3, 4)
    add_rect(12, 7, 3, 3)

    add_rect(17, 1, 3, 10)
    add_rect(22, 1, 3, 10)

    add_rect(11, 1, 1, 7)
    add_rect(15, 1, 1, 7)

    add_rect(13, 5, 2, 2)

    add_rect(11, 11, 3, 2)
    add_rect(15, 11, 3, 2)

    add_rect(4, 14, 4, 2)
    add_rect(18, 14, 4, 2)

    add_rect(0, 14, 2, 2)
    add_rect(25, 14, 2, 2)

    add_rect(2, 18, 3, 8)
    add_rect(7, 18, 3, 8)
    add_rect(18, 18, 3, 8)
    add_rect(22, 18, 3, 8)

    add_rect(11, 16, 2, 7)
    add_rect(15, 16, 2, 7)
    add_rect(12, 16, 3, 2)
    add_rect(12, 22, 3, 1)

    add_rect(12, 23, 1, 2)
    add_rect(14, 23, 1, 2)
    add_rect(11, 25, 2, 1)
    add_rect(14, 25, 2, 1)

    return rects


def can_move_to(px, py, size, field_x, field_y):
    tank_rect = pygame.Rect(px, py, size, size)

    # границы поля
    if tank_rect.left < field_x:
        return False
    if tank_rect.top < field_y:
        return False
    if tank_rect.right > field_x + FIELD_W:
        return False
    if tank_rect.bottom > field_y + FIELD_H:
        return False

    for rect in get_collision_rects(field_x, field_y):
        if tank_rect.colliderect(rect):
            return False

    return True