import random
import pygame
import assets
import level
from bullet import Bullet


class Enemy:
    def __init__(self, x, y, fast=False):
        self.x = x
        self.y = y
        self.fast = fast

        self.size = int(level.TILE * 0.75)
        self.speed = 4 if fast else 2
        self.direction = "down"
        self.bullet = None
        self.is_alive = True

        self.change_dir_time = pygame.time.get_ticks()
        self.dir_interval = random.randint(700, 1500)

        self.last_shot_time = 0
        self.shot_cooldown = random.randint(1000, 2200)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def get_image(self):
        if self.fast:
            if self.direction == "up":
                img = assets.enemy_fast_tank_up_img
            elif self.direction == "right":
                img = assets.enemy_fast_tank_right_img
            elif self.direction == "left":
                img = assets.enemy_fast_tank_left_img
            else:
                img = assets.enemy_fast_tank_down_img
        else:
            if self.direction == "up":
                img = assets.enemy_tank_up_img
            elif self.direction == "right":
                img = assets.enemy_tank_right_img
            elif self.direction == "left":
                img = assets.enemy_tank_left_img
            else:
                img = assets.enemy_tank_down_img

        return pygame.transform.scale(img, (self.size, self.size))

    def draw(self, screen):
        if not self.is_alive:
            return

        screen.blit(self.get_image(), (self.x, self.y))

        if self.bullet and self.bullet.is_alive:
            self.bullet.draw(screen)

    def choose_new_direction(self):
        self.direction = random.choice(["up", "down", "left", "right"])
        self.change_dir_time = pygame.time.get_ticks()
        self.dir_interval = random.randint(700, 1500)

    def try_change_direction(self):
        now = pygame.time.get_ticks()
        if now - self.change_dir_time >= self.dir_interval:
            self.choose_new_direction()

    def move(self, field_x, field_y, blocked_rects):
        if not self.is_alive:
            return

        self.try_change_direction()

        new_x = self.x
        new_y = self.y

        if self.direction == "left":
            new_x -= self.speed
        elif self.direction == "right":
            new_x += self.speed
        elif self.direction == "up":
            new_y -= self.speed
        elif self.direction == "down":
            new_y += self.speed

        new_rect = pygame.Rect(new_x, new_y, self.size, self.size)

        can_move = level.can_move_to(new_x, new_y, self.size, field_x, field_y)

        for rect in blocked_rects:
            if new_rect.colliderect(rect):
                can_move = False
                break

        if can_move:
            self.x = new_x
            self.y = new_y
        else:
            self.choose_new_direction()

    def shoot(self):
        if not self.is_alive:
            return

        now = pygame.time.get_ticks()

        if now - self.last_shot_time < self.shot_cooldown:
            return

        if self.bullet and self.bullet.is_alive:
            return

        bullet_x = self.x
        bullet_y = self.y

        if self.direction == "up":
            bullet_x = self.x + self.size // 2 - 6
            bullet_y = self.y - 12
        elif self.direction == "down":
            bullet_x = self.x + self.size // 2 - 6
            bullet_y = self.y + self.size
        elif self.direction == "left":
            bullet_x = self.x - 12
            bullet_y = self.y + self.size // 2 - 6
        elif self.direction == "right":
            bullet_x = self.x + self.size
            bullet_y = self.y + self.size // 2 - 6

        self.bullet = Bullet(bullet_x, bullet_y, self.direction)
        self.last_shot_time = now
        self.shot_cooldown = random.randint(1000, 2200)

    def update_bullet(self, field_x, field_y, player_rect):
        if not self.bullet or not self.bullet.is_alive:
            return None

        hit = self.bullet.move(field_x, field_y)

        if hit == "eagle":
            return "game_over"

        if self.bullet and self.bullet.is_alive and self.bullet.get_rect().colliderect(player_rect):
            self.bullet.is_alive = False
            return "player_dead"

        if self.bullet and not self.bullet.is_alive:
            self.bullet = None

        return None

    def update(self, field_x, field_y, blocked_rects, player_rect):
        if not self.is_alive:
            return None

        self.move(field_x, field_y, blocked_rects)
        self.shoot()
        return self.update_bullet(field_x, field_y, player_rect)