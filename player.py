import pygame
from settings import PLAYER_SPEED, PLAYER_SIZE, COLOR_PLAYER

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(COLOR_PLAYER)
        self.rect = self.image.get_rect(center=pos)

        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.speed = PLAYER_SPEED

        self.can_shoot = True
        self.shoot_cooldown = 0.22 
        self.cooldown_timer = 0.0

    def get_input(self):
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1

        if direction.magnitude() > 0:
            direction = direction.normalize()

        wants_to_shoot = keys[pygame.K_SPACE]

        return direction, wants_to_shoot

    def update_cooldown(self, dt):
        if not self.can_shoot:
            self.cooldown_timer += dt
            if self.cooldown_timer >= self.shoot_cooldown:
                self.can_shoot = True
                self.cooldown_timer = 0.0

    def update(self, dt):
        direction, wants_to_shoot = self.get_input()

        self.pos_x += direction.x * self.speed * dt
        self.pos_y += direction.y * self.speed * dt
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)
        self.clamp_position()

        self.update_cooldown(dt)

        shot_fired = wants_to_shoot and self.can_shoot
        if shot_fired:
            self.can_shoot = False

        return shot_fired

    def clamp_position(self):
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()

        if self.rect.left < 0:
            self.rect.left = 0
            self.pos_x = float(self.rect.x)
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
            self.pos_x = float(self.rect.x)

        if self.rect.top < 0:
            self.rect.top = 0
            self.pos_y = float(self.rect.y)
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.pos_y = float(self.rect.y)