import sys
import random
import pygame
import settings as stn
from player import Player
from projectile import Laser
from enemy import (
    StandardEnemy, ZigZagEnemy, FastEnemy, TankEnemy, ShooterEnemy,
)
from background import Starfield


def load_scaled(path, scale):
    """Module-level helper — no `self` needed."""
    raw = pygame.image.load(path).convert_alpha()
    w = int(stn.ENEMY_SIZE[0] * scale)
    h = int(stn.ENEMY_SIZE[1] * scale)
    return pygame.transform.scale(raw, (w, h))


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (stn.SCREEN_WIDTH, stn.SCREEN_HEIGHT),
            pygame.RESIZABLE
        )
        pygame.display.set_caption(stn.CAPTION)

        self.clock = pygame.time.Clock()
        self.is_running = True

        # Starfield
        self.starfield = Starfield(
            self.screen.get_width(),
            self.screen.get_height(),
            stn.STAR_COUNT,
        )

        # Fonts
        self.font = pygame.font.Font(stn.PATH_FONT or None, stn.UI_FONT_SIZE)
        self.font_big = pygame.font.Font(stn.PATH_FONT or None, stn.UI_FONT_SIZE_BIG)

        # --- Enemy registry (class, surface, spawn_weight) ---
        self.enemy_defs = [
            (StandardEnemy, load_scaled(stn.ENEMY_TEXTURES[0], 1.0),                   50),
            (ZigZagEnemy,   load_scaled(stn.ENEMY_TEXTURES[1], 1.0),                   20),
            (FastEnemy,     load_scaled(stn.ENEMY_TEXTURES[2], stn.FAST_SIZE_SCALE),   15),
            (TankEnemy,     load_scaled(stn.ENEMY_TEXTURES[3], stn.TANK_SIZE_SCALE),    8),
            (ShooterEnemy,  load_scaled(stn.ENEMY_TEXTURES[4], 1.0),                    7),
        ]
        self._enemy_classes  = [d[0] for d in self.enemy_defs]
        self._enemy_surfaces = [d[1] for d in self.enemy_defs]
        self._enemy_weights  = [d[2] for d in self.enemy_defs]

        # Custom event for spawning
        self.SPAWN_ENEMY = pygame.USEREVENT + 1

        self.reset_game()
    # ------------------------------------------------------------------
    # Setup / Reset
    # ------------------------------------------------------------------
    def reset_game(self):
        """(Re)initialize a fresh round."""
        start_pos = (self.screen.get_width() // 2, self.screen.get_height() - 60)
        self.player_sprite = Player(start_pos)
        self.player_group = pygame.sprite.GroupSingle(self.player_sprite)

        self.laser_group = pygame.sprite.Group()
        self.enemy_laser_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.score = 0
        self.paused = False
        self.game_over = False

        # Ensure spawn timer is running exactly once
        pygame.time.set_timer(self.SPAWN_ENEMY, stn.ENEMY_SPAWN_RATE)

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                self.starfield.resize(event.w, event.h)  # <--- RESIZE STARFIELD BOUNDS

            elif event.type == pygame.KEYDOWN:
                if event.key == stn.PAUSE_KEY and not self.game_over:
                    self.paused = not self.paused

                if self.game_over and event.key in stn.RESTART_KEYS:
                    self.reset_game()

            elif event.type == self.SPAWN_ENEMY:
                if not self.paused and not self.game_over:
                    self.spawn_enemy()

    def spawn_enemy(self):
        cls, surf = random.choices(
            list(zip(self._enemy_classes, self._enemy_surfaces)),
            weights=self._enemy_weights,
            k=1,
        )[0]

        # Leave some margin so big tanks don't clip off the edges at spawn
        half_w = surf.get_width() // 2 + 5
        random_x = random.randint(half_w, self.screen.get_width() - half_w)
        spawn_pos = (random_x, -surf.get_height())

        self.enemy_group.add(cls(spawn_pos, surf))

    # ------------------------------------------------------------------
    # Collisions
    # ------------------------------------------------------------------
    def check_collisions(self):
        # --- Player laser vs enemies ------------------------------------
        hits = pygame.sprite.groupcollide(
            self.laser_group, self.enemy_group, True, False
        )
        for _laser, enemies_hit in hits.items():
            for enemy in enemies_hit:
                if enemy.hit(1):
                    self.score += enemy.POINTS
                    enemy.kill()

        # --- Enemy laser vs player --------------------------------------
        if self.player_group.sprite:
            player_laser_hits = pygame.sprite.spritecollide(
                self.player_group.sprite, self.enemy_laser_group, True
            )
            if player_laser_hits:
                self._damage_player(len(player_laser_hits))

        # --- Enemy body vs player ---------------------------------------
        if self.player_group.sprite:
            player_hits = pygame.sprite.spritecollide(
                self.player_group.sprite, self.enemy_group, True
            )
            if player_hits:
                self._damage_player(len(player_hits))


    def _damage_player(self, amount):
        dead = self.player_group.sprite.take_damage(amount)
        if dead:
            self.game_over = True
            self.paused = False
            self.player_group.empty()

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self, dt):
        if self.paused or self.game_over:
            return

        self.starfield.update(dt)

        if self.player_group.sprite:
            shot_fired = self.player_group.sprite.update(dt)
            if shot_fired:
                laser_pos = self.player_group.sprite.rect.midtop
                self.laser_group.add(Laser(laser_pos))

        player = self.player_group.sprite
        self.laser_group.update(dt)
        self.enemy_group.update(dt, player, self.enemy_laser_group)   # <-- NEW
        self.enemy_laser_group.update(dt)                             # <-- NEW
        self.check_collisions()

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
    def draw_ui(self):
        # Score (top-left)
        score_surf = self.font.render(f"Score: {self.score}", True, stn.COLOR_UI_TEXT)
        self.screen.blit(score_surf, (stn.UI_PADDING, stn.UI_PADDING))

        # Health (top-right) — simple hearts / rectangles
        if self.player_group.sprite:
            hp = self.player_group.sprite.health
            max_hp = self.player_group.sprite.max_health
        else:
            hp, max_hp = 0, stn.PLAYER_MAX_HEALTH

        heart_size = 22
        gap = 6
        for i in range(max_hp):
            color = stn.COLOR_UI_BAD if i < hp else (70, 70, 80)
            rect = pygame.Rect(
                self.screen.get_width() - stn.UI_PADDING - (max_hp - i) * (heart_size + gap),
                stn.UI_PADDING,
                heart_size, heart_size
            )
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            pygame.draw.rect(self.screen, stn.COLOR_UI_TEXT, rect, 2, border_radius=5)

        # Optional hint
        hint = self.font.render("Tab: Pause", True, (140, 140, 150))
        self.screen.blit(
            hint,
            (stn.UI_PADDING, self.screen.get_height() - stn.UI_PADDING - hint.get_height())
        )

    def draw_overlay(self, title, subtitle, color):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill(stn.COLOR_OVERLAY)
        self.screen.blit(overlay, (0, 0))

        title_surf = self.font_big.render(title, True, color)
        sub_surf = self.font.render(subtitle, True, stn.COLOR_UI_TEXT)

        cx = self.screen.get_width() // 2
        cy = self.screen.get_height() // 2

        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, cy - 40)))
        self.screen.blit(sub_surf, sub_surf.get_rect(center=(cx, cy + 40)))

    def draw(self):
        self.screen.fill(stn.COLOR_BG)

        self.starfield.draw(self.screen)  

        self.player_group.draw(self.screen)
        self.laser_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.enemy_laser_group.draw(self.screen)

        self.draw_ui()

        if self.paused and not self.game_over:
            self.draw_overlay("PAUSED", "Press Tab to resume", stn.COLOR_UI_ACCENT)

        if self.game_over:
            self.draw_overlay(
                "GAME OVER",
                f"Score: {self.score}   |   Press R or Enter to restart",
                stn.COLOR_UI_BAD
            )

        pygame.display.flip()

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        while self.is_running:
            dt = self.clock.tick(stn.FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()