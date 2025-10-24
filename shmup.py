#!/usr/bin/env python3
"""
Cho Ren Sha-inspired Shoot'em Up
A vertical scrolling shooter game in the style of classic arcade shmups
"""

import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
PAUSED = 3


class Player(pygame.sprite.Sprite):
    """Player ship class"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 30))
        self.image.fill(BLUE)
        # Draw ship shape
        pygame.draw.polygon(self.image, CYAN, [(10, 0), (0, 30), (20, 30)])
        pygame.draw.circle(self.image, RED, (10, 20), 3)

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30

        self.speed = 5
        self.shoot_delay = 100  # milliseconds
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.power = 1
        self.max_power = 5
        self.invincible = False
        self.invincible_timer = 0
        self.bomb_count = 3

    def update(self):
        """Update player position and state"""
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Handle invincibility
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def shoot(self):
        """Fire bullets"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullets = []

            if self.power == 1:
                bullets.append(Bullet(self.rect.centerx, self.rect.top))
            elif self.power == 2:
                bullets.append(Bullet(self.rect.centerx - 5, self.rect.top))
                bullets.append(Bullet(self.rect.centerx + 5, self.rect.top))
            elif self.power == 3:
                bullets.append(Bullet(self.rect.centerx, self.rect.top))
                bullets.append(Bullet(self.rect.centerx - 10, self.rect.top + 5, -5))
                bullets.append(Bullet(self.rect.centerx + 10, self.rect.top + 5, 5))
            elif self.power == 4:
                bullets.append(Bullet(self.rect.centerx - 5, self.rect.top))
                bullets.append(Bullet(self.rect.centerx + 5, self.rect.top))
                bullets.append(Bullet(self.rect.centerx - 15, self.rect.top + 5, -3))
                bullets.append(Bullet(self.rect.centerx + 15, self.rect.top + 5, 3))
            else:  # Max power
                bullets.append(Bullet(self.rect.centerx, self.rect.top))
                bullets.append(Bullet(self.rect.centerx - 8, self.rect.top))
                bullets.append(Bullet(self.rect.centerx + 8, self.rect.top))
                bullets.append(Bullet(self.rect.centerx - 15, self.rect.top + 5, -5))
                bullets.append(Bullet(self.rect.centerx + 15, self.rect.top + 5, 5))

            return bullets
        return []

    def power_up(self):
        """Increase power level"""
        if self.power < self.max_power:
            self.power += 1

    def hit(self):
        """Player takes damage"""
        if not self.invincible:
            self.lives -= 1
            self.power = max(1, self.power - 1)
            self.invincible = True
            self.invincible_timer = 120  # 2 seconds at 60 FPS
            return True
        return False

    def use_bomb(self):
        """Use a bomb"""
        if self.bomb_count > 0:
            self.bomb_count -= 1
            self.invincible = True
            self.invincible_timer = 60
            return True
        return False


