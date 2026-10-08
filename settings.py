import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CAPTION = "Arcade Ship Shooter"

FPS = 60

COLOR_BG = (15, 15, 25)  

TOGGLE_FULLSCREEN_KEY = pygame.K_F11

#-----------------------------------------------------PLAYER
PLAYER_SPEED = 500.0  
PLAYER_SIZE = (50, 40) 
COLOR_PLAYER = (50, 200, 255) 
PLAYER_ACCEL_DELAY = 0.20
PLAYER_ACCEL_INTERVAL = 0.075
PLAYER_ACCEL_FACTOR = 0.03  

#-----------------------------------------------------PROJECTILE

LASER_SPEED = 600.0  
LASER_SIZE = (6, 18)   
COLOR_LASER = (255, 220, 50)  

#-----------------------------------------------------ENEMY

ENEMY_SPEED = 200.0   
ENEMY_SIZE = (40, 30)  
COLOR_ENEMY = (255, 70, 70)  
ENEMY_SPAWN_RATE = 1000  

#-----------------------------------------------------ASSET PATHS

PATH_PLAYER_IMG = "assets/player.png"
PATH_LASER_IMG = "assets/laser.png"

ENEMY_TEXTURES = [
    "assets/enemy1.png",
    "assets/enemy2.png",
    "assets/enemy3.png",
    "assets/enemy4.png",
    "assets/enemy5.png",
]

#-----------------------------------------------------UI
UI_FONT_SIZE = 28
UI_FONT_SIZE_BIG = 72
UI_PADDING = 15
COLOR_UI_TEXT = (240, 240, 240)
COLOR_UI_ACCENT = (255, 220, 50)
COLOR_UI_BAD = (255, 70, 70)
COLOR_OVERLAY = (0, 0, 0, 160)

#-----------------------------------------------------GAMEPLAY
PLAYER_MAX_HEALTH = 3
POINTS_PER_ENEMY = 1

PAUSE_KEY = pygame.K_TAB
RESTART_KEYS = (pygame.K_r, pygame.K_RETURN)

#-----------------------------------------------------FONTS
PATH_FONT = "assets/fonts/Debrosee-ALPnL.ttf"  

#-----------------------------------------------------BACKGROUND
STAR_COUNT = 150