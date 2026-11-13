"""
================================================================================
RUNGTA INTERNATIONAL SKILLS UNIVERSITY
SCHOOL OF COMPUTER SCIENCE AND ENGINEERING
COURSE CODE: RU-100-01-0021 (Programming Fundamentals & Logic Building Using Python)
PROBLEM STATEMENT NO. 59: SPACE SHOOTER
================================================================================
Problem Statement:
Build a space shooter game in which the player's spaceship moves left and right 
at the bottom of the screen and fires bullets upward to destroy enemy ships 
descending from the top. The player earns points for each hit and loses a life 
when an enemy reaches the bottom.

Language: Python 3      Concepts: Pygame, Objects, Collision Detection
Note: Window 600x600. Ship is 50x50 at y = 520 and moves 8 px per key press. 
Bullet is 5x10 and moves 10 px per frame upward; maximum 5 bullets on screen. 
Enemy is 40x40. Hit = +10 score; an enemy reaching y = 600 costs 1 life 
(start with 3 lives). Positions given as (x, y) = top-left corner.
================================================================================
"""

import os
import sys
import random

try:
    import pygame
except ImportError:
    pygame = None


# ----------------------------------------------------------------------
# GLOBAL CONSTANTS & GAME SPECIFICATIONS
# ----------------------------------------------------------------------
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FPS = 60

# Ship specifications
SHIP_WIDTH = 50
SHIP_HEIGHT = 50
SHIP_Y = 520
SHIP_SPEED = 8
SHIP_START_X = 275

# Bullet specifications
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 10
MAX_BULLETS = 5

# Enemy specifications
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_SPEED = 2
SPAWN_INTERVAL_MS = 1200

# Game rules
STARTING_LIVES = 3
HIT_SCORE = 10

# Color palette
COLOR_BG = (10, 12, 28)
COLOR_WHITE = (245, 245, 245)
COLOR_CYAN = (64, 224, 255)
COLOR_YELLOW = (255, 220, 70)
COLOR_RED = (255, 82, 82)
COLOR_GREEN = (76, 217, 100)
COLOR_GRAY = (160, 160, 175)


# ----------------------------------------------------------------------
# FALLBACK RECT IMPLEMENTATION (Ensures headless / fallback compatibility)
# ----------------------------------------------------------------------
class PureRect:
    """Lightweight 2D Axis-Aligned Bounding Box with colliderect method."""
    def __init__(self, x, y, width, height):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)

    @property
    def left(self): return self.x
    @property
    def right(self): return self.x + self.width
    @property
    def top(self): return self.y
    @property
    def bottom(self): return self.y + self.height

    def colliderect(self, other):
        return (self.left < other.right and
                self.right > other.left and
                self.top < other.bottom and
                self.bottom > other.top)


def make_rect(x, y, w, h):
    """Create a pygame.Rect if pygame is available, else fallback to PureRect."""
    if pygame is not None:
        return pygame.Rect(int(x), int(y), int(w), int(h))
    return PureRect(x, y, w, h)


