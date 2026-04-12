from random import random, choice
from settings import GRID_SIZE


class Board:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if not empty:
            return None
        r, c = choice(empty)
        value = 4 if random() < 0.1 else 2
        self.grid[r][c] = value
        return (r, c, value)

    def _compress(self, row):
        new_row = [v for v in row if v != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row

    def _merge(self, row):
        for i in range(GRID_SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def _move_left_with_tracking(self):
        animations = []
        merges = []
        moved = False

        for r in range(GRID_SIZE):
            tiles = [(c, self.grid[r][c]) for c in range(GRID_SIZE) if self.grid[r][c] != 0]
            new_row = []
            i = 0
            while i < len(tiles):
                target_c = len(new_row)
                if i + 1 < len(tiles) and tiles[i][1] == tiles[i + 1][1]:
                    merged_val = tiles[i][1] * 2
                    self.score += merged_val
                    animations.append((r, tiles[i][0], r, target_c, tiles[i][1]))
                    animations.append((r, tiles[i + 1][0], r, target_c, tiles[i + 1][1]))
                    merges.append((r, target_c, merged_val))
                    new_row.append(merged_val)
                    i += 2
                else:
                    animations.append((r, tiles[i][0], r, target_c, tiles[i][1]))
                    new_row.append(tiles[i][1])
                    i += 1

            new_row += [0] * (GRID_SIZE - len(new_row))
            if self.grid[r] != new_row:
                moved = True
            self.grid[r] = new_row

        return moved, animations, merges

    def _rotate_cw(self):
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

    def _rotate_ccw(self):
        self.grid = [list(row) for row in zip(*self.grid)][::-1]

    @staticmethod
    def _rotate_coord_cw(r, c):
        return (c, GRID_SIZE - 1 - r)

    def _transform_animations(self, animations, merges, n_rotations):
        for _ in range(n_rotations):
            animations = [
                (*self._rotate_coord_cw(fr, fc), *self._rotate_coord_cw(tr, tc), v)
                for fr, fc, tr, tc, v in animations
            ]
            merges = [(*self._rotate_coord_cw(r, c), v) for r, c, v in merges]
        return animations, merges

    def move(self, direction):
        if self.game_over:
            return False, [], [], None

        rotations = {'left': 0, 'down': 1, 'right': 2, 'up': 3}
        n = rotations[direction]

        for _ in range(n):
            self._rotate_cw()

        moved, animations, merges = self._move_left_with_tracking()

        for _ in range((4 - n) % 4):
            self._rotate_cw()

        back_rotations = (4 - n) % 4
        animations, merges = self._transform_animations(animations, merges, back_rotations)

        spawn_info = None
        if moved:
            spawn_info = self.spawn_tile()
            self._check_game_over()

        return moved, animations, merges, spawn_info

    def _check_game_over(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 0:
                    return
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return
        for r in range(GRID_SIZE - 1):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return
        self.game_over = True

    def reset(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.spawn_tile()
        self.spawn_tile()