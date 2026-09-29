import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, FPS, COLOR_BG
from player import Player
from projectile import Laser  

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.is_running = True

        start_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        self.player_sprite = Player(start_pos)
        self.player_group = pygame.sprite.GroupSingle(self.player_sprite)

        self.laser_group = pygame.sprite.Group()

    def run(self):
        while self.is_running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self, dt):
        shot_fired = self.player_group.sprite.update(dt)

        if shot_fired:
            laser_pos = self.player_group.sprite.rect.midtop
            new_laser = Laser(laser_pos)
            self.laser_group.add(new_laser)

        self.laser_group.update(dt)

    def draw(self):
        self.screen.fill(COLOR_BG)

        self.player_group.draw(self.screen)
        self.laser_group.draw(self.screen)

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()