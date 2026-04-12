import pygame
import random
from settings import *


class Alien(pygame.sprite.Sprite):
    def __init__(self, row, col, alien_type):
        super().__init__()
        self.row = row
        self.col = col
        self.alien_type = alien_type
        self.image = self._create_sprite(alien_type)
        self.rect = self.image.get_rect()
        self.score = ALIEN_SCORES[alien_type]
        self.frame = 0
        self.image_alt = self._create_sprite_alt(alien_type)

    def _create_sprite(self, alien_type):
        size = SPRITE_SIZE
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        if alien_type == 'top':
            color = pygame.Color(COLORS['alien_top'])
            pygame.draw.rect(surf, color, (4, 0, 4, 4))
            pygame.draw.rect(surf, color, (24, 0, 4, 4))
            pygame.draw.rect(surf, color, (8, 4, 16, 4))
            pygame.draw.rect(surf, color, (0, 8, 32, 4))
            pygame.draw.rect(surf, color, (8, 12, 4, 4))
            pygame.draw.rect(surf, color, (20, 12, 4, 4))
            pygame.draw.rect(surf, color, (4, 16, 24, 4))
            pygame.draw.rect(surf, color, (12, 20, 8, 4))
            pygame.draw.rect(surf, color, (4, 24, 4, 4))
            pygame.draw.rect(surf, color, (24, 24, 4, 4))
        elif alien_type == 'mid':
            color = pygame.Color(COLORS['alien_mid'])
            pygame.draw.rect(surf, color, (12, 0, 8, 4))
            pygame.draw.rect(surf, color, (8, 4, 16, 4))
            pygame.draw.rect(surf, color, (0, 8, 32, 4))
            pygame.draw.rect(surf, color, (4, 12, 8, 4))
            pygame.draw.rect(surf, color, (20, 12, 8, 4))
            pygame.draw.rect(surf, color, (0, 16, 8, 4))
            pygame.draw.rect(surf, color, (24, 16, 8, 4))
            pygame.draw.rect(surf, color, (4, 20, 24, 4))
            pygame.draw.rect(surf, color, (0, 24, 8, 4))
            pygame.draw.rect(surf, color, (24, 24, 8, 4))
            pygame.draw.rect(surf, color, (12, 24, 8, 4))
        else:
            color = pygame.Color(COLORS['alien_bottom'])
            pygame.draw.rect(surf, color, (4, 0, 24, 4))
            pygame.draw.rect(surf, color, (0, 4, 32, 4))
            pygame.draw.rect(surf, color, (4, 4, 4, 4))
            pygame.draw.rect(surf, color, (24, 4, 4, 4))
            pygame.draw.rect(surf, color, (0, 8, 32, 8))
            pygame.draw.rect(surf, color, (8, 8, 4, 4))
            pygame.draw.rect(surf, color, (20, 8, 4, 4))
            pygame.draw.rect(surf, color, (8, 16, 16, 4))
            pygame.draw.rect(surf, color, (4, 20, 8, 4))
            pygame.draw.rect(surf, color, (20, 20, 8, 4))
            pygame.draw.rect(surf, color, (0, 24, 4, 4))
            pygame.draw.rect(surf, color, (28, 24, 4, 4))
        return surf

    def _create_sprite_alt(self, alien_type):
        size = SPRITE_SIZE
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        if alien_type == 'top':
            color = pygame.Color(COLORS['alien_top'])
            pygame.draw.rect(surf, color, (4, 0, 4, 4))
            pygame.draw.rect(surf, color, (24, 0, 4, 4))
            pygame.draw.rect(surf, color, (12, 0, 8, 4))
            pygame.draw.rect(surf, color, (8, 4, 16, 4))
            pygame.draw.rect(surf, color, (0, 8, 32, 4))
            pygame.draw.rect(surf, color, (4, 12, 8, 4))
            pygame.draw.rect(surf, color, (20, 12, 8, 4))
            pygame.draw.rect(surf, color, (4, 16, 24, 4))
            pygame.draw.rect(surf, color, (0, 20, 4, 4))
            pygame.draw.rect(surf, color, (12, 20, 8, 4))
            pygame.draw.rect(surf, color, (28, 20, 4, 4))
            pygame.draw.rect(surf, color, (8, 24, 4, 4))
            pygame.draw.rect(surf, color, (20, 24, 4, 4))
        elif alien_type == 'mid':
            color = pygame.Color(COLORS['alien_mid'])
            pygame.draw.rect(surf, color, (12, 0, 8, 4))
            pygame.draw.rect(surf, color, (4, 4, 24, 4))
            pygame.draw.rect(surf, color, (0, 8, 32, 4))
            pygame.draw.rect(surf, color, (4, 12, 8, 4))
            pygame.draw.rect(surf, color, (20, 12, 8, 4))
            pygame.draw.rect(surf, color, (4, 16, 24, 4))
            pygame.draw.rect(surf, color, (0, 20, 8, 4))
            pygame.draw.rect(surf, color, (12, 20, 8, 4))
            pygame.draw.rect(surf, color, (24, 20, 8, 4))
            pygame.draw.rect(surf, color, (4, 24, 4, 4))
            pygame.draw.rect(surf, color, (24, 24, 4, 4))
        else:
            color = pygame.Color(COLORS['alien_bottom'])
            pygame.draw.rect(surf, color, (4, 0, 24, 4))
            pygame.draw.rect(surf, color, (0, 4, 32, 4))
            pygame.draw.rect(surf, color, (0, 8, 32, 8))
            pygame.draw.rect(surf, color, (8, 16, 16, 4))
            pygame.draw.rect(surf, color, (0, 20, 8, 4))
            pygame.draw.rect(surf, color, (24, 20, 8, 4))
            pygame.draw.rect(surf, color, (4, 24, 8, 4))
            pygame.draw.rect(surf, color, (20, 24, 8, 4))
        return surf

    def toggle_frame(self):
        self.frame = 1 - self.frame
        if self.frame == 0:
            self.image = self._create_sprite(self.alien_type)
        else:
            self.image = self.image_alt


