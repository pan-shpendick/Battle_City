import pygame
import assets
import level

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 4
        self.direction = "up"
        self.size = 32

    def spawn(self, field_x, field_y):
        self.x = field_x + 10 * 32
        self.y = field_y + 24 * 32
        self.direction = "up"

    def draw(self, screen):
        if self.direction == "up":
            img = assets.player_tank_up_img
        elif self.direction == "right":
            img = assets.player_tank_right_img
        elif self.direction == "left":
            img = assets.player_tank_left_img
        else:
            img = assets.player_tank_down_img

        screen.blit(img, (self.x, self.y))

    def move(self, keys, field_x, field_y):
        new_x = self.x
        new_y = self.y

        if keys[pygame.K_LEFT]:
            new_x -= self.speed
            self.direction = "left"
        elif keys[pygame.K_RIGHT]:
            new_x += self.speed
            self.direction = "right"
        elif keys[pygame.K_UP]:
            new_y -= self.speed
            self.direction = "up"
        elif keys[pygame.K_DOWN]:
            new_y += self.speed
            self.direction = "down"

        if level.can_move_to(new_x, new_y, self.size, field_x, field_y):
            self.x = new_x
            self.y = new_y