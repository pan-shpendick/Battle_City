import pygame
import config
import assets

WHITE = (255,255,255)
BLACK = (0,0,0)

def draw(screen,font,WIDTH,HEIGHT):

    screen.fill(BLACK)

    title = font.render("НАЛАШТУВАННЯ",True,WHITE)

    screen.blit(title,(WIDTH//2-title.get_width()//2,HEIGHT*0.2))

    volume_text = font.render(f"Гучність: {config.volume}",True,WHITE)

    y = HEIGHT*0.5

    screen.blit(volume_text,(WIDTH//2-volume_text.get_width()//2,y))

    screen.blit(assets.tank_menu_img, (WIDTH // 2 - 300, y))


def input(event):

    if event.key == pygame.K_LEFT:

        if config.volume > 1:
            config.volume -= 1

    if event.key == pygame.K_RIGHT:

        if config.volume < 10:
            config.volume += 1