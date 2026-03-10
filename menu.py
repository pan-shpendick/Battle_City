import pygame
import config
import assets

WHITE = (255, 255, 255)

def draw(screen, font, WIDTH, HEIGHT, menu_offset):
    title_rel_y = HEIGHT * 0.15
    option1_rel_y = HEIGHT * 0.75
    option2_rel_y = HEIGHT * 0.85

    title_y = title_rel_y + menu_offset

    if assets.title_img is not None:
        screen.blit(
            assets.title_img,
            (WIDTH // 2 - assets.title_img.get_width() // 2, title_y)
        )

    option1 = font.render("1 ГРАВЕЦЬ", True, WHITE)
    option2 = font.render("НАЛАШТУВАННЯ", True, WHITE)

    max_width = max(option1.get_width(), option2.get_width())
    menu_x = WIDTH // 2 - max_width // 2

    option1_y = option1_rel_y + menu_offset
    option2_y = option2_rel_y + menu_offset

    screen.blit(option1, (menu_x, option1_y))
    screen.blit(option2, (menu_x, option2_y))

    cursor_y = option1_y if config.menu_selected == 0 else option2_y
    screen.blit(assets.tank_menu_img, (menu_x - 80, cursor_y - 10))