class Bullet(pygame.sprite.Sprite):
    """Player bullet class"""

    def __init__(self, x, y, dx=0):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
        self.dx = dx

    def update(self):
        """Move bullet"""
        self.rect.y += self.speed
        self.rect.x += self.dx
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    """Enemy bullet class"""

    def __init__(self, x, y, angle, speed=3):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill(RED)
        pygame.draw.circle(self.image, ORANGE, (3, 3), 3)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.angle = angle
        self.dx = math.cos(math.radians(angle)) * speed
        self.dy = math.sin(math.radians(angle)) * speed

    def update(self):
        """Move bullet"""
        self.rect.x += self.dx
        self.rect.y += self.dy

        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    """Base enemy class"""

    def __init__(self, x, y, enemy_type=0):
        super().__init__()
        self.enemy_type = enemy_type
        self.hp = 1
        self.points = 100

        # Different enemy types
        if enemy_type == 0:  # Basic enemy
            self.image = pygame.Surface((30, 30))
            self.image.fill(GREEN)
            pygame.draw.circle(self.image, RED, (15, 15), 12)
            self.speed = 2
            self.hp = 1
            self.shoot_timer = 0
            self.shoot_delay = 60

        elif enemy_type == 1:  # Fast enemy
            self.image = pygame.Surface((20, 20))
            self.image.fill(MAGENTA)
            pygame.draw.polygon(self.image, PURPLE, [(10, 0), (0, 20), (20, 20)])
            self.speed = 4
            self.hp = 1
            self.points = 150
            self.shoot_timer = 0
            self.shoot_delay = 90

        elif enemy_type == 2:  # Tank enemy
            self.image = pygame.Surface((40, 40))
            self.image.fill(ORANGE)
            pygame.draw.rect(self.image, RED, (5, 5, 30, 30))
            self.speed = 1
            self.hp = 3
            self.points = 300
            self.shoot_timer = 0
            self.shoot_delay = 45

        elif enemy_type == 3:  # Weaving enemy
            self.image = pygame.Surface((25, 25))
            self.image.fill(CYAN)
            pygame.draw.circle(self.image, BLUE, (12, 12), 10)
            self.speed = 3
            self.hp = 2
            self.points = 200
            self.shoot_timer = 0
            self.shoot_delay = 75
            self.wave_offset = random.randint(0, 360)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_x = x

    def update(self):
        """Update enemy position"""
        self.rect.y += self.speed

        # Weaving pattern for type 3
        if self.enemy_type == 3:
            self.wave_offset += 5
            self.rect.x = self.original_x + math.sin(math.radians(self.wave_offset)) * 50

        # Remove if off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

        self.shoot_timer += 1

    def shoot(self, player_x, player_y):
        """Fire bullets at player"""
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            bullets = []

            # Calculate angle to player
            dx = player_x - self.rect.centerx
            dy = player_y - self.rect.centery
            angle = math.degrees(math.atan2(dy, dx))

            if self.enemy_type == 0:
                # Single aimed shot
                bullets.append(EnemyBullet(self.rect.centerx, self.rect.centery, angle))

            elif self.enemy_type == 1:
                # Two angled shots
                bullets.append(EnemyBullet(self.rect.centerx, self.rect.centery, angle - 15))
                bullets.append(EnemyBullet(self.rect.centerx, self.rect.centery, angle + 15))

            elif self.enemy_type == 2:
                # Five-way spread
                for i in range(-2, 3):
                    bullets.append(EnemyBullet(self.rect.centerx, self.rect.centery, angle + i * 20))

            elif self.enemy_type == 3:
                # Circular pattern
                for i in range(8):
                    bullets.append(EnemyBullet(self.rect.centerx, self.rect.centery, i * 45))

            return bullets
        return []

    def hit(self):
        """Enemy takes damage"""
        self.hp -= 1
        if self.hp <= 0:
            # Chance to drop power-up
            if random.random() < 0.15:
                return PowerUp(self.rect.centerx, self.rect.centery)
        return None


