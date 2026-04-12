import pygame
from settings import *


class Score:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.font = pygame.font.SysFont('arial', 20, bold=True)
        self.big_font = pygame.font.SysFont('arial', 36, bold=True)

    def add_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def reset(self):
        self.score = 0

    def next_level(self):
        self.level += 1

    def draw(self, surface, lives):
        pygame.draw.rect(surface, pygame.Color(COLORS['hud_bg']),
                         (0, 0, WINDOW_WIDTH, HUD_HEIGHT))

        score_text = self.font.render(f'SCORE: {self.score}', True,
                                      pygame.Color(COLORS['white']))
        surface.blit(score_text, (PADDING, 10))

        hi_text = self.font.render(f'HI: {self.high_score}', True,
                                   pygame.Color(COLORS['white']))
        surface.blit(hi_text, (WINDOW_WIDTH // 2 - hi_text.get_width() // 2, 10))

        level_text = self.font.render(f'LEVEL {self.level}', True,
                                      pygame.Color(COLORS['yellow']))
        surface.blit(level_text, (WINDOW_WIDTH // 2 + 100, 10))

        for i in range(lives):
            player_icon = pygame.Surface((20, 14), pygame.SRCALPHA)
            pygame.draw.polygon(player_icon, pygame.Color(COLORS['cyan']),
                                [(10, 0), (20, 14), (0, 14)])
            surface.blit(player_icon, (WINDOW_WIDTH - PADDING - 25 * (i + 1), 10))