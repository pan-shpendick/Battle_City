import pygame
import assets


class HitEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.frames = [
            pygame.transform.scale(assets.hit_frames[0], (24, 24)),
            pygame.transform.scale(assets.hit_frames[1], (32, 32)),
            pygame.transform.scale(assets.hit_frames[2], (40, 40)),
        ]

        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 40
        self.alive = True

    def update(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > self.frame_delay:
            self.frame_index += 1
            self.last_update = now

            if self.frame_index >= len(self.frames):
                self.alive = False

    def draw(self, screen):
        if self.alive:
            img = self.frames[self.frame_index]
            screen.blit(
                img,
                (self.x - img.get_width() // 2, self.y - img.get_height() // 2)
            )

    def is_alive(self):
        return self.alive