import pygame
import assets
import level
from bullet import Bullet
from effects import HitEffect


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 4
        self.size = int(level.TILE * 0.75)
        self.direction = "up"
        self.bullet = None
        self.effects = []
        self.is_alive = True

        self.shot_cooldown = 500
        self.last_shot_time = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def spawn(self, field_x, field_y):
        self.x = field_x + 6 * level.TILE
        self.y = field_y + 15 * level.TILE
        self.direction = "up"
        self.bullet = None
        self.effects = []
        self.last_shot_time = 0
        self.is_alive = True

    def get_image(self):
        if self.direction == "up":
            img = assets.player_tank_up_img
        elif self.direction == "right":
            img = assets.player_tank_right_img
        elif self.direction == "left":
            img = assets.player_tank_left_img
        else:
            img = assets.player_tank_down_img

        return pygame.transform.scale(img, (self.size, self.size))

    def draw(self, screen):
        if self.is_alive:
            screen.blit(self.get_image(), (self.x, self.y))

        if self.bullet and self.bullet.is_alive:
            self.bullet.draw(screen)

        for effect in self.effects:
            effect.draw(screen)

    def move(self, keys, field_x, field_y):
        if not self.is_alive:
            return

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

    def update_bullet(self, field_x, field_y, enemies):
        if self.bullet and self.bullet.is_alive:
            hit, _, _ = self.bullet.move(field_x, field_y)

            if hit:
                effect_x = self.bullet.x + self.bullet.width // 2
                effect_y = self.bullet.y + self.bullet.height // 2
                self.effects.append(HitEffect(effect_x, effect_y))

                if hit == "eagle":
                    return "game_over"

            if self.bullet and self.bullet.is_alive:
                bullet_rect = self.bullet.get_rect()
                for bot in enemies:
                    if bot.is_alive and bullet_rect.colliderect(bot.get_rect()):
                        bot.is_alive = False
                        self.bullet.is_alive = False
                        effect_x = bot.x + bot.size // 2
                        effect_y = bot.y + bot.size // 2
                        self.effects.append(HitEffect(effect_x, effect_y))
                        break

        new_effects = []
        for effect in self.effects:
            effect.update()
            if effect.is_alive():
                new_effects.append(effect)
        self.effects = new_effects

        return None