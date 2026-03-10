from pygame import *
import sys

import menu
import settings
import config
import assets
import level
import player

init()

screen = display.set_mode((0, 0), FULLSCREEN)
clock = time.Clock()

WIDTH, HEIGHT = screen.get_size()

assets.load()

menu_font = font.SysFont("Courier New", int(HEIGHT * 0.06), bold=True)

menu_offset = HEIGHT
animation_speed = 15

player1 = player.Player()
stage_start_time = 0

running = True

while running:
    screen.fill((0, 0, 0))

    if config.game_state == "menu":
        if not config.settings_mode:
            if menu_offset > 0:
                menu_offset -= animation_speed
            else:
                menu_offset = 0

            menu.draw(screen, menu_font, WIDTH, HEIGHT, menu_offset)
        else:
            settings.draw(screen, menu_font, WIDTH, HEIGHT)

    elif config.game_state == "stage_intro":
        screen.fill((120, 120, 120))
        text = menu_font.render("ПЕРШИЙ ЕТАП", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

        if time.get_ticks() - stage_start_time > 2000:
            config.game_state = "game"

    elif config.game_state == "game":
        field_x, field_y = level.draw_level(screen, WIDTH, HEIGHT)

        if not config.player_spawned:
            player1.spawn(field_x, field_y)
            config.player_spawned = True

        keys = key.get_pressed()
        player1.move(keys, field_x, field_y)
        player1.draw(screen)

    for e in event.get():
        if e.type == QUIT:
            running = False

        if e.type == KEYDOWN:
            if config.game_state == "menu":
                if config.settings_mode:
                    if e.key == K_ESCAPE:
                        config.settings_mode = False
                    else:
                        settings.input(e)
                else:
                    if e.key == K_ESCAPE:
                        running = False

                    if e.key == K_UP:
                        config.menu_selected = 0

                    if e.key == K_DOWN:
                        config.menu_selected = 1

                    if e.key == K_RETURN:
                        if config.menu_selected == 0:
                            config.settings_mode = False
                            config.game_state = "stage_intro"
                            config.player_spawned = False
                            stage_start_time = time.get_ticks()

                        elif config.menu_selected == 1:
                            config.settings_mode = True

            elif config.game_state == "stage_intro":
                if e.key == K_ESCAPE:
                    config.game_state = "menu"
                    config.settings_mode = False
                    menu_offset = HEIGHT

            elif config.game_state == "game":
                if e.key == K_ESCAPE:
                    config.game_state = "menu"
                    config.settings_mode = False
                    menu_offset = HEIGHT

    display.update()
    clock.tick(60)

quit()
sys.exit()