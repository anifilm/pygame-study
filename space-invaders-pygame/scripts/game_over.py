import pygame
from settings import *


class GameOver:
    def __init__(self):
        self.font_big = pygame.font.SysFont('arial', 48, bold=True)
        self.font_med = pygame.font.SysFont('arial', 24, bold=True)
        self.font_small = pygame.font.SysFont('arial', 18)

    def draw_game_over(self, surface, score):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        text = self.font_big.render('GAME OVER', True,
                                     pygame.Color(COLORS['red']))
        surface.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2,
                            WINDOW_HEIGHT // 2 - 60))

        score_text = self.font_med.render(f'Final Score: {score}', True,
                                          pygame.Color(COLORS['white']))
        surface.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                                   WINDOW_HEIGHT // 2))

        restart_text = self.font_small.render('Press R to Restart or ESC to Quit',
                                              True, pygame.Color(COLORS['yellow']))
        surface.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2,
                                     WINDOW_HEIGHT // 2 + 50))

    def draw_victory(self, surface, score, level):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        text = self.font_big.render(f'LEVEL {level} CLEAR!', True,
                                     pygame.Color(COLORS['green']))
        surface.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2,
                            WINDOW_HEIGHT // 2 - 60))

        score_text = self.font_med.render(f'Score: {score}', True,
                                          pygame.Color(COLORS['white']))
        surface.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                                   WINDOW_HEIGHT // 2))

        cont_text = self.font_small.render('Press SPACE for Next Level',
                                           True, pygame.Color(COLORS['yellow']))
        surface.blit(cont_text, (WINDOW_WIDTH // 2 - cont_text.get_width() // 2,
                                   WINDOW_HEIGHT // 2 + 50))

    def draw_start_screen(self, surface):
        surface.fill(pygame.Color(COLORS['bg']))

        title = self.font_big.render('SPACE INVADERS', True,
                                     pygame.Color(COLORS['green']))
        surface.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2,
                              WINDOW_HEIGHT // 3))

        subtitle = self.font_med.render('A Pygame Clone', True,
                                        pygame.Color(COLORS['cyan']))
        surface.blit(subtitle, (WINDOW_WIDTH // 2 - subtitle.get_width() // 2,
                                 WINDOW_HEIGHT // 3 + 60))

        start = self.font_small.render('Press SPACE to Start', True,
                                        pygame.Color(COLORS['yellow']))
        surface.blit(start, (WINDOW_WIDTH // 2 - start.get_width() // 2,
                              WINDOW_HEIGHT // 2 + 50))

        controls = self.font_small.render('← → Move  |  SPACE Shoot  |  P Pause',
                                          True, pygame.Color(COLORS['white']))
        surface.blit(controls, (WINDOW_WIDTH // 2 - controls.get_width() // 2,
                                 WINDOW_HEIGHT // 2 + 100))