class Boss(pygame.sprite.Sprite):
    """Boss enemy class"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill(PURPLE)
        pygame.draw.rect(self.image, RED, (10, 10, 60, 60))
        pygame.draw.rect(self.image, ORANGE, (20, 20, 40, 40))

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.y = -100

        self.hp = 100
        self.max_hp = 100
        self.points = 5000
        self.speed = 1
        self.direction = 1
        self.shoot_timer = 0
        self.pattern = 0
        self.pattern_timer = 0
        self.active = False

    def update(self):
        """Update boss behavior"""
        # Move into position
        if not self.active:
            self.rect.y += self.speed
            if self.rect.y >= 50:
                self.active = True
        else:
            # Move side to side
            self.rect.x += self.direction * 2
            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.direction *= -1

        self.shoot_timer += 1
        self.pattern_timer += 1

        # Change attack pattern every 5 seconds
        if self.pattern_timer >= 300:
            self.pattern = (self.pattern + 1) % 3
            self.pattern_timer = 0

    def shoot(self):
        """Fire bullet patterns"""
        bullets = []

        if self.pattern == 0:  # Spiral pattern
            if self.shoot_timer % 5 == 0:
                angle = (self.shoot_timer * 10) % 360
                for i in range(3):
                    bullets.append(EnemyBullet(
                        self.rect.centerx,
                        self.rect.centery,
                        angle + i * 120,
                        4
                    ))

        elif self.pattern == 1:  # Aimed burst
            if self.shoot_timer % 30 == 0:
                # Fire ring of bullets
                for i in range(12):
                    bullets.append(EnemyBullet(
                        self.rect.centerx,
                        self.rect.centery,
                        i * 30,
                        3
                    ))

        elif self.pattern == 2:  # Wave pattern
            if self.shoot_timer % 10 == 0:
                for i in range(-3, 4):
                    bullets.append(EnemyBullet(
                        self.rect.centerx + i * 20,
                        self.rect.centery,
                        90,
                        2 + abs(i) * 0.5
                    ))

        return bullets

    def hit(self):
        """Boss takes damage"""
        self.hp -= 1


class PowerUp(pygame.sprite.Sprite):
    """Power-up item class"""

    def __init__(self, x, y, powerup_type=None):
        super().__init__()
        if powerup_type is None:
            powerup_type = random.choice(['power', 'bomb'])

        self.powerup_type = powerup_type

        if powerup_type == 'power':
            self.image = pygame.Surface((20, 20))
            self.image.fill(BLUE)
            pygame.draw.circle(self.image, CYAN, (10, 10), 8)
        else:  # bomb
            self.image = pygame.Surface((20, 20))
            self.image.fill(RED)
            pygame.draw.circle(self.image, ORANGE, (10, 10), 8)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def update(self):
        """Move power-up down"""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    """Explosion effect"""

    def __init__(self, x, y, size=30):
        super().__init__()
        self.size = size
        self.image = pygame.Surface((size, size))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, ORANGE, (size//2, size//2), size//2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = 10

    def update(self):
        """Animate explosion"""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        else:
            # Expand and fade
            scale = 1 + (10 - self.lifetime) * 0.2
            new_size = int(self.size * scale)
            self.image = pygame.Surface((new_size, new_size))
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            color = (255, int(165 * self.lifetime / 10), 0)
            pygame.draw.circle(self.image, color, (new_size//2, new_size//2), new_size//2)
            self.rect = self.image.get_rect(center=self.rect.center)


class Game:
    """Main game class"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cho Ren Sha - Python Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.state = MENU
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.background_scroll = 0

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.player = None
        self.boss = None
        self.enemy_spawn_timer = 0
        self.boss_active = False

    def new_game(self):
        """Start a new game"""
        self.all_sprites.empty()
        self.player_bullets.empty()
        self.enemy_bullets.empty()
        self.enemies.empty()
        self.powerups.empty()
        self.explosions.empty()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.score = 0
        self.level = 1
        self.enemy_spawn_timer = 0
        self.boss = None
        self.boss_active = False
        self.state = PLAYING

    def spawn_enemy(self):
        """Spawn enemies in waves"""
        self.enemy_spawn_timer += 1

        # Spawn boss every 30 seconds
        if self.enemy_spawn_timer % 1800 == 0 and not self.boss_active:
            self.boss = Boss()
            self.enemies.add(self.boss)
            self.all_sprites.add(self.boss)
            self.boss_active = True
            return

        # Regular enemy spawning
        if self.boss_active:
            return

        if self.enemy_spawn_timer % 60 == 0:
            # Spawn random enemy type
            enemy_type = random.choices([0, 1, 2, 3], weights=[40, 30, 15, 15])[0]
            x = random.randint(50, SCREEN_WIDTH - 50)
            enemy = Enemy(x, -30, enemy_type)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        # Formation spawning
        if self.enemy_spawn_timer % 180 == 0:
            for i in range(5):
                x = 100 + i * 80
                enemy = Enemy(x, -30 - i * 40, random.randint(0, 1))
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.state == MENU:
                    if event.key == pygame.K_RETURN:
                        self.new_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False

                elif self.state == PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        self.state = PAUSED
                    elif event.key == pygame.K_x:
                        # Bomb
                        if self.player.use_bomb():
                            # Clear all enemy bullets
                            for bullet in self.enemy_bullets:
                                explosion = Explosion(bullet.rect.centerx, bullet.rect.centery, 20)
                                self.explosions.add(explosion)
                                self.all_sprites.add(explosion)
                            self.enemy_bullets.empty()

                            # Damage all enemies
                            for enemy in self.enemies:
                                if isinstance(enemy, Boss):
                                    enemy.hit()
                                    enemy.hit()
                                    enemy.hit()
                                else:
                                    powerup = enemy.hit()
                                    if powerup:
                                        self.powerups.add(powerup)
                                        self.all_sprites.add(powerup)
                                    if enemy.hp <= 0:
                                        explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                                        self.explosions.add(explosion)
                                        self.all_sprites.add(explosion)
                                        self.score += enemy.points
                                        enemy.kill()

                elif self.state == PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.state = PLAYING

                elif self.state == GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        self.state = MENU

        return True

    def update(self):
        """Update game state"""
        if self.state != PLAYING:
            return

        # Scroll background
        self.background_scroll = (self.background_scroll + 2) % SCREEN_HEIGHT

        # Player shooting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] or keys[pygame.K_SPACE]:
            bullets = self.player.shoot()
            for bullet in bullets:
                self.player_bullets.add(bullet)
                self.all_sprites.add(bullet)

        # Spawn enemies
        self.spawn_enemy()

        # Enemy shooting
        for enemy in self.enemies:
            if isinstance(enemy, Boss):
                bullets = enemy.shoot()
            else:
                bullets = enemy.shoot(self.player.rect.centerx, self.player.rect.centery)
            for bullet in bullets:
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(bullet)

        # Update sprites
        self.all_sprites.update()

        # Check collisions - player bullets hit enemies
        for bullet in self.player_bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
            if hit_enemies:
                bullet.kill()
                for enemy in hit_enemies:
                    powerup = enemy.hit()
                    if powerup:
                        self.powerups.add(powerup)
                        self.all_sprites.add(powerup)

                    if enemy.hp <= 0:
                        explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                        self.explosions.add(explosion)
                        self.all_sprites.add(explosion)
                        self.score += enemy.points

                        if isinstance(enemy, Boss):
                            self.boss_active = False
                            self.boss = None
                            self.level += 1

                        enemy.kill()

        # Check collisions - enemy bullets hit player
        if not self.player.invincible:
            hit_bullets = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
            if hit_bullets:
                if self.player.hit():
                    explosion = Explosion(self.player.rect.centerx, self.player.rect.centery)
                    self.explosions.add(explosion)
                    self.all_sprites.add(explosion)

                    if self.player.lives <= 0:
                        self.state = GAME_OVER
                        if self.score > self.high_score:
                            self.high_score = self.score

        # Check collisions - enemies hit player
        if not self.player.invincible:
            hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if hit_enemies:
                if self.player.hit():
                    explosion = Explosion(self.player.rect.centerx, self.player.rect.centery)
                    self.explosions.add(explosion)
                    self.all_sprites.add(explosion)

                    if self.player.lives <= 0:
                        self.state = GAME_OVER
                        if self.score > self.high_score:
                            self.high_score = self.score

        # Check collisions - player collects powerups
        hit_powerups = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in hit_powerups:
            if powerup.powerup_type == 'power':
                self.player.power_up()
                self.score += 50
            elif powerup.powerup_type == 'bomb':
                self.player.bomb_count += 1
                self.score += 100

    def draw_background(self):
        """Draw scrolling background"""
        # Create starfield effect
        for i in range(0, SCREEN_HEIGHT, 20):
            y = (i + self.background_scroll) % SCREEN_HEIGHT
            for j in range(0, SCREEN_WIDTH, 40):
                if random.random() < 0.1:
                    size = random.randint(1, 2)
                    pygame.draw.circle(self.screen, WHITE, (j, y), size)

    def draw_ui(self):
        """Draw user interface"""
        # Score
        score_text = self.small_font.render(f'SCORE: {self.score:08d}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # High score
        high_score_text = self.small_font.render(f'HI: {self.high_score:08d}', True, YELLOW)
        self.screen.blit(high_score_text, (10, 35))

        # Lives
        lives_text = self.small_font.render(f'LIVES: {self.player.lives}', True, GREEN)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

        # Power level
        power_text = self.small_font.render(f'POW: {self.player.power}', True, CYAN)
        self.screen.blit(power_text, (SCREEN_WIDTH - 120, 35))

        # Bombs
        bomb_text = self.small_font.render(f'BOMB: {self.player.bomb_count}', True, RED)
        self.screen.blit(bomb_text, (SCREEN_WIDTH - 120, 60))

        # Boss health bar
        if self.boss_active and self.boss:
            bar_width = 400
            bar_height = 20
            bar_x = (SCREEN_WIDTH - bar_width) // 2
            bar_y = SCREEN_HEIGHT - 30

            # Background
            pygame.draw.rect(self.screen, WHITE, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
            pygame.draw.rect(self.screen, BLACK, (bar_x, bar_y, bar_width, bar_height))

            # Health
            health_width = int((self.boss.hp / self.boss.max_hp) * bar_width)
            pygame.draw.rect(self.screen, RED, (bar_x, bar_y, health_width, bar_height))

            # Boss label
            boss_text = self.small_font.render('BOSS', True, YELLOW)
            self.screen.blit(boss_text, (bar_x - 50, bar_y))

    def draw_menu(self):
        """Draw menu screen"""
        self.screen.fill(BLACK)

        title = self.font.render('CHO REN SHA', True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        subtitle = self.small_font.render('Python Edition', True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)

        start = self.small_font.render('Press ENTER to Start', True, GREEN)
        start_rect = start.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(start, start_rect)

        controls1 = self.small_font.render('Arrow Keys / WASD - Move', True, WHITE)
        controls1_rect = controls1.get_rect(center=(SCREEN_WIDTH // 2, 420))
        self.screen.blit(controls1, controls1_rect)

        controls2 = self.small_font.render('Z / SPACE - Shoot', True, WHITE)
        controls2_rect = controls2.get_rect(center=(SCREEN_WIDTH // 2, 450))
        self.screen.blit(controls2, controls2_rect)

        controls3 = self.small_font.render('X - Bomb', True, WHITE)
        controls3_rect = controls3.get_rect(center=(SCREEN_WIDTH // 2, 480))
        self.screen.blit(controls3, controls3_rect)

        controls4 = self.small_font.render('ESC - Pause/Quit', True, WHITE)
        controls4_rect = controls4.get_rect(center=(SCREEN_WIDTH // 2, 510))
        self.screen.blit(controls4, controls4_rect)

        if self.high_score > 0:
            hi_score = self.font.render(f'High Score: {self.high_score:08d}', True, YELLOW)
            hi_score_rect = hi_score.get_rect(center=(SCREEN_WIDTH // 2, 280))
            self.screen.blit(hi_score, hi_score_rect)

    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))

        game_over = self.font.render('GAME OVER', True, RED)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(game_over, game_over_rect)

        final_score = self.small_font.render(f'Final Score: {self.score:08d}', True, WHITE)
        final_score_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, 320))
        self.screen.blit(final_score, final_score_rect)

        continue_text = self.small_font.render('Press ENTER to Continue', True, GREEN)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(continue_text, continue_rect)

    def draw_paused(self):
        """Draw pause screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        paused = self.font.render('PAUSED', True, YELLOW)
        paused_rect = paused.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(paused, paused_rect)

    def draw(self):
        """Draw everything"""
        if self.state == MENU:
            self.draw_menu()
        else:
            self.screen.fill(BLACK)
            self.draw_background()

            # Draw sprites
            for sprite in self.all_sprites:
                # Flash invincible player
                if sprite == self.player and self.player.invincible:
                    if pygame.time.get_ticks() % 200 < 100:
                        self.screen.blit(sprite.image, sprite.rect)
                else:
                    self.screen.blit(sprite.image, sprite.rect)

            if self.state == PLAYING:
                self.draw_ui()
            elif self.state == GAME_OVER:
                self.draw_game_over()
            elif self.state == PAUSED:
                self.draw_paused()

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
