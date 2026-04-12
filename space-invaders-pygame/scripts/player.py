import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = self._create_sprite()
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = GAME_BOTTOM - 10

        self.lives = PLAYER_LIVES
        self.invincible = False
        self.invincible_timer = 0
        self.visible = True
        self.flicker_timer = 0

        self.last_shot_time = 0

    def _create_sprite(self):
        surf = pygame.Surface((38, 24), pygame.SRCALPHA)
        color = pygame.Color(COLORS['player'])
        pygame.draw.polygon(surf, color, [
            (19, 0), (38, 24), (0, 24)
        ])
        pygame.draw.rect(surf, color, (14, 8, 10, 16))
        return surf

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < GAME_LEFT:
            self.rect.left = GAME_LEFT
        if self.rect.right > GAME_RIGHT:
            self.rect.right = GAME_RIGHT

        if self.invincible:
            now = pygame.time.get_ticks()
            self.flicker_timer += 1
            if self.flicker_timer % 6 < 3:
                self.visible = True
            else:
                self.visible = False

            if now - self.invincible_timer >= PLAYER_INVINCIBLE_TIME:
                self.invincible = False
                self.visible = True
                self.flicker_timer = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= PLAYER_BULLET_COOLDOWN:
            self.last_shot_time = now
            return True
        return False

    def hit(self):
        if self.invincible:
            return False
        self.lives -= 1
        self.invincible = True
        self.invincible_timer = pygame.time.get_ticks()
        self.visible = True
        self.flicker_timer = 0
        return True

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)