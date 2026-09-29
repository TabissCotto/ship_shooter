import pygame
from settings import SCREEN_HEIGHT, ENEMY_SPEED, ENEMY_SIZE, COLOR_ENEMY

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface(ENEMY_SIZE)
        self.image.fill(COLOR_ENEMY)
        self.rect = self.image.get_rect(center=pos)

        self.pos_y = float(self.rect.y)
        self.speed = ENEMY_SPEED

    def update(self, dt):
        self.pos_y += self.speed * dt
        self.rect.y = int(self.pos_y)

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()