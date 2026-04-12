import pygame
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, color, is_player=True):
        super().__init__()
        self.speed = speed
        self.is_player = is_player
        self.image = self._create_sprite(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        if is_player:
            self.rect.bottom = y
        else:
            self.rect.top = y

    def _create_sprite(self, color):
        surf = pygame.Surface((4, 12), pygame.SRCALPHA)
        c = pygame.Color(color)
        pygame.draw.rect(surf, c, (0, 0, 4, 12))
        return surf

    def update(self):
        self.rect.y -= self.speed
        if self.is_player:
            if self.rect.bottom < GAME_TOP:
                self.kill()
        else:
            if self.rect.top > GAME_BOTTOM:
                self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BulletManager:
    def __init__(self):
        self.player_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

    def player_shoot(self, x, y):
        if len(self.player_bullets) < 1:
            bullet = Bullet(x, y, PLAYER_BULLET_SPEED, COLORS['bullet_player'], True)
            self.player_bullets.add(bullet)

    def alien_shoot(self, x, y):
        bullet = Bullet(x, y, ALIEN_BULLET_SPEED, COLORS['bullet_alien'], False)
        self.alien_bullets.add(bullet)

    def update(self):
        self.player_bullets.update()
        self.alien_bullets.update()

    def draw(self, surface):
        self.player_bullets.draw(surface)
        self.alien_bullets.draw(surface)