# ----------------------------------------------------------------------
# 1. SHIP CLASS (OBJECT-ORIENTED MODEL)
# ----------------------------------------------------------------------
class Ship:
    """
    Player spaceship controlled with LEFT and RIGHT arrow keys.
    Size: 50x50, locked vertically at y = 520.
    Moves 8 px per press, strictly clamped inside window boundaries [0, 550].
    """
    def __init__(self, x=SHIP_START_X, y=SHIP_Y):
        self.x = x
        self.y = y
        self.width = SHIP_WIDTH
        self.height = SHIP_HEIGHT
        self.speed = SHIP_SPEED

    @property
    def rect(self):
        return make_rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        """
        Move spaceship left (-1) or right (+1).
        Enforces strict window boundary [0, WINDOW_WIDTH - SHIP_WIDTH].
        """
        self.x += direction * self.speed
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))

    def draw(self, screen):
        """Render stylish vector-rendered spaceship on Pygame surface."""
        if pygame is None:
            return
        # Main fuselage
        tip = (self.x + self.width // 2, self.y)
        bottom_right = (self.x + self.width, self.y + self.height)
        bottom_mid = (self.x + self.width // 2, self.y + 36)
        bottom_left = (self.x, self.y + self.height)
        pygame.draw.polygon(screen, COLOR_CYAN, [tip, bottom_right, bottom_mid, bottom_left])

        # Cockpit canopy
        pygame.draw.rect(screen, COLOR_WHITE, (self.x + 21, self.y + 18, 8, 16), border_radius=3)
        # Thruster glow
        pygame.draw.line(screen, COLOR_YELLOW, (self.x + 20, self.y + self.height + 1), (self.x + 30, self.y + self.height + 1), 3)


# ----------------------------------------------------------------------
# 2. BULLET CLASS (OBJECT-ORIENTED MODEL)
# ----------------------------------------------------------------------
class Bullet:
    """
    Bullet fired upward from the center-top of the spaceship.
    Size: 5x10, speed: 10 px per frame upward.
    """
    def __init__(self, x, y):
        # x is horizontal center; top coordinate is y
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.speed = BULLET_SPEED

    @property
    def rect(self):
        # Top-left corner bounding box
        return make_rect(int(self.x - self.width // 2), int(self.y), self.width, self.height)

    def update(self):
        """Move bullet upward."""
        self.y -= self.speed

    def draw(self, screen):
        """Render bullet on Pygame surface."""
        if pygame is None:
            return
        pygame.draw.rect(screen, COLOR_YELLOW, self.rect, border_radius=2)


# ----------------------------------------------------------------------
# 3. ENEMY CLASS (OBJECT-ORIENTED MODEL)
# ----------------------------------------------------------------------
class Enemy:
    """
    Enemy ship descending from top of screen.
    Size: 40x40, speed: 2 px per frame downward.
    """
    def __init__(self, x, y=0):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = ENEMY_SPEED

    @property
    def rect(self):
        return make_rect(self.x, self.y, self.width, self.height)

    def update(self):
        """Descend downward."""
        self.y += self.speed

    def draw(self, screen):
        """Render alien enemy craft on Pygame surface."""
        if pygame is None:
            return
        # Craft hull
        pygame.draw.rect(screen, COLOR_RED, self.rect, border_radius=8)
        # Cockpit eyes
        pygame.draw.circle(screen, COLOR_WHITE, (int(self.x + 11), int(self.y + 14)), 4)
        pygame.draw.circle(screen, COLOR_WHITE, (int(self.x + 29), int(self.y + 14)), 4)
        # Antenna / wings
        pygame.draw.line(screen, (200, 40, 40), (self.x + 4, self.y + 4), (self.x + 36, self.y + 4), 2)


# ----------------------------------------------------------------------
# 4. SPACE SHOOTER CONTROLLER & GAME ENGINE
# ----------------------------------------------------------------------
class SpaceShooter:
    """
    Master game loop orchestrator and physics state engine.
    Controls game objects, lifecycle, scoring, collisions, and HUD.
    """
    def __init__(self):
        self.ship = Ship(x=SHIP_START_X, y=SHIP_Y)
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.lives = STARTING_LIVES
        self.game_over = False
        self.last_spawn_time = 0
        self.spawn_interval = SPAWN_INTERVAL_MS

    def fire_bullet(self):
        """
        Fires a bullet if current bullets on screen are strictly less than MAX_BULLETS (5).
        Returns the spawned Bullet instance or None if limit reached.
        """
        if len(self.bullets) < MAX_BULLETS:
            # Center of ship: ship.x + ship.width // 2 = 275 + 25 = 300
            bullet_x = self.ship.x + self.ship.width // 2
            bullet_y = self.ship.y
            bullet = Bullet(bullet_x, bullet_y)
            self.bullets.append(bullet)
            return bullet
        return None

    def update_bullets(self):
        """Advance bullets upward and clean up off-screen entities."""
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y + bullet.height < 0:
                self.bullets.remove(bullet)

    def update_enemies(self):
        """
        Advance enemy ships downward.
        If an enemy's top coordinate reaches or exceeds y = 600, it escapes:
        costing 1 player life and triggering game over if lives deplete.
        """
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.y >= WINDOW_HEIGHT:
                self.enemies.remove(enemy)
                self.lives -= 1
                if self.lives <= 0:
                    self.lives = 0
                    self.game_over = True

    def check_collisions(self):
        """
        Detect collisions between bullets and enemies using Rect.colliderect().
        Upon impact: destroys bullet & enemy, awards +10 score.
        """
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    self.score += HIT_SCORE
                    break

    def spawn_enemy(self):
        """Spawn an enemy at a randomized horizontal coordinate at y = 0."""
        x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH)
        self.enemies.append(Enemy(x, 0))

    def restart(self):
        """Reset game state for a new session."""
        self.__init__()


# ----------------------------------------------------------------------
# 5. PYGAME GUI DISPLAY & INTERACTION LOOP
# ----------------------------------------------------------------------
def draw_hud(screen, game, font):
    """Render heads-up display (Score, Lives, Bullet capacity)."""
    score_surf = font.render(f"Score: {game.score}", True, COLOR_WHITE)
    lives_surf = font.render(f"Lives: {game.lives}", True, COLOR_RED if game.lives == 1 else COLOR_WHITE)
    bullets_surf = font.render(f"Bullets: {len(game.bullets)}/{MAX_BULLETS}", True, COLOR_YELLOW if len(game.bullets) == MAX_BULLETS else COLOR_WHITE)

    screen.blit(score_surf, (15, 12))
    screen.blit(lives_surf, (255, 12))
    screen.blit(bullets_surf, (445, 12))

    # Boundary guideline
    pygame.draw.line(screen, (30, 35, 60), (0, 40), (WINDOW_WIDTH, 40), 1)


def draw_game_over(screen, game, big_font, font):
    """Render Game Over overlay with final score and restart options."""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    screen.blit(overlay, (0, 0))

    title = big_font.render("GAME OVER", True, COLOR_RED)
    score_txt = font.render(f"Final Score: {game.score}", True, COLOR_WHITE)
    restart_txt = font.render("Press [R] to Restart  |  [ESC] to Quit", True, COLOR_CYAN)

    screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 230)))
    screen.blit(score_txt, score_txt.get_rect(center=(WINDOW_WIDTH // 2, 300)))
    screen.blit(restart_txt, restart_txt.get_rect(center=(WINDOW_WIDTH // 2, 360)))


def main():
    """Main interactive Pygame entry point."""
    global pygame
    if pygame is None:
        import shutil
        import subprocess
        uv_exe = shutil.which("uv")
        if uv_exe:
            cmd = [uv_exe, "run", "--python", "3.12", "--with", "pygame", "python", os.path.abspath(__file__)] + sys.argv[1:]
            sys.exit(subprocess.call(cmd))
        print("Error: Pygame library is not installed in current environment.")
        print("Please install via: pip install pygame")
        sys.exit(1)

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Space Shooter - PS No. 59 (Rungta University)")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("consolas", 18, bold=True)
    big_font = pygame.font.SysFont("consolas", 46, bold=True)

    game = SpaceShooter()

    # Dynamic starfield background
    stars = [
        [random.randrange(WINDOW_WIDTH), random.randrange(WINDOW_HEIGHT), random.choice([1, 2])]
        for _ in range(90)
    ]

    running = True
    while running:
        clock.tick(FPS)

        # Event Dispatcher
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game.game_over:
                    game.fire_bullet()
                elif event.key == pygame.K_r and game.game_over:
                    game.restart()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # Gameplay update
        if not game.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                game.ship.move(-1)
            if keys[pygame.K_RIGHT]:
                game.ship.move(1)

            game.update_bullets()
            game.update_enemies()
            game.check_collisions()

            # Enemy spawner timer
            now = pygame.time.get_ticks()
            if now - game.last_spawn_time >= game.spawn_interval:
                game.spawn_enemy()
                game.last_spawn_time = now

        # Render stage
        screen.fill(COLOR_BG)

        # Starfield parallax motion
        for star in stars:
            star[1] = (star[1] + star[2]) % WINDOW_HEIGHT
            color = (180, 180, 210) if star[2] == 1 else (255, 255, 255)
            screen.set_at((star[0], star[1]), color)

        # Draw game entities
        if not game.game_over:
            game.ship.draw(screen)
            for bullet in game.bullets:
                bullet.draw(screen)
            for enemy in game.enemies:
                enemy.draw(screen)
            draw_hud(screen, game, font)
        else:
            game.ship.draw(screen)
            draw_hud(screen, game, font)
            draw_game_over(screen, game, big_font, font)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
