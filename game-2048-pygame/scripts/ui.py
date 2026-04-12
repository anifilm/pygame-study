import pygame
from settings import *


class UI:
    def __init__(self, surface):
        self.surface = surface
        self.title_font = pygame.font.SysFont('Arial', TITLE_FONT_SIZE, bold=True)
        self.score_font = pygame.font.SysFont('Arial', SCORE_FONT_SIZE, bold=True)
        self.score_label_font = pygame.font.SysFont('Arial', SCORE_LABEL_FONT_SIZE, bold=True)
        self.button_font = pygame.font.SysFont('Arial', BUTTON_FONT_SIZE, bold=True)
        self.tile_fonts = {
            size: pygame.font.SysFont('Arial', size, bold=True)
            for size in FONT_SIZES.values()
        }
        self.new_game_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)

    def _get_tile_font(self, value):
        digits = len(str(value))
        font_size = FONT_SIZES.get(digits, FONT_SIZES[4])
        return self.tile_fonts[font_size]

    def _get_tile_text_color(self, value):
        return TILE_TEXT_COLORS.get(value, DEFAULT_TEXT_COLOR)

    def _draw_rounded_rect(self, color, rect, radius=6):
        pygame.draw.rect(self.surface, color, rect, border_radius=radius)

    def _draw_text_centered(self, text, font, color, rect):
        text_surf = font.render(str(text), True, color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.surface.blit(text_surf, text_rect)

    def _cell_rect(self, row, col):
        x = BOARD_OFFSET_X + CELL_GAP + col * (CELL_SIZE + CELL_GAP)
        y = BOARD_OFFSET_Y + CELL_GAP + row * (CELL_SIZE + CELL_GAP)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def _pixel_pos(self, row, col):
        x = BOARD_OFFSET_X + CELL_GAP + col * (CELL_SIZE + CELL_GAP)
        y = BOARD_OFFSET_Y + CELL_GAP + row * (CELL_SIZE + CELL_GAP)
        return (x, y)

    def draw_header(self, score, best_score):
        title_surf = self.title_font.render('2048', True, '#776e65')
        self.surface.blit(title_surf, (WINDOW_PADDING, WINDOW_PADDING))

        self._draw_score_box(WINDOW_WIDTH - WINDOW_PADDING - 120, WINDOW_PADDING, 'SCORE', score)
        self._draw_score_box(WINDOW_WIDTH - WINDOW_PADDING - 260, WINDOW_PADDING, 'BEST', best_score)

        self.new_game_rect.x = WINDOW_WIDTH - WINDOW_PADDING - BUTTON_WIDTH
        self.new_game_rect.y = WINDOW_PADDING + 70
        self._draw_rounded_rect(BUTTON_COLOR, self.new_game_rect, 6)
        self._draw_text_centered('New Game', self.button_font, BUTTON_TEXT_COLOR, self.new_game_rect)

    def _draw_score_box(self, x, y, label, value):
        box_rect = pygame.Rect(x, y, 120, 60)
        self._draw_rounded_rect(BOARD_COLOR, box_rect, 6)
        label_surf = self.score_label_font.render(label, True, '#eee4da')
        label_rect = label_surf.get_rect(centerx=box_rect.centerx, top=box_rect.top + 6)
        self.surface.blit(label_surf, label_rect)
        value_surf = self.score_font.render(str(value), True, '#ffffff')
        value_rect = value_surf.get_rect(centerx=box_rect.centerx, top=box_rect.top + 28)
        self.surface.blit(value_surf, value_rect)

    def _draw_tile_at(self, value, cx, cy, scale=1.0):
        if value == 0:
            return
        size = int(CELL_SIZE * scale)
        offset = (CELL_SIZE - size) // 2
        tile_rect = pygame.Rect(int(cx) + offset, int(cy) + offset, size, size)
        color = TILE_COLORS.get(value, '#3c3a32')
        self._draw_rounded_rect(color, tile_rect, 6)
        text_color = self._get_tile_text_color(value)
        font = self._get_tile_font(value)
        self._draw_text_centered(value, font, text_color, tile_rect)

    def draw_board(self, grid):
        board_rect = pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_SIZE, BOARD_SIZE)
        self._draw_rounded_rect(BOARD_COLOR, board_rect, 8)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell_rect = self._cell_rect(r, c)
                self._draw_rounded_rect(EMPTY_CELL_COLOR, cell_rect, 6)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = grid[r][c]
                if value != 0:
                    px, py = self._pixel_pos(r, c)
                    self._draw_tile_at(value, px, py)

    def draw_board_animated(self, grid, anim_manager):
        board_rect = pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_SIZE, BOARD_SIZE)
        self._draw_rounded_rect(BOARD_COLOR, board_rect, 8)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell_rect = self._cell_rect(r, c)
                self._draw_rounded_rect(EMPTY_CELL_COLOR, cell_rect, 6)

        spawn_pos = None
        if anim_manager.spawn_info:
            spawn_pos = (anim_manager.spawn_info[0], anim_manager.spawn_info[1])

        if anim_manager.state == 'sliding':
            t = anim_manager.get_slide_progress()
            moved_to = set()
            for fr, fc, tr, tc, v in anim_manager.slide_animations:
                moved_to.add((tr, tc))
                from_px, from_py = self._pixel_pos(fr, fc)
                to_px, to_py = self._pixel_pos(tr, tc)
                px = from_px + (to_px - from_px) * t
                py = from_py + (to_py - from_py) * t
                self._draw_tile_at(v, px, py)

            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if grid[r][c] != 0 and (r, c) not in moved_to and (r, c) != spawn_pos:
                        px, py = self._pixel_pos(r, c)
                        self._draw_tile_at(grid[r][c], px, py)

        elif anim_manager.state == 'spawning':
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if grid[r][c] != 0:
                        px, py = self._pixel_pos(r, c)
                        if (r, c) == spawn_pos:
                            self._draw_tile_at(grid[r][c], px, py, anim_manager.get_spawn_progress())
                        else:
                            self._draw_tile_at(grid[r][c], px, py)

    def draw_game_over(self):
        overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
        overlay.fill((*pygame.Color(OVERLAY_COLOR)[:3], OVERLAY_ALPHA))
        self.surface.blit(overlay, (BOARD_OFFSET_X, BOARD_OFFSET_Y))

        go_font = pygame.font.SysFont('Arial', 52, bold=True)
        hint_font = pygame.font.SysFont('Arial', 20)
        go_text = go_font.render('Game Over!', True, OVERLAY_TEXT_COLOR)
        hint_text = hint_font.render('Press R to restart', True, OVERLAY_TEXT_COLOR)

        center_x = BOARD_OFFSET_X + BOARD_SIZE // 2
        center_y = BOARD_OFFSET_Y + BOARD_SIZE // 2
        self.surface.blit(go_text, go_text.get_rect(center=(center_x, center_y - 20)))
        self.surface.blit(hint_text, hint_text.get_rect(center=(center_x, center_y + 30)))

    def is_new_game_clicked(self, pos):
        return self.new_game_rect.collidepoint(pos)