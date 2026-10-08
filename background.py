# background.py
import random
import pygame
import settings as stn

class Starfield:
    def __init__(self, screen_width, screen_height, count=120):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.stars = []

        # Generate stars: [x, y, speed, size, color]
        for _ in range(count):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            layer = random.choices([1, 2, 3], weights=[60, 30, 10])[0]

            if layer == 1:
                speed, size, color = 40.0, 1, (120, 120, 160)   # Distant slow stars
            elif layer == 2:
                speed, size, color = 90.0, 2, (200, 200, 225)   # Mid-layer stars
            else:
                speed, size, color = 180.0, 3, (255, 255, 255)  # Fast foreground stars

            self.stars.append([x, y, speed, size, color])

    def resize(self, new_width, new_height):
        self.screen_width = new_width
        self.screen_height = new_height

    def update(self, dt):
        for star in self.stars:
            star[1] += star[2] * dt  
            if star[1] > self.screen_height:
                star[1] = 0
                star[0] = random.randint(0, self.screen_width)

    def draw(self, surface):
        for x, y, _, size, color in self.stars:
            pygame.draw.circle(surface, color, (int(x), int(y)), size)