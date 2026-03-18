import pygame


class HitEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 12
        self.max_life = 12

    def update(self):
        self.life -= 1

    def is_alive(self):
        return self.life > 0

    def draw(self, screen):
        radius = max(2, self.life * 2)

        pygame.draw.circle(screen, (255, 220, 120), (self.x, self.y), radius, 2)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), max(1, radius // 2), 1)