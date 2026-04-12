import pygame
from settings import *

ALIEN_COLOR_MAP = {
    'top': COLORS['alien_top'],
    'mid': COLORS['alien_mid'],
    'bottom': COLORS['alien_bottom'],
}

class Explosion:
    def __init__(self, x, y, color='white', duration=300):
        self.x = x
        self.y = y
        resolved = ALIEN_COLOR_MAP.get(color, COLORS.get(color, color))
        self.color = pygame.Color(resolved)
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.active = True
        self.frame = 0

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        progress = elapsed / self.duration
        self.frame = min(int(progress * 4), 3)
        if elapsed >= self.duration:
            self.active = False

    def draw(self, surface):
        if not self.active:
            return
        radius = 8 + self.frame * 6
        alpha = max(0, 255 - self.frame * 70)
        s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        c = (self.color.r, self.color.g, self.color.b, alpha)
        pygame.draw.circle(s, c, (radius, radius), radius)
        inner_c = (self.color.r, self.color.g, self.color.b, min(255, alpha + 50))
        pygame.draw.circle(s, inner_c, (radius, radius), max(1, radius // 2))
        surface.blit(s, (self.x - radius, self.y - radius))


class ExplosionManager:
    def __init__(self):
        self.explosions = []

    def add(self, x, y, color='white', duration=300):
        self.explosions.append(Explosion(x, y, color, duration))

    def update(self):
        for exp in self.explosions:
            exp.update()
        self.explosions = [e for e in self.explosions if e.active]

    def draw(self, surface):
        for exp in self.explosions:
            exp.draw(surface)