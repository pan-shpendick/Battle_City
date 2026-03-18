import pygame
import assets
import level


class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 6
        self.width = 12
        self.height = 12
        self.is_alive = True

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, field_x, field_y):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed

        if self.x < field_x or self.y < field_y:
            self.is_alive = False
            return False, None, None

        if self.x + self.width > field_x + level.FIELD_W:
            self.is_alive = False
            return False, None, None

        if self.y + self.height > field_y + level.FIELD_H:
            self.is_alive = False
            return False, None, None

        hit, col, row = level.hit_block_at_pixel(
            self.x, self.y, self.width, self.height, field_x, field_y
        )
        if hit:
            self.is_alive = False
            return True, col, row

        if self.get_rect().colliderect(level.eagle_rect(field_x, field_y)):
            self.is_alive = False
            return "eagle", None, None

        return False, None, None

    def get_image(self):
        img = pygame.transform.scale(assets.bullet_img, (self.width, self.height))

        if self.direction == "up":
            return img
        elif self.direction == "right":
            return pygame.transform.rotate(img, -90)
        elif self.direction == "left":
            return pygame.transform.rotate(img, 90)
        elif self.direction == "down":
            return pygame.transform.rotate(img, 180)

        return img

    def draw(self, screen):
        screen.blit(self.get_image(), (self.x, self.y))