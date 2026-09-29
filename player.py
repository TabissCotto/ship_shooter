import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_SIZE, COLOR_PLAYER

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(COLOR_PLAYER)
        self.rect = self.image.get_rect(center=pos)

        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.speed = PLAYER_SPEED

    def get_input(self):
        keys = pygame.key.get_pressed()

        direction_x = 0
        direction_y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction_x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction_x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction_y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction_y += 1

        return direction_x, direction_y

    def update(self, dt):
        direction_x, direction_y = self.get_input()

        self.pos_x += direction_x * self.speed * dt
        self.pos_y += direction_y * self.speed * dt

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        self.clamp_position()

    def clamp_position(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos_x = float(self.rect.x)
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.pos_x = float(self.rect.x)

        if self.rect.top < 0:
            self.rect.top = 0
            self.pos_y = float(self.rect.y)
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.pos_y = float(self.rect.y)