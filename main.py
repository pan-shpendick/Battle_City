from pygame import *
import sys
import os

init()


screen = display.set_mode((0, 0), FULLSCREEN)
display.set_caption("Батл Сіті")

clock = time.Clock()


WIDTH, HEIGHT = screen.get_size()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BASE_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE_DIR, "image")
title_path = os.path.join(IMAGE_DIR, "brick_title.png")
tank_path = os.path.join(IMAGE_DIR, "Tank_menu.png")


tank_img = image.load(tank_path).convert_alpha()
tank_img = transform.rotate(tank_img, -90)
tank_img = transform.scale(tank_img, (60, 60))

title_img = image.load(title_path).convert_alpha()
title_width = WIDTH * 0.6
scale_ratio = title_width / title_img.get_width()
title_height = title_img.get_height() * scale_ratio
title_img = transform.scale(title_img, (int(title_width), int(title_height)))

menu_font = font.SysFont("Courier New", int(HEIGHT * 0.06), bold=True)

selected = 0
running = True


menu_block_y = HEIGHT
animation_speed = 15


title_rel_y = HEIGHT * 0.15
option1_rel_y = HEIGHT * 0.75
option2_rel_y = HEIGHT * 0.85
cursor_offset_x = -80

while running:
    screen.fill(BLACK)


    if menu_block_y > 0:
        menu_block_y -= animation_speed
    else:
        menu_block_y = 0


    title_y = title_rel_y + menu_block_y
    screen.blit(title_img, (WIDTH // 2 - title_img.get_width() // 2, title_y))


    option1 = menu_font.render("1 ГРАВЕЦЬ", True, WHITE)
    option2 = menu_font.render("НАЛАШТУВАННЯ", True, WHITE)

    max_width = max(option1.get_width(), option2.get_width())
    menu_x = WIDTH // 2 - max_width // 2

    option1_y = option1_rel_y + menu_block_y
    option2_y = option2_rel_y + menu_block_y

    screen.blit(option1, (menu_x, option1_y))
    screen.blit(option2, (menu_x, option2_y))


    cursor_y = option1_y if selected == 0 else option2_y
    cursor_x = menu_x + cursor_offset_x
    screen.blit(tank_img, (cursor_x, cursor_y - 10))
    draw.rect(screen, (255, 200, 50), (cursor_x, cursor_y + 10, 30, 20))
    draw.rect(screen, (255, 200, 50), (cursor_x + 30, cursor_y + 17, 15, 6))


    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                running = False
            if e.key == K_UP:
                selected = 0
            if e.key == K_DOWN:
                selected = 1
            if e.key == K_RETURN:
                if selected == 0:
                    print("Старт гри")
                if selected == 1:
                    print("Налаштування")

    display.update()
    clock.tick(60)

quit()
sys.exit()