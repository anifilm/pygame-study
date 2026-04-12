import pygame
from random import sample
from collections import deque
from settings import *


class Board:
    def __init__(self, difficulty=DEFAULT_DIFFICULTY):
        self._difficulty = difficulty
        cfg = DIFFICULTIES[difficulty]
        self.cols        = cfg['cols']
        self.rows        = cfg['rows']
        self.total_mines = cfg['mines']

        self.mines  = [[False]        * self.cols for _ in range(self.rows)]
        self.counts = [[0]            * self.cols for _ in range(self.rows)]
        self.states = [[STATE_HIDDEN] * self.cols for _ in range(self.rows)]

        self.flags_placed   = 0
        self.cells_revealed = 0
        self.total_safe     = self.rows * self.cols - self.total_mines

        self.start_ticks    = None
        self.elapsed_seconds = 0

        self.game_state = GAME_WAITING

    # ------------------------------------------------------------------ #
    #  지뢰 배치                                                           #
    # ------------------------------------------------------------------ #

    def _place_mines(self, safe_row, safe_col):
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]

        exclusion = set()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = safe_row + dr, safe_col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    exclusion.add((nr, nc))

        candidates = [(r, c) for (r, c) in all_cells if (r, c) not in exclusion]
        if len(candidates) < self.total_mines:
            candidates = [(r, c) for (r, c) in all_cells if (r, c) != (safe_row, safe_col)]

        mine_cells = sample(candidates, self.total_mines)
        for r, c in mine_cells:
            self.mines[r][c] = True

        self._compute_counts()

    def _compute_counts(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mines[r][c]:
                    self.counts[r][c] = -1
                    continue
                total = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.mines[nr][nc]:
                                total += 1
                self.counts[r][c] = total

    # ------------------------------------------------------------------ #
    #  홍수 채우기                                                          #
    # ------------------------------------------------------------------ #

    def _flood_fill(self, row, col):
        queue   = deque()
        visited = set()
        queue.append((row, col))
        visited.add((row, col))

        while queue:
            r, c = queue.popleft()
            if self.states[r][c] == STATE_HIDDEN:
                self.states[r][c] = STATE_REVEALED
                self.cells_revealed += 1

            if self.counts[r][c] == 0:
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < self.rows and 0 <= nc < self.cols
                                and (nr, nc) not in visited
                                and self.states[nr][nc] == STATE_HIDDEN):
                            visited.add((nr, nc))
                            queue.append((nr, nc))

    # ------------------------------------------------------------------ #
    #  공개 / 플래그 / 코드                                                 #
    # ------------------------------------------------------------------ #

    def reveal(self, row, col):
        if self.game_state in (GAME_WON, GAME_LOST):
            return False
        if self.states[row][col] != STATE_HIDDEN:
            return False

        if self.game_state == GAME_WAITING:
            self._place_mines(row, col)
            self.start_ticks = pygame.time.get_ticks()
            self.game_state  = GAME_ACTIVE

        if self.mines[row][col]:
            self.states[row][col] = STATE_EXPLODED
            self._reveal_all_mines()
            self.game_state = GAME_LOST
            return True

        self._flood_fill(row, col)
        self._check_win()
        return True

    def toggle_flag(self, row, col):
        if self.game_state not in (GAME_WAITING, GAME_ACTIVE):
            return False
        state = self.states[row][col]
        if state == STATE_HIDDEN:
            self.states[row][col] = STATE_FLAGGED
            self.flags_placed += 1
        elif state == STATE_FLAGGED:
            self.states[row][col] = STATE_QUESTION
            self.flags_placed -= 1
        elif state == STATE_QUESTION:
            self.states[row][col] = STATE_HIDDEN
        return True

    def chord(self, row, col):
        if self.states[row][col] != STATE_REVEALED:
            return False
        count = self.counts[row][col]
        if count <= 0:
            return False

        neighbours = [
            (row + dr, col + dc)
            for dr in (-1, 0, 1)
            for dc in (-1, 0, 1)
            if not (dr == 0 and dc == 0)
            and 0 <= row + dr < self.rows
            and 0 <= col + dc < self.cols
        ]
        adjacent_flags = sum(
            1 for r, c in neighbours if self.states[r][c] == STATE_FLAGGED
        )
        if adjacent_flags != count:
            return False

        for r, c in neighbours:
            if self.states[r][c] == STATE_HIDDEN:
                self.reveal(r, c)
        return True

    # ------------------------------------------------------------------ #
    #  내부 헬퍼                                                            #
    # ------------------------------------------------------------------ #

    def _reveal_all_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mines[r][c] and self.states[r][c] == STATE_HIDDEN:
                    self.states[r][c] = STATE_MINE_SHOW
                if not self.mines[r][c] and self.states[r][c] == STATE_FLAGGED:
                    self.states[r][c] = STATE_WRONG_FLAG

    def _check_win(self):
        if self.cells_revealed == self.total_safe:
            self.game_state = GAME_WON
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.mines[r][c] and self.states[r][c] == STATE_HIDDEN:
                        self.states[r][c] = STATE_FLAGGED
                        self.flags_placed += 1

    # ------------------------------------------------------------------ #
    #  타이머 / 프로퍼티                                                    #
    # ------------------------------------------------------------------ #

    def update_timer(self):
        if self.game_state == GAME_ACTIVE and self.start_ticks is not None:
            raw = (pygame.time.get_ticks() - self.start_ticks) // 1000
            self.elapsed_seconds = min(raw, 999)

    @property
    def mine_counter(self):
        return self.total_mines - self.flags_placed

    def reset(self, difficulty=None):
        self.__init__(difficulty or self._difficulty)
