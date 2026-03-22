import os
import pygame
import config

BASE_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")

title_img = None
tank_menu_img = None

player_tank_up_img = None
player_tank_right_img = None
player_tank_left_img = None
player_tank_down_img = None

enemy_tank_up_img = None
enemy_tank_right_img = None
enemy_tank_left_img = None
enemy_tank_down_img = None

enemy_fast_tank_up_img = None
enemy_fast_tank_right_img = None
enemy_fast_tank_left_img = None
enemy_fast_tank_down_img = None

brick_img = None
steel_img = None
eagle_img = None
enemy_icon_img = None
player_icon_img = None
flag_img = None
bullet_img = None
final_end_img = None

hit_frames = []

start_sound = None
concrete_sound = None
shot_sound = None
enemy_death_sound = None
died_sound = None
defeat_sound = None


def update_sound_volume():
    volume_value = config.volume / 10.0

    if start_sound:
        start_sound.set_volume(volume_value)
    if concrete_sound:
        concrete_sound.set_volume(volume_value)
    if shot_sound:
        shot_sound.set_volume(volume_value)
    if enemy_death_sound:
        enemy_death_sound.set_volume(volume_value)
    if died_sound:
        died_sound.set_volume(volume_value)
    if defeat_sound:
        defeat_sound.set_volume(volume_value)


def load():
    global title_img
    global tank_menu_img

    global player_tank_up_img
    global player_tank_right_img
    global player_tank_left_img
    global player_tank_down_img

    global enemy_tank_up_img
    global enemy_tank_right_img
    global enemy_tank_left_img
    global enemy_tank_down_img

    global enemy_fast_tank_up_img
    global enemy_fast_tank_right_img
    global enemy_fast_tank_left_img
    global enemy_fast_tank_down_img

    global brick_img
    global steel_img
    global eagle_img
    global enemy_icon_img
    global player_icon_img
    global flag_img
    global bullet_img
    global final_end_img
    global hit_frames

    global start_sound
    global concrete_sound
    global shot_sound
    global enemy_death_sound
    global died_sound
    global defeat_sound

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

    base_enemy_tank = pygame.image.load(
        os.path.join(IMAGE_DIR, "enemy_tank.png")
    ).convert_alpha()
    base_enemy_tank = pygame.transform.scale(base_enemy_tank, (32, 32))

    enemy_tank_up_img = base_enemy_tank
    enemy_tank_right_img = pygame.transform.rotate(base_enemy_tank, -90)
    enemy_tank_left_img = pygame.transform.rotate(base_enemy_tank, 90)
    enemy_tank_down_img = pygame.transform.rotate(base_enemy_tank, 180)

    base_fast_enemy_tank = pygame.image.load(
        os.path.join(IMAGE_DIR, "enemy_fast_tank.png")
    ).convert_alpha()
    base_fast_enemy_tank = pygame.transform.scale(base_fast_enemy_tank, (32, 32))

    enemy_fast_tank_up_img = base_fast_enemy_tank
    enemy_fast_tank_right_img = pygame.transform.rotate(base_fast_enemy_tank, -90)
    enemy_fast_tank_left_img = pygame.transform.rotate(base_fast_enemy_tank, 90)
    enemy_fast_tank_down_img = pygame.transform.rotate(base_fast_enemy_tank, 180)

    brick_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "brick.png")
    ).convert_alpha()

    steel_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "steel.png")
    ).convert_alpha()

    eagle_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "eagle.png")
    ).convert_alpha()

    enemy_icon_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "enemy_icon.png")
    ).convert_alpha()

    player_icon_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "player_icon.png")
    ).convert_alpha()



    flag_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "flag.png")
    ).convert_alpha()

    bullet_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "bullet.png")
    ).convert_alpha()

    final_end_img = pygame.image.load(
        os.path.join(IMAGE_DIR, "final_end.png")
    ).convert_alpha()

    hit_frames = [
        pygame.image.load(os.path.join(IMAGE_DIR, "hit_1.png")).convert_alpha(),
        pygame.image.load(os.path.join(IMAGE_DIR, "hit_2.png")).convert_alpha(),
        pygame.image.load(os.path.join(IMAGE_DIR, "hit_3.png")).convert_alpha(),
    ]

    start_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "start.wav"))
    concrete_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "concrete.wav"))
    shot_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "shot.wav"))
    enemy_death_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "enemy_death.wav"))
    died_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "died.wav"))
    defeat_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "defeat.wav"))

    update_sound_volume()