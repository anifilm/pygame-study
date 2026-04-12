import pygame
import math
from settings import *


class UI:
    def __init__(self, surface, theme):
        self.surface     = surface
        self.T           = theme
        self.number_font      = pygame.font.SysFont('arial', 17, bold=True)
        self.lcd_font         = pygame.font.SysFont('arial', 20, bold=True)
        self.popup_title_font = pygame.font.SysFont('arial', 26, bold=True)
        self.popup_sub_font   = pygame.font.SysFont('arial', 15)
        self.popup_btn_font   = pygame.font.SysFont('arial', 15, bold=True)
        self.smiley_rect      = pygame.Rect(0, 0, SMILEY_SIZE, SMILEY_SIZE)
        self.popup_again_rect = None
        self.popup_menu_rect  = None

    # ------------------------------------------------------------------ #
    #  헤더                                                                #
    # ------------------------------------------------------------------ #

    def draw_header(self, mine_counter, elapsed, game_state, cols):
        win_w = self.surface.get_width()
        cy    = HEADER_HEIGHT // 2

        if self.T['name'] == 'classic':
            self._draw_header_classic(win_w)
        else:
            self._draw_header_modern(win_w)

        lcd_left = pygame.Rect(HEADER_PADDING, cy - LCD_HEIGHT // 2, LCD_WIDTH, LCD_HEIGHT)
        self._draw_lcd(mine_counter, lcd_left)

        self.smiley_rect.center = (win_w // 2, cy)
        self._draw_reset_button(self.smiley_rect, game_state)

        lcd_right = pygame.Rect(win_w - HEADER_PADDING - LCD_WIDTH, cy - LCD_HEIGHT // 2, LCD_WIDTH, LCD_HEIGHT)
        self._draw_lcd(elapsed, lcd_right)

    def _draw_header_classic(self, win_w):
        pygame.draw.rect(self.surface, self.T['COLOR_HEADER_BG'],
                         pygame.Rect(0, 0, win_w, HEADER_HEIGHT))
        panel = pygame.Rect(HEADER_PADDING, HEADER_PADDING,
                            win_w - HEADER_PADDING * 2, HEADER_HEIGHT - HEADER_PADDING * 2)
        self._bevel_sunken(panel, self.T['BORDER_WIDTH'])

    def _draw_header_modern(self, win_w):
        pygame.draw.rect(self.surface, self.T['COLOR_HEADER_BG'],
                         pygame.Rect(0, 0, win_w, HEADER_HEIGHT))
        pygame.draw.line(self.surface, self.T['COLOR_HEADER_BORDER'],
                         (0, HEADER_HEIGHT - 1), (win_w, HEADER_HEIGHT - 1))

    def _draw_lcd(self, value, rect):
        radius = 4 if self.T['name'] == 'dark' else 0
        pygame.draw.rect(self.surface, self.T['LCD_BG_COLOR'], rect, border_radius=radius)
        display = max(-99, min(999, value))
        text = f'{display:03d}' if display >= 0 else f'-{abs(display):02d}'
        surf = self.lcd_font.render(text, True, self.T['LCD_COLOR_ON'])
        self.surface.blit(surf, surf.get_rect(center=rect.center))

    def _draw_reset_button(self, rect, game_state):
        cx, cy = rect.center

        if self.T['name'] == 'classic':
            self._bevel_raised(rect, self.T['BORDER_WIDTH'])
            face_color = (255, 220, 0)
            face_r     = rect.width // 2 - 4
            pygame.draw.circle(self.surface, face_color, (cx, cy), face_r)
            pygame.draw.circle(self.surface, (0, 0, 0), (cx, cy), face_r, 1)
            draw_color = (0, 0, 0)
        else:
            if game_state == GAME_WON:
                bg, face_color = (30, 70, 40), (74, 222, 128)
            elif game_state == GAME_LOST:
                bg, face_color = (70, 20, 20), (248, 113, 113)
            else:
                bg, face_color = (38, 38, 66), (255, 210, 60)
            r = rect.width // 2
            pygame.draw.circle(self.surface, bg, (cx, cy), r)
            pygame.draw.circle(self.surface, face_color, (cx, cy), r, 2)
            face_r = r - 5
            pygame.draw.circle(self.surface, face_color, (cx, cy), face_r)
            draw_color = bg

        # 표정 그리기
        if game_state == GAME_WON:
            pygame.draw.circle(self.surface, draw_color, (cx - 4, cy - 3), 3)
            pygame.draw.circle(self.surface, draw_color, (cx + 4, cy - 3), 3)
            pygame.draw.line(self.surface, draw_color, (cx - 7, cy - 3), (cx + 7, cy - 3), 1)
            pygame.draw.arc(self.surface, draw_color,
                            pygame.Rect(cx - 5, cy + 1, 10, 6), math.pi, 0, 2)
        elif game_state == GAME_LOST:
            for ox in (-4, 4):
                pygame.draw.line(self.surface, draw_color,
                                 (cx + ox - 2, cy - 5), (cx + ox + 2, cy - 1), 2)
                pygame.draw.line(self.surface, draw_color,
                                 (cx + ox + 2, cy - 5), (cx + ox - 2, cy - 1), 2)
            pygame.draw.arc(self.surface, draw_color,
                            pygame.Rect(cx - 5, cy + 3, 10, 6), 0, math.pi, 2)
        else:
            pygame.draw.circle(self.surface, draw_color, (cx - 4, cy - 3), 2)
            pygame.draw.circle(self.surface, draw_color, (cx + 4, cy - 3), 2)
            pygame.draw.arc(self.surface, draw_color,
                            pygame.Rect(cx - 5, cy + 1, 10, 6), math.pi, 0, 2)

    # ------------------------------------------------------------------ #
    #  보드                                                                #
    # ------------------------------------------------------------------ #

    def draw_board(self, board):
        for r in range(board.rows):
            for c in range(board.cols):
                slot = pygame.Rect(BOARD_PADDING + c * CELL_SIZE,
                                   HEADER_HEIGHT + BOARD_PADDING + r * CELL_SIZE,
                                   CELL_SIZE, CELL_SIZE)
                self._draw_cell(slot, board.states[r][c], board.counts[r][c])

    def _draw_cell(self, slot, state, count):
        inset  = self.T['CELL_INSET']
        radius = self.T['CELL_RADIUS']
        inner  = slot.inflate(-inset * 2, -inset * 2)

        if state == STATE_HIDDEN:
            self._draw_hidden_cell(inner)

        elif state == STATE_QUESTION:
            self._draw_hidden_cell(inner)
            q_color = (167, 139, 250) if self.T['name'] == 'dark' else (0, 0, 128)
            surf = self.number_font.render('?', True, q_color)
            self.surface.blit(surf, surf.get_rect(center=inner.center))

        elif state == STATE_FLAGGED:
            self._draw_hidden_cell(inner)
            self._draw_flag(inner)

        elif state == STATE_REVEALED:
            self._draw_revealed_cell(inner, radius)
            if count > 0:
                self._draw_number(inner, count)

        elif state == STATE_EXPLODED:
            pygame.draw.rect(self.surface, self.T['COLOR_EXPLODED_BG'], inner, border_radius=radius)
            self._draw_mine(inner)

        elif state == STATE_MINE_SHOW:
            self._draw_revealed_cell(inner, radius)
            self._draw_mine(inner)

        elif state == STATE_WRONG_FLAG:
            self._draw_revealed_cell(inner, radius)
            self._draw_flag(inner)
            self._draw_red_x(inner)

    def _draw_hidden_cell(self, rect):
        if self.T['name'] == 'classic':
            self._bevel_raised(rect, self.T['BORDER_WIDTH'])
        else:
            r = self.T['CELL_RADIUS']
            pygame.draw.rect(self.surface, self.T['COLOR_CELL_HIDDEN'], rect, border_radius=r)
            x, y, w, h = rect
            pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                             (x + r, y + 1), (x + w - r, y + 1))
            pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                             (x + 1, y + r), (x + 1, y + h - r))
            pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                             (x + r, y + h - 2), (x + w - r, y + h - 2))
            pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                             (x + w - 2, y + r), (x + w - 2, y + h - r))

    def _draw_revealed_cell(self, rect, radius):
        if self.T['name'] == 'classic':
            pygame.draw.rect(self.surface, self.T['COLOR_CELL_REVEALED'], rect)
            pygame.draw.rect(self.surface, self.T['COLOR_CELL_SHADOW'], rect, 1)
        else:
            pygame.draw.rect(self.surface, self.T['COLOR_CELL_REVEALED'], rect, border_radius=radius)

    # ------------------------------------------------------------------ #
    #  Bevel 프리미티브 (Classic 테마 전용)                                 #
    # ------------------------------------------------------------------ #

    def _bevel_raised(self, rect, b):
        pygame.draw.rect(self.surface, self.T['COLOR_CELL_HIDDEN'], rect)
        x, y, w, h = rect
        for i in range(b):
            pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                             (x+i, y+i), (x+w-i-1, y+i))
            pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                             (x+i, y+i), (x+i, y+h-i-1))
            pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                             (x+w-i-1, y+i+1), (x+w-i-1, y+h-i-1))
            pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                             (x+i+1, y+h-i-1), (x+w-i-1, y+h-i-1))

    def _bevel_sunken(self, rect, b):
        pygame.draw.rect(self.surface, self.T['COLOR_CELL_HIDDEN'], rect)
        x, y, w, h = rect
        for i in range(b):
            pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                             (x+i, y+i), (x+w-i-1, y+i))
            pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                             (x+i, y+i), (x+i, y+h-i-1))
            pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                             (x+w-i-1, y+i+1), (x+w-i-1, y+h-i-1))
            pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                             (x+i+1, y+h-i-1), (x+w-i-1, y+h-i-1))

    # ------------------------------------------------------------------ #
    #  셀 콘텐츠                                                            #
    # ------------------------------------------------------------------ #

    def _draw_number(self, rect, count):
        color = self.T['NUMBER_COLORS'].get(count, (0, 0, 0))
        surf  = self.number_font.render(str(count), True, color)
        self.surface.blit(surf, surf.get_rect(center=rect.center))

    def _draw_mine(self, rect):
        cx, cy    = rect.center
        r_body    = rect.width // 5
        spike_len = rect.width // 3
        color     = self.T['MINE_COLOR']
        for deg in range(0, 360, 45):
            angle = math.radians(deg)
            pygame.draw.line(self.surface, color, (cx, cy),
                             (cx + int(math.cos(angle) * spike_len),
                              cy + int(math.sin(angle) * spike_len)), 2)
        pygame.draw.circle(self.surface, color, (cx, cy), r_body)
        hl = tuple(min(255, c + 80) for c in color)
        pygame.draw.circle(self.surface, hl,
                           (cx - r_body // 3, cy - r_body // 3), max(2, r_body // 3))

    def _draw_flag(self, rect):
        cx, cy   = rect.center
        pole_x   = cx + 2
        pole_top = cy - rect.height // 5
        pole_bot = cy + rect.height // 5
        pygame.draw.line(self.surface, self.T['FLAG_POLE'],
                         (pole_x, pole_top), (pole_x, pole_bot), 2)
        pygame.draw.polygon(self.surface, self.T['FLAG_COLOR'], [
            (pole_x,                    pole_top),
            (pole_x,                    pole_top + rect.height // 5),
            (pole_x - rect.width // 4,  pole_top + rect.height // 10),
        ])
        pygame.draw.line(self.surface, self.T['FLAG_POLE'],
                         (cx - rect.width // 6, pole_bot + 2),
                         (cx + rect.width // 4,  pole_bot + 2), 2)

    def _draw_red_x(self, rect):
        x, y, w, h = rect
        m = 6
        pygame.draw.line(self.surface, self.T['X_COLOR'],
                         (x+m, y+m), (x+w-m, y+h-m), 2)
        pygame.draw.line(self.surface, self.T['X_COLOR'],
                         (x+w-m, y+m), (x+m, y+h-m), 2)

    # ------------------------------------------------------------------ #
    #  팝업 (게임 오버 / 클리어)                                             #
    # ------------------------------------------------------------------ #

    def draw_popup(self, game_state, elapsed):
        if game_state not in (GAME_WON, GAME_LOST):
            return

        win_w, win_h = self.surface.get_size()
        is_win = (game_state == GAME_WON)

        # 반투명 오버레이
        overlay = pygame.Surface((win_w, win_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150 if self.T['name'] == 'dark' else 90))
        self.surface.blit(overlay, (0, 0))

        # 팝업 패널
        pop_w = 250
        pop_h = 188 if is_win else 170
        px = (win_w - pop_w) // 2
        py = (win_h - pop_h) // 2
        pop_rect = pygame.Rect(px, py, pop_w, pop_h)

        accent = (74, 222, 128) if is_win else (248, 113, 113)

        # 팝업 패널 — 70% 불투명 (alpha=178)
        ALPHA = 178
        panel = pygame.Surface((pop_w, pop_h), pygame.SRCALPHA)
        if self.T['name'] == 'dark':
            pygame.draw.rect(panel, (22, 22, 40, ALPHA),
                             panel.get_rect(), border_radius=14)
            pygame.draw.rect(panel, (*accent, ALPHA),
                             panel.get_rect(), width=2, border_radius=14)
        else:
            pygame.draw.rect(panel, (*self.T['COLOR_CELL_HIDDEN'], ALPHA),
                             panel.get_rect())
            x, y, w, h = 0, 0, pop_w, pop_h
            for i in range(3):
                pygame.draw.line(panel, self.T['COLOR_CELL_LIGHT'],
                                 (x+i, y+i), (x+w-i-1, y+i))
                pygame.draw.line(panel, self.T['COLOR_CELL_LIGHT'],
                                 (x+i, y+i), (x+i, y+h-i-1))
                pygame.draw.line(panel, self.T['COLOR_CELL_SHADOW'],
                                 (x+w-i-1, y+i+1), (x+w-i-1, y+h-i-1))
                pygame.draw.line(panel, self.T['COLOR_CELL_SHADOW'],
                                 (x+i+1, y+h-i-1), (x+w-i-1, y+h-i-1))
        self.surface.blit(panel, (px, py))

        # 제목
        title = 'YOU WIN!' if is_win else 'GAME OVER'
        if self.T['name'] == 'dark':
            title_color = accent
        else:
            title_color = (0, 0, 160) if is_win else (180, 0, 0)
        title_surf = self.popup_title_font.render(title, True, title_color)
        self.surface.blit(title_surf,
                          title_surf.get_rect(centerx=pop_rect.centerx, top=pop_rect.top + 22))

        # 서브 텍스트
        if is_win:
            sub = f'Cleared in  {elapsed}s'
        else:
            sub = 'Better luck next time!'
        sub_color = (180, 180, 200) if self.T['name'] == 'dark' else (70, 70, 70)
        sub_surf = self.popup_sub_font.render(sub, True, sub_color)
        self.surface.blit(sub_surf,
                          sub_surf.get_rect(centerx=pop_rect.centerx, top=pop_rect.top + 66))

        # 버튼 배치
        btn_w, btn_h = 100, 34
        gap = 10
        total = btn_w * 2 + gap
        bx = pop_rect.centerx - total // 2
        by = pop_rect.bottom - btn_h - 22

        self.popup_again_rect = pygame.Rect(bx, by, btn_w, btn_h)
        self.popup_menu_rect  = pygame.Rect(bx + btn_w + gap, by, btn_w, btn_h)

        self._draw_popup_btn(self.popup_again_rect, 'Play Again', accent)
        menu_color = (100, 100, 130) if self.T['name'] == 'dark' else (80, 80, 80)
        self._draw_popup_btn(self.popup_menu_rect, 'Menu', menu_color)

    def _draw_popup_btn(self, rect, label, color):
        if self.T['name'] == 'dark':
            bg = tuple(max(0, int(c * 0.22)) for c in color)
            pygame.draw.rect(self.surface, bg, rect, border_radius=7)
            pygame.draw.rect(self.surface, color, rect, width=1, border_radius=7)
            surf = self.popup_btn_font.render(label, True, color)
        else:
            self._bevel_raised(rect, 2)
            surf = self.popup_btn_font.render(label, True, (0, 0, 0))
        self.surface.blit(surf, surf.get_rect(center=rect.center))

    def is_popup_again_clicked(self, pos):
        return self.popup_again_rect is not None and self.popup_again_rect.collidepoint(pos)

    def is_popup_menu_clicked(self, pos):
        return self.popup_menu_rect is not None and self.popup_menu_rect.collidepoint(pos)

    # ------------------------------------------------------------------ #
    #  유틸리티                                                             #
    # ------------------------------------------------------------------ #

    def is_smiley_clicked(self, pos):
        return self.smiley_rect.collidepoint(pos)

    def get_cell_at(self, pos, board_rows, board_cols):
        x, y = pos
        if y < HEADER_HEIGHT + BOARD_PADDING:
            return None
        col = (x - BOARD_PADDING) // CELL_SIZE
        row = (y - HEADER_HEIGHT - BOARD_PADDING) // CELL_SIZE
        if 0 <= row < board_rows and 0 <= col < board_cols:
            return (row, col)
        return None
