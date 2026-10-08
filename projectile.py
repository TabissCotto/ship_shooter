import pygame
import settings as stn

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        raw_image = pygame.image.load(stn.PATH_LASER_IMG).convert_alpha()
        self.image = pygame.transform.scale(raw_image, stn.LASER_SIZE)
        self.rect = self.image.get_rect(center=pos)

        self.pos_y = float(self.rect.y)
        self.speed = stn.LASER_SPEED

    def update(self, dt):
        self.pos_y -= self.speed * dt
        self.rect.y = int(self.pos_y)

        if self.rect.bottom < 0:
            self.kill()