import pygame
import settings as stn

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface(stn.ENEMY_SIZE)
        self.image.fill(stn.COLOR_ENEMY)
        self.rect = self.image.get_rect(center=pos)

        self.pos_y = float(self.rect.y)
        self.speed = stn.ENEMY_SPEED

    def update(self, dt):
        self.pos_y += self.speed * dt
        self.rect.y = int(self.pos_y)

        screen = pygame.display.get_surface()
        if self.rect.top > screen.get_height():
            self.kill()