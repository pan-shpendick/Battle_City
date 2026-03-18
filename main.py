from pygame import *
import sys
import random

import menu
import settings
import config
import assets
import level
import player
import enemy

init()

screen = display.set_mode((0, 0), FULLSCREEN)
clock = time.Clock()

WIDTH, HEIGHT = screen.get_size()

assets.load()

menu_font = font.SysFont("Courier New", int(HEIGHT * 0.06), bold=True)
small_font = font.SysFont("Courier New", 36, bold=True)
big_font = font.SysFont("Courier New", 48, bold=True)

menu_offset = HEIGHT
animation_speed = 15

player1 = player.Player()
stage_start_time = 0
enemies = []

running = True


def spawn_enemy(field_x, field_y, enemies, player1):
    spawn_points = [
        (field_x + 1 * level.TILE, field_y + 1 * level.TILE),
        (field_x + 8 * level.TILE, field_y + 1 * level.TILE),
        (field_x + 15 * level.TILE, field_y + 1 * level.TILE),
    ]

    random.shuffle(spawn_points)

    for x, y in spawn_points:
        temp_enemy = enemy.Enemy(x, y)
        enemy_rect = temp_enemy.get_rect()

        if not level.can_move_to(x, y, temp_enemy.size, field_x, field_y):
            continue

        if enemy_rect.colliderect(player1.get_rect()):
            continue

        blocked = False
        for bot in enemies:
            if bot.is_alive and enemy_rect.colliderect(bot.get_rect()):
                blocked = True
                break

        if not blocked:
            enemies.append(temp_enemy)
            return True

    return False


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
            enemies = []
            config.enemy_spawned_count = 0
            config.enemy_spawn_time = time.get_ticks()

        # постепенный спавн
        now = time.get_ticks()
        alive_enemies = [bot for bot in enemies if bot.is_alive]

        if config.enemy_spawned_count < config.enemy_max_count:
            if now - config.enemy_spawn_time > 2000:
                spawned = spawn_enemy(field_x, field_y, alive_enemies, player1)
                if spawned:
                    enemies = alive_enemies
                    config.enemy_spawned_count += 1
                    config.enemy_spawn_time = now

        keys = key.get_pressed()
        player1.move(keys, field_x, field_y)

        result = player1.update_bullet(field_x, field_y, alive_enemies)
        if result == "game_over":
            config.game_over = True
            config.game_state = "game_over_scroll"
            config.game_over_start_time = time.get_ticks()

        player1.draw(screen)

        updated_enemies = []
        for i, bot in enumerate(alive_enemies):
            other_rects = []

            for j, other_bot in enumerate(alive_enemies):
                if i != j and other_bot.is_alive:
                    other_rects.append(other_bot.get_rect())

            if player1.is_alive:
                other_rects.append(player1.get_rect())

            enemy_result = bot.update(field_x, field_y, other_rects, player1.get_rect())
            bot.draw(screen)

            if enemy_result == "game_over" or enemy_result == "player_dead":
                player1.is_alive = False
                config.game_over = True
                config.game_state = "game_over_scroll"
                config.game_over_start_time = time.get_ticks()

            if bot.is_alive:
                updated_enemies.append(bot)

        enemies = updated_enemies

    elif config.game_state == "game_over_scroll":
        field_x, field_y = level.draw_level(screen, WIDTH, HEIGHT)
        player1.draw(screen)

        for bot in enemies:
            if bot.is_alive:
                bot.draw(screen)

        game_over_text = menu_font.render("КІНЕЦЬ ГРИ", True, (255, 60, 60))

        elapsed = time.get_ticks() - config.game_over_start_time
        start_y = HEIGHT
        target_y = HEIGHT // 2 - game_over_text.get_height() // 2
        speed = 8

        current_y = start_y - (elapsed // 10) * speed
        if current_y < target_y:
            current_y = target_y

        screen.blit(
            game_over_text,
            (WIDTH // 2 - game_over_text.get_width() // 2, current_y)
        )

        if current_y == target_y and elapsed > 2500:
            config.game_state = "battle_stats"
            config.game_over_start_time = time.get_ticks()

    elif config.game_state == "battle_stats":
        screen.fill((0, 0, 0))

        title_red = big_font.render("РЕКОРД", True, (255, 80, 40))
        score_gold = big_font.render("20000", True, (255, 180, 80))
        stage_white = big_font.render("ЕТАП", True, (255, 255, 255))
        stage_num = big_font.render("1", True, (255, 255, 255))
        player_title = big_font.render("1 ГРАВЕЦЬ", True, (255, 80, 40))

        screen.blit(title_red, (WIDTH // 2 - 180, 60))
        screen.blit(score_gold, (WIDTH // 2 + 70, 60))
        screen.blit(stage_white, (WIDTH // 2 - 95, 120))
        screen.blit(stage_num, (WIDTH // 2 + 75, 120))
        screen.blit(player_title, (WIDTH // 2 - 260, 200))

        enemy_icon = transform.scale(assets.enemy_icon_img, (36, 36))
        row_y = [310, 410, 510, 610]

        for y in row_y:
            left_zero = small_font.render("0", True, (255, 255, 255))
            points = small_font.render("ОЧК", True, (255, 255, 255))
            right_zero = small_font.render("0", True, (255, 255, 255))

            screen.blit(left_zero, (WIDTH // 2 - 170, y))
            screen.blit(points, (WIDTH // 2 - 110, y))
            screen.blit(right_zero, (WIDTH // 2 + 40, y))

        screen.blit(enemy_icon, (WIDTH // 2 + 110, row_y[0] - 5))
        screen.blit(enemy_icon, (WIDTH // 2 + 110, row_y[1] - 5))
        screen.blit(enemy_icon, (WIDTH // 2 + 110, row_y[2] - 5))
        screen.blit(enemy_icon, (WIDTH // 2 + 110, row_y[3] - 5))

        draw.line(screen, (255, 255, 255), (WIDTH // 2 - 10, 705), (WIDTH // 2 + 220, 705), 4)

        total_text = big_font.render("ІТОГ 0", True, (255, 255, 255))
        screen.blit(total_text, (WIDTH // 2 - 120, 730))

        if time.get_ticks() - config.game_over_start_time > 3500:
            config.game_state = "final_end"
            config.game_over_start_time = time.get_ticks()

    elif config.game_state == "final_end":
        screen.fill((0, 0, 0))

        end_img = assets.final_end_img
        img_x = WIDTH // 2 - end_img.get_width() // 2
        img_y = HEIGHT // 2 - end_img.get_height() // 2
        screen.blit(end_img, (img_x, img_y))

        if time.get_ticks() - config.game_over_start_time > 2500:
            config.game_state = "menu"
            config.settings_mode = False
            config.player_spawned = False
            config.game_over = False
            menu_offset = HEIGHT

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
                            config.game_over = False
                            config.enemy_spawned_count = 0
                            level.init_level()
                            stage_start_time = time.get_ticks()
                        elif config.menu_selected == 1:
                            config.settings_mode = True

            elif config.game_state == "stage_intro":
                if e.key == K_ESCAPE:
                    running = False

            elif config.game_state == "game":
                if e.key == K_ESCAPE:
                    running = False

                if e.key == K_SPACE:
                    player1.shoot()

            elif config.game_state == "game_over_scroll":
                if e.key == K_ESCAPE:
                    running = False

            elif config.game_state == "battle_stats":
                if e.key == K_ESCAPE:
                    running = False

            elif config.game_state == "final_end":
                if e.key == K_ESCAPE:
                    running = False

    display.update()
    clock.tick(60)

quit()
sys.exit()