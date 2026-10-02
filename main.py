# main.py
import sys
import random
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, FPS, COLOR_BG, ENEMY_SPAWN_RATE
from player import Player
from projectile import Laser
from enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.RESIZABLE
        )
        pygame.display.set_caption(CAPTION)
        
        self.clock = pygame.time.Clock()
        self.is_running = True

        # Player setup
        start_pos = (self.screen.get_width() // 2, self.screen.get_height() - 60)
        self.player_sprite = Player(start_pos)
        self.player_group = pygame.sprite.GroupSingle(self.player_sprite)

        # Sprite Groups
        self.laser_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        # Custom Event for Enemy Spawning
        self.SPAWN_ENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_ENEMY, ENEMY_SPAWN_RATE)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(
                    event.size,
                    pygame.RESIZABLE
                )

            elif event.type == self.SPAWN_ENEMY:
                random_x = random.randint(20, self.screen.get_width() - 20)
                spawn_pos = (random_x, -20)
                new_enemy = Enemy(spawn_pos)
                self.enemy_group.add(new_enemy)

    def check_collisions(self):
        collisions = pygame.sprite.groupcollide(self.laser_group, self.enemy_group, True, True)

        if self.player_group.sprite:
            player_hit = pygame.sprite.spritecollide(self.player_group.sprite, self.enemy_group, True)
            if player_hit:
                print("Player Ship Destroyed!")
                self.is_running = False

    def update(self, dt):
        if self.player_group.sprite:
            shot_fired = self.player_group.sprite.update(dt)
            if shot_fired:
                laser_pos = self.player_group.sprite.rect.midtop
                new_laser = Laser(laser_pos)
                self.laser_group.add(new_laser)

        self.laser_group.update(dt)
        self.enemy_group.update(dt)
        self.check_collisions()

    def draw(self):
        self.screen.fill(COLOR_BG)

        self.player_group.draw(self.screen)
        self.laser_group.draw(self.screen)
        self.enemy_group.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.is_running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()