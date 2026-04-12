import pygame
from sys import exit
from os import path
from settings import *
from board import Board
from ui import UI
from animation import AnimationManager


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('2048')

        self.board = Board()
        self.ui = UI(self.display_surface)
        self.anim = AnimationManager()
        self.best_score = self._load_best_score()

    def _load_best_score(self):
        try:
            score_path = path.join(path.dirname(path.abspath(__file__)), '..', 'best_score.txt')
            with open(score_path, 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_best_score(self):
        score_path = path.join(path.dirname(path.abspath(__file__)), '..', 'best_score.txt')
        with open(score_path, 'w') as f:
            f.write(str(self.best_score))

    def _update_best_score(self):
        if self.board.score > self.best_score:
            self.best_score = self.board.score
            self._save_best_score()

    def _reset_game(self):
        self._update_best_score()
        self.board.reset()
        self.anim = AnimationManager()

    def _handle_move(self, direction):
        moved, animations, merges, spawn_info = self.board.move(direction)
        if moved:
            self._update_best_score()
            self.anim.start(animations, merges, spawn_info)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._update_best_score()
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.ui.is_new_game_clicked(event.pos):
                        self._reset_game()

                if event.type == pygame.KEYDOWN and not self.anim.is_animating():
                    if event.key == pygame.K_r:
                        self._reset_game()
                    elif not self.board.game_over:
                        direction_map = {
                            pygame.K_LEFT: 'left',
                            pygame.K_RIGHT: 'right',
                            pygame.K_UP: 'up',
                            pygame.K_DOWN: 'down',
                        }
                        direction = direction_map.get(event.key)
                        if direction:
                            self._handle_move(direction)

            self.anim.update()

            self.display_surface.fill(BG_COLOR)
            self.ui.draw_header(self.board.score, self.best_score)

            if self.anim.is_animating():
                self.ui.draw_board_animated(self.board.grid, self.anim)
            else:
                self.ui.draw_board(self.board.grid)

            if self.board.game_over and not self.anim.is_animating():
                self.ui.draw_game_over()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    main = Main()
    main.run()