class AlienGroup:
    def __init__(self, game):
        self.game = game
        self.aliens = pygame.sprite.Group()
        self.direction = 1
        self.speed = ALIEN_MOVE_SPEED
        self.move_timer = 0
        self.move_interval = 35
        self.should_drop = False
        self.frame_toggle = False
        self.alien_fire_rate = ALIEN_FIRE_RATE

    def create_aliens(self):
        self.aliens.empty()
        self.direction = 1
        self.move_timer = 0
        self.frame_toggle = False

        for row in range(ALIEN_ROWS):
            if row == 0:
                alien_type = 'top'
            elif row < 3:
                alien_type = 'mid'
            else:
                alien_type = 'bottom'

            for col in range(ALIEN_COLS):
                alien = Alien(row, col, alien_type)
                x = ALIEN_START_X + col * ALIEN_HORIZONTAL_SPACING
                y = ALIEN_START_Y + row * ALIEN_VERTICAL_SPACING
                alien.rect.topleft = (x, y)
                self.aliens.add(alien)

    def update(self):
        self.move_timer += 1
        if self.move_timer >= self.move_interval // (FPS // 60):
            self.move_timer = 0
            self._move()
            self.frame_toggle = not self.frame_toggle
            for alien in self.aliens:
                alien.toggle_frame()
            self._alien_shoot()

        alive_count = len(self.aliens)
        if alive_count > 0:
            self.move_interval = max(5, 35 - (55 - alive_count) * 0.5)

    def _move(self):
        edge_hit = False
        for alien in self.aliens:
            if self.direction == 1 and alien.rect.right >= GAME_RIGHT:
                edge_hit = True
                break
            elif self.direction == -1 and alien.rect.left <= GAME_LEFT:
                edge_hit = True
                break

        if edge_hit:
            self.direction *= -1
            for alien in self.aliens:
                alien.rect.y += ALIEN_DROP_DISTANCE
        else:
            for alien in self.aliens:
                alien.rect.x += self.direction * self.speed

    def _alien_shoot(self):
        if len(self.aliens) == 0:
            return
        if random.random() < self.alien_fire_rate:
            bottom_aliens = self._get_bottom_aliens()
            if bottom_aliens:
                shooter = random.choice(bottom_aliens)
                self.game.bullet_manager.alien_shoot(
                    shooter.rect.centerx,
                    shooter.rect.bottom
                )

    def _get_bottom_aliens(self):
        columns = {}
        for alien in self.aliens:
            col = alien.col
            if col not in columns or alien.row > columns[col].row:
                columns[col] = alien
        return list(columns.values())

    def check_reach_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom >= GAME_BOTTOM - 60:
                return True
        return False

    def draw(self, surface):
        for alien in self.aliens:
            surface.blit(alien.image, alien.rect)