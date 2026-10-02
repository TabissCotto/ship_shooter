import pygame
from settings import LASER_SPEED, LASER_SIZE, COLOR_LASER

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface(LASER_SIZE)
        self.image.fill(COLOR_LASER)
        self.rect = self.image.get_rect(center=pos)

        self.pos_y = float(self.rect.y)
        self.speed = LASER_SPEED

    def update(self, dt):
        self.pos_y -= self.speed * dt
        self.rect.y = int(self.pos_y)

        if self.rect.bottom < 0:
            self.kill()