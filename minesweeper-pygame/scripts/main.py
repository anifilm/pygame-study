import pygame
from sys import exit
from settings import *
from themes import THEMES, DEFAULT_THEME
from board import Board
from ui import UI
from menu import Menu, MENU_WIDTH, MENU_HEIGHT


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Minesweeper')
        self.clock = pygame.time.Clock()

        self.theme_name = DEFAULT_THEME
        self.theme      = THEMES[self.theme_name]

        self.display_surface = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
        self.scene  = 'menu'
        self.menu   = Menu(self.display_surface, self.theme, self.theme_name)

        self.difficulty = None
        self.board      = None
        self.ui         = None

    def _start_game(self, difficulty):
        self.difficulty = difficulty
        self.board = Board(difficulty)
        cfg   = DIFFICULTIES[difficulty]
        win_w = cfg['cols'] * CELL_SIZE + BOARD_PADDING * 2
        win_h = HEADER_HEIGHT + cfg['rows'] * CELL_SIZE + BOARD_PADDING * 2
        self.display_surface = pygame.display.set_mode((win_w, win_h))
        self.ui    = UI(self.display_surface, self.theme)
        self.scene = 'game'

    def _back_to_menu(self):
        self.display_surface = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
        self.menu  = Menu(self.display_surface, self.theme, self.theme_name)
        self.scene = 'menu'
        self.board = None
        self.ui    = None

    def _set_theme(self, name):
        self.theme_name = name
        self.theme      = THEMES[name]

    def _reset_game(self, difficulty=None):
        self._start_game(difficulty or self.difficulty)

    def run(self):
        DOUBLE_CLICK_MS = 400
        last_click_time = 0
        last_click_cell = None

        while True:
            # ── 메뉴 씬 ─────────────────────────────────────────────── #
            if self.scene == 'menu':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    result = self.menu.handle_event(event)
                    if result:
                        if result['action'] == 'theme':
                            self._set_theme(result['theme'])
                            self.menu = Menu(self.display_surface, self.theme, self.theme_name)
                        elif result['action'] == 'start':
                            self._start_game(result['difficulty'])
                            last_click_time = 0
                            last_click_cell = None

                    # 메뉴에서 키보드 단축키
                    if event.type == pygame.KEYDOWN:
                        key = event.key
                        if key == pygame.K_r:
                            difficulty = self.difficulty or DEFAULT_DIFFICULTY
                        elif key == pygame.K_1:
                            difficulty = 'beginner'
                        elif key == pygame.K_2:
                            difficulty = 'intermediate'
                        elif key == pygame.K_3:
                            difficulty = 'expert'
                        else:
                            difficulty = None
                        if difficulty:
                            self._start_game(difficulty)
                            last_click_time = 0
                            last_click_cell = None

                if self.scene == 'menu':
                    self.menu.draw()

            # ── 게임 씬 ─────────────────────────────────────────────── #
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos

                        if self.ui.is_smiley_clicked(pos):
                            self._reset_game()
                            last_click_time = 0
                            last_click_cell = None
                            continue

                        # 팝업 버튼 처리 (게임 종료 시)
                        if self.board.game_state in (GAME_WON, GAME_LOST):
                            if event.button == 1:
                                if self.ui.is_popup_again_clicked(pos):
                                    self._reset_game()
                                elif self.ui.is_popup_menu_clicked(pos):
                                    self._back_to_menu()
                            continue

                        cell = self.ui.get_cell_at(pos, self.board.rows, self.board.cols)
                        if cell is None:
                            continue
                        row, col = cell

                        if event.button == 1:
                            now = pygame.time.get_ticks()
                            if cell == last_click_cell and now - last_click_time < DOUBLE_CLICK_MS:
                                self.board.chord(row, col)
                            else:
                                self.board.reveal(row, col)
                            last_click_time = now
                            last_click_cell = cell

                        elif event.button == 3:
                            self.board.toggle_flag(row, col)

                        elif event.button == 2:
                            self.board.chord(row, col)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self._back_to_menu()
                        elif event.key == pygame.K_r:
                            self._reset_game()
                            last_click_time = 0
                            last_click_cell = None
                        elif event.key == pygame.K_1:
                            self._reset_game('beginner')
                        elif event.key == pygame.K_2:
                            self._reset_game('intermediate')
                        elif event.key == pygame.K_3:
                            self._reset_game('expert')

                if self.scene == 'game':
                    self.board.update_timer()
                    self.display_surface.fill(self.theme['COLOR_BG'])
                    self.ui.draw_header(
                        self.board.mine_counter,
                        self.board.elapsed_seconds,
                        self.board.game_state,
                        self.board.cols
                    )
                    self.ui.draw_board(self.board)
                    if self.board.game_state in (GAME_WON, GAME_LOST):
                        self.ui.draw_popup(self.board.game_state, self.board.elapsed_seconds)
                    pygame.display.update()

            self.clock.tick(60)


if __name__ == '__main__':
    main = Main()
    main.run()
