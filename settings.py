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

PAUSE_KEY = pygame.K_TAB
RESTART_KEYS = (pygame.K_r, pygame.K_RETURN)

#-----------------------------------------------------FONTS
PATH_FONT = "assets/fonts/Flottflott.ttf"  

#-----------------------------------------------------BACKGROUND
STAR_COUNT = 150

#-----------------------------------------------------ENEMY BEHAVIOR

# ZigZag
ZIGZAG_FREQUENCY = 4.0
ZIGZAG_AMPLITUDE = 80.0
ZIGZAG_SPEED_MULT = 0.9

# Fast
FAST_SIZE_SCALE   = 0.8
FAST_SPEED_MULT   = 1.75

# Tank
TANK_SIZE_SCALE   = 1.3
TANK_SPEED_MULT   = 0.5
TANK_MAX_HEALTH   = 4
TANK_HIT_FLASH    = 0.10   # seconds of white flash per hit

# Shooter
SHOOTER_SPEED_MULT    = 0.8
SHOOTER_MAX_HEALTH    = 2
SHOOTER_TARGET_Y_FRAC = 0.22   # descends to 22% of screen height
SHOOTER_HOVER_SPEED   = 120.0  # horizontal patrol speed
SHOOTER_FIRE_COOLDOWN = 1.6    # seconds between shots
SHOOTER_HIT_FLASH     = 0.10

#-----------------------------------------------------ENEMY LASER
ENEMY_LASER_SPEED = 420.0
ENEMY_LASER_SIZE  = (24, 24)                 # square, so rotation looks right
ENEMY_LASER_SPIN  = 720.0                    # degrees per second (2 full turns/sec)
PATH_ENEMY_LASER_IMG = "assets/enemy_laser.png"   # <-- your shuriken

# Points per enemy 
POINTS_STANDARD = 100
POINTS_ZIGZAG   = 150
POINTS_FAST     = 200
POINTS_TANK     = 400
POINTS_SHOOTER  = 300