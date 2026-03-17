import os
import pygame

BASE_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")

title_img = None
tank_menu_img = None

player_tank_up_img = None
player_tank_right_img = None
player_tank_left_img = None
player_tank_down_img = None

brick_img = None
steel_img = None
eagle_img = None
enemy_icon_img = None
player_icon_img = None
flag_img = None
bullet_img = None


def load():
    global title_img
    global tank_menu_img
    global player_tank_up_img
    global player_tank_right_img
    global player_tank_left_img
    global player_tank_down_img
    global brick_img
    global steel_img
    global eagle_img
    global enemy_icon_img
    global player_icon_img
    global flag_img
    global bullet_img

    bullet_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "bullet.png")
    ).convert_alpha()
    bullet_img = pygame.transform.scale(bullet_img, (12, 12))

    title_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "brick_title.png")
    ).convert_alpha()

    base_tank = pygame.image.load(
        os.path.join(IMAGE_DIR, "Tank_menu.png")
    ).convert_alpha()
    base_tank = pygame.transform.scale(base_tank, (32, 32))

    player_tank_up_img = base_tank
    player_tank_right_img = pygame.transform.rotate(base_tank, -90)
    player_tank_left_img = pygame.transform.rotate(base_tank, 90)
    player_tank_down_img = pygame.transform.rotate(base_tank, 180)

    tank_menu_img = pygame.transform.rotate(base_tank, -90)
    tank_menu_img = pygame.transform.scale(tank_menu_img, (60, 60))

    brick_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "brick.png")
    ).convert_alpha()
    brick_img = pygame.transform.scale(brick_img, (32, 32))

    steel_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "steel.png")
    ).convert_alpha()
    steel_img = pygame.transform.scale(steel_img, (32, 32))

    eagle_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "eagle.png")
    ).convert_alpha()
    eagle_img = pygame.transform.scale(eagle_img, (64, 64))

    enemy_icon_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "enemy_icon.png")
    ).convert_alpha()
    enemy_icon_img = pygame.transform.scale(enemy_icon_img, (24, 24))

    player_icon_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "player_icon.png")
    ).convert_alpha()
    player_icon_img = pygame.transform.scale(player_icon_img, (32, 32))

    flag_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "flag.png")
    ).convert_alpha()
    flag_img = pygame.transform.scale(flag_img, (40, 40))