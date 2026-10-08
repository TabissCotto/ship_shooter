# enemy.py
import math
import pygame
import settings as stn


# =====================================================================
# Base class
# =====================================================================
class BaseEnemy(pygame.sprite.Sprite):
    # Common scaffolding: image, hp, score, position floats, hit flash.

    SCALE        = 1.0
    SPEED_MULT   = 1.0
    MAX_HEALTH   = 1
    POINTS       = 100
    HIT_FLASH    = 0.10   # seconds of white overlay after a hit

    def __init__(self, pos, image_surface):
        super().__init__()

        # Store the *original* (already scaled for this class at load time)
        self.original_image = image_surface
        self.image = image_surface
        self.rect = self.image.get_rect(center=pos)

        # Float positions so we don't lose sub-pixel motion at high speeds
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        self.speed = stn.ENEMY_SPEED * self.SPEED_MULT
        self.health = self.MAX_HEALTH
        self.flash_timer = 0.0

        # White-flash tint cached once
        self._flash_surface = None

    # ---------------- damage / score ----------------
    def hit(self, damage=1):
        """Returns True if this hit destroyed the enemy."""
        self.health -= damage
        if self.health <= 0:
            return True
        self.flash_timer = self.HIT_FLASH
        self._apply_flash()
        return False

    def _apply_flash(self):
        if self._flash_surface is None:
            self._flash_surface = self.original_image.copy()
            self._flash_surface.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.image = self._flash_surface

    def _clear_flash(self):
        self.image = self.original_image

    # ---------------- helpers ----------------
    def _apply_rect_from_floats(self):
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

    def _screen_size(self):
        surf = pygame.display.get_surface()
        return surf.get_size() if surf else (stn.SCREEN_WIDTH, stn.SCREEN_HEIGHT)

    def _off_bottom(self):
        _, sh = self._screen_size()
        return self.rect.top > sh

    # ---------------- per-frame ----------------
    def update(self, dt, player=None, enemy_laser_group=None):
        """Subclasses override `behave()`."""
        if self.flash_timer > 0:
            self.flash_timer -= dt
            if self.flash_timer <= 0:
                self._clear_flash()

        self.behave(dt, player, enemy_laser_group)
        self._apply_rect_from_floats()

        if self._off_bottom():
            self.kill()

    def behave(self, dt, player, enemy_laser_group):
        # Default: straight down
        self.pos_y += self.speed * dt


# =====================================================================
# 1. Standard — enemy1
# =====================================================================
class StandardEnemy(BaseEnemy):
    MAX_HEALTH = 1
    POINTS     = stn.POINTS_STANDARD
    SPEED_MULT = 1.0


# =====================================================================
# 2. ZigZag — enemy2
# =====================================================================
class ZigZagEnemy(BaseEnemy):
    MAX_HEALTH = 1
    POINTS     = stn.POINTS_ZIGZAG
    SPEED_MULT = stn.ZIGZAG_SPEED_MULT

    def __init__(self, pos, image_surface):
        super().__init__(pos, image_surface)
        self.start_x = self.pos_x
        self.elapsed = 0.0

    def behave(self, dt, player, enemy_laser_group):
        self.elapsed += dt
        self.pos_y += self.speed * dt
        self.pos_x = self.start_x + math.sin(self.elapsed * stn.ZIGZAG_FREQUENCY) * stn.ZIGZAG_AMPLITUDE

        # Clamp horizontally so it doesn't leave the screen
        sw, _ = self._screen_size()
        half_w = self.rect.width / 2
        if self.pos_x < half_w:
            self.pos_x = half_w
        elif self.pos_x > sw - half_w:
            self.pos_x = sw - half_w


# =====================================================================
# 3. Fast — enemy3
# =====================================================================
class FastEnemy(BaseEnemy):
    MAX_HEALTH = 1
    POINTS     = stn.POINTS_FAST
    SPEED_MULT = stn.FAST_SPEED_MULT
    # Fast movement — the base class already handles straight-down by default


# =====================================================================
# 4. Tank — enemy4
# =====================================================================
class TankEnemy(BaseEnemy):
    MAX_HEALTH = stn.TANK_MAX_HEALTH
    POINTS     = stn.POINTS_TANK
    SPEED_MULT = stn.TANK_SPEED_MULT
    HIT_FLASH  = stn.TANK_HIT_FLASH

    def behave(self, dt, player, enemy_laser_group):
        self.pos_y += self.speed * dt


# =====================================================================
# 5. Shooter — enemy5
# =====================================================================
class ShooterEnemy(BaseEnemy):
    MAX_HEALTH = stn.SHOOTER_MAX_HEALTH
    POINTS     = stn.POINTS_SHOOTER
    SPEED_MULT = stn.SHOOTER_SPEED_MULT
    HIT_FLASH  = stn.SHOOTER_HIT_FLASH

    def __init__(self, pos, image_surface):
        super().__init__(pos, image_surface)

        # Phase state
        self.phase = "descend"          # -> "hover"
        _, sh = self._screen_size()
        self.target_y = sh * stn.SHOOTER_TARGET_Y_FRAC
        self.vx = stn.SHOOTER_HOVER_SPEED
        self.fire_timer = stn.SHOOTER_FIRE_COOLDOWN   # wait a beat before first shot

    def behave(self, dt, player, enemy_laser_group):
        if self.phase == "descend":
            self.pos_y += self.speed * dt
            if self.pos_y >= self.target_y:
                self.pos_y = self.target_y
                self.phase = "hover"
        else:  # hover & patrol
            self.pos_x += self.vx * dt
            sw, _ = self._screen_size()
            half_w = self.rect.width / 2

            # Bounce off screen edges
            if self.pos_x < half_w:
                self.pos_x = half_w
                self.vx = abs(self.vx)
            elif self.pos_x > sw - half_w:
                self.pos_x = sw - half_w
                self.vx = -abs(self.vx)

            # Fire on cooldown
            self.fire_timer -= dt
            if self.fire_timer <= 0 and enemy_laser_group is not None:
                self.fire_timer = stn.SHOOTER_FIRE_COOLDOWN
                shot_pos = self.rect.midbottom
                enemy_laser_group.add(EnemyLaser(shot_pos))


# =====================================================================
# Enemy projectile
# =====================================================================
class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Load once, scale once — keep the upright original for re-rotation
        raw = pygame.image.load(stn.PATH_ENEMY_LASER_IMG).convert_alpha()
        self.original = pygame.transform.scale(raw, stn.ENEMY_LASER_SIZE)

        # Start sprite with the upright image
        self.image = self.original
        self.rect  = self.image.get_rect(midtop=pos)

        # Keep center in floats so rotation stays smooth
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

        self.speed = stn.ENEMY_LASER_SPEED
        self.angle = 0.0                       # current rotation, in degrees

    def update(self, dt):
        # Spin
        self.angle = (self.angle + stn.ENEMY_LASER_SPIN * dt) % 360

        # Rotate the sprite around its center
        self.image = pygame.transform.rotate(self.original, self.angle)
        self.rect  = self.image.get_rect(center=(self.pos_x, self.pos_y))

        # Fall
        self.pos_y += self.speed * dt
        self.rect.centery = int(self.pos_y)

        screen = pygame.display.get_surface()
        if screen and self.rect.top > screen.get_height():
            self.kill()