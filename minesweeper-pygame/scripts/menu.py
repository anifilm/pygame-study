import pygame
import math
from settings import *

# 초급 게임 창 크기와 동일하게 맞춤
_cfg        = DIFFICULTIES['beginner']
MENU_WIDTH  = _cfg['cols'] * CELL_SIZE + BOARD_PADDING * 2
MENU_HEIGHT = HEADER_HEIGHT + _cfg['rows'] * CELL_SIZE + BOARD_PADDING * 2

DIFFICULTY_ITEMS = [
    {'key': 'beginner',     'label': 'Beginner',     'detail': '9 x 9   |   10 mines'},
    {'key': 'intermediate', 'label': 'Intermediate', 'detail': '16 x 16  |  40 mines'},
    {'key': 'expert',       'label': 'Expert',       'detail': '30 x 16  |  99 mines'},
]

DIFF_ACCENTS = {
    'beginner':     ( 74, 222, 128),
    'intermediate': ( 96, 165, 250),
    'expert':       (248, 113, 113),
}

BTN_WIDTH  = 246
BTN_HEIGHT = 55
BTN_GAP    = 10

TOGGLE_W = 96
TOGGLE_H = 26


class Menu:
    def __init__(self, surface, theme, theme_name):
        self.surface     = surface
        self.T           = theme
        self.theme_name  = theme_name
        self.title_font  = pygame.font.SysFont('arial', 26, bold=True)
        self.label_font  = pygame.font.SysFont('arial', 20, bold=True)
        self.detail_font = pygame.font.SysFont('arial', 14)
        self.toggle_font = pygame.font.SysFont('arial', 14, bold=True)
        self.hint_font   = pygame.font.SysFont('arial', 12)
        self.hovered     = None   # difficulty key or 'classic'/'dark'
        self._build_rects()

    def _build_rects(self):
        cx = MENU_WIDTH // 2

        # 테마 토글 버튼 (제목 아래)
        self.toggle_classic = pygame.Rect(cx - TOGGLE_W - 4, 82, TOGGLE_W, TOGGLE_H)
        self.toggle_dark    = pygame.Rect(cx + 4,             82, TOGGLE_W, TOGGLE_H)

        # 난이도 버튼 — 구분선(y=118) 아래 공간에서 수직 중앙 정렬
        SEPARATOR_Y = 120
        HINT_AREA   = 30
        total_btn_h = len(DIFFICULTY_ITEMS) * BTN_HEIGHT + (len(DIFFICULTY_ITEMS) - 1) * BTN_GAP
        available   = MENU_HEIGHT - SEPARATOR_Y - HINT_AREA
        start_y     = SEPARATOR_Y + (available - total_btn_h) // 2
        self.diff_rects = {}
        for i, item in enumerate(DIFFICULTY_ITEMS):
            x = (MENU_WIDTH - BTN_WIDTH) // 2
            y = start_y + i * (BTN_HEIGHT + BTN_GAP)
            self.diff_rects[item['key']] = pygame.Rect(x, y, BTN_WIDTH, BTN_HEIGHT)

    # ------------------------------------------------------------------ #
    #  이벤트                                                               #
    # ------------------------------------------------------------------ #

    def handle_event(self, event):
        """
        반환값:
          {'action': 'start',  'difficulty': key}
          {'action': 'theme',  'theme': name}
          None
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = None
            for key, rect in self.diff_rects.items():
                if rect.collidepoint(event.pos):
                    self.hovered = key
                    break
            if self.toggle_classic.collidepoint(event.pos):
                self.hovered = 'classic'
            elif self.toggle_dark.collidepoint(event.pos):
                self.hovered = 'dark'

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.toggle_classic.collidepoint(pos):
                return {'action': 'theme', 'theme': 'classic'}
            if self.toggle_dark.collidepoint(pos):
                return {'action': 'theme', 'theme': 'dark'}
            for key, rect in self.diff_rects.items():
                if rect.collidepoint(pos):
                    return {'action': 'start', 'difficulty': key}

        return None

    # ------------------------------------------------------------------ #
    #  그리기                                                               #
    # ------------------------------------------------------------------ #

    def draw(self):
        self.surface.fill(self.T['MENU_BG'])
        self._draw_title()
        self._draw_theme_toggle()
        self._draw_separator(118)
        for item in DIFFICULTY_ITEMS:
            key  = item['key']
            rect = self.diff_rects[key]
            self._draw_diff_button(rect, item['label'], item['detail'],
                                   DIFF_ACCENTS[key], hovered=(self.hovered == key))
        self._draw_hint()
        pygame.display.update()

    def _draw_title(self):
        surf = self.title_font.render('MINESWEEPER', True, self.T['MENU_TITLE'])
        self.surface.blit(surf, surf.get_rect(centerx=MENU_WIDTH // 2, top=20))

        if self.T['name'] == 'dark':
            # 그라디언트 라인
            line_y  = 58
            line_x1 = (MENU_WIDTH - 160) // 2
            for i in range(160):
                t = i / 160
                r = int(74  + (96  - 74)  * t)
                g = int(222 + (165 - 222) * t)
                b = int(128 + (250 - 128) * t)
                alpha = int(220 * math.sin(t * math.pi))
                color = (min(255, r), min(255, g), min(255, b))
                pygame.draw.line(self.surface, color,
                                 (line_x1 + i, line_y), (line_x1 + i, line_y + 1))
        else:
            line_y = 58
            pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                             (20, line_y), (MENU_WIDTH - 20, line_y))
            pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                             (20, line_y + 1), (MENU_WIDTH - 20, line_y + 1))

    def _draw_theme_toggle(self):
        label_surf = self.hint_font.render('Theme', True, self.T['MENU_DETAIL'])
        self.surface.blit(label_surf,
                          label_surf.get_rect(centerx=MENU_WIDTH // 2, top=66))

        for name, rect in [('classic', self.toggle_classic), ('dark', self.toggle_dark)]:
            active  = (self.theme_name == name)
            hovered = (self.hovered == name)
            self._draw_toggle_btn(rect, name.capitalize(), active, hovered)

    def _draw_toggle_btn(self, rect, label, active, hovered):
        if self.T['name'] == 'classic':
            if active:
                # 선택된 것은 sunken
                pygame.draw.rect(self.surface, self.T['COLOR_CELL_HIDDEN'], rect)
                x, y, w, h = rect
                b = 2
                for i in range(b):
                    pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                                     (x+i, y+i), (x+w-i-1, y+i))
                    pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                                     (x+i, y+i), (x+i, y+h-i-1))
                    pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                                     (x+w-i-1, y+i+1), (x+w-i-1, y+h-i-1))
                    pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                                     (x+i+1, y+h-i-1), (x+w-i-1, y+h-i-1))
                text_color = self.T['MENU_ACCENT']
            else:
                pygame.draw.rect(self.surface, self.T['COLOR_CELL_HIDDEN'], rect)
                x, y, w, h = rect
                b = 2
                for i in range(b):
                    pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                                     (x+i, y+i), (x+w-i-1, y+i))
                    pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                                     (x+i, y+i), (x+i, y+h-i-1))
                    pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                                     (x+w-i-1, y+i+1), (x+w-i-1, y+h-i-1))
                    pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                                     (x+i+1, y+h-i-1), (x+w-i-1, y+h-i-1))
                text_color = self.T['MENU_DETAIL'] if not hovered else self.T['MENU_LABEL']
        else:
            # Dark 테마 토글
            accent = self.T['MENU_ACCENT']
            if active:
                bg         = tuple(int(c * 0.3) for c in accent)
                border_col = accent
                text_color = accent
            elif hovered:
                bg         = (38, 38, 66)
                border_col = (60, 60, 100)
                text_color = self.T['MENU_LABEL']
            else:
                bg         = (24, 24, 42)
                border_col = (38, 38, 66)
                text_color = self.T['MENU_DETAIL']
            pygame.draw.rect(self.surface, bg, rect, border_radius=5)
            pygame.draw.rect(self.surface, border_col, rect, width=1, border_radius=5)

        surf = self.toggle_font.render(label, True, text_color)
        self.surface.blit(surf, surf.get_rect(center=rect.center))

    def _draw_separator(self, y):
        if self.T['name'] == 'classic':
            pygame.draw.line(self.surface, self.T['COLOR_CELL_SHADOW'],
                             (20, y), (MENU_WIDTH - 20, y))
            pygame.draw.line(self.surface, self.T['COLOR_CELL_LIGHT'],
                             (20, y + 1), (MENU_WIDTH - 20, y + 1))
        else:
            pygame.draw.line(self.surface, (38, 38, 66),
                             (20, y), (MENU_WIDTH - 20, y))

    def _draw_diff_button(self, rect, label, detail, accent, hovered):
        if self.T['name'] == 'classic':
            # 클래식: raised bevel 버튼
            bg = self.T['MENU_CARD_HOVER'] if hovered else self.T['MENU_CARD_BG']
            pygame.draw.rect(self.surface, bg, rect)
            x, y, w, h = rect
            b = 2
            lc = self.T['COLOR_CELL_SHADOW'] if hovered else self.T['COLOR_CELL_LIGHT']
            sc = self.T['COLOR_CELL_LIGHT']  if hovered else self.T['COLOR_CELL_SHADOW']
            for i in range(b):
                pygame.draw.line(self.surface, lc, (x+i, y+i), (x+w-i-1, y+i))
                pygame.draw.line(self.surface, lc, (x+i, y+i), (x+i, y+h-i-1))
                pygame.draw.line(self.surface, sc, (x+w-i-1, y+i+1), (x+w-i-1, y+h-i-1))
                pygame.draw.line(self.surface, sc, (x+i+1, y+h-i-1), (x+w-i-1, y+h-i-1))

            # 왼쪽 컬러 바
            bar = pygame.Rect(rect.left + 6, rect.top + 8, 4, rect.height - 16)
            pygame.draw.rect(self.surface, accent, bar)

            label_surf  = self.label_font.render(label,  True, self.T['MENU_LABEL'])
            detail_surf = self.detail_font.render(detail, True, self.T['MENU_DETAIL'])
        else:
            # 다크: 카드 버튼
            bg = self.T['MENU_CARD_HOVER'] if hovered else self.T['MENU_CARD_BG']
            pygame.draw.rect(self.surface, bg, rect, border_radius=8)
            if hovered:
                border_col = tuple(int(c * 0.55) for c in accent)
                pygame.draw.rect(self.surface, border_col, rect, width=1, border_radius=8)

            # 왼쪽 컬러 바
            bar = pygame.Rect(rect.left, rect.top + 8, 4, rect.height - 16)
            pygame.draw.rect(self.surface, accent, bar, border_radius=2)

            label_surf  = self.label_font.render(label,  True, self.T['MENU_LABEL'])
            detail_surf = self.detail_font.render(detail, True, self.T['MENU_DETAIL'])

            # 화살표
            if hovered:
                ax, ay = rect.right - 16, rect.centery
                pygame.draw.polygon(self.surface, accent,
                                    [(ax-4, ay-5), (ax+2, ay), (ax-4, ay+5)])

        lx = rect.left + 18
        self.surface.blit(label_surf,
                          label_surf.get_rect(left=lx, centery=rect.centery - 10))
        self.surface.blit(detail_surf,
                          detail_surf.get_rect(left=lx, centery=rect.centery + 12))

    def _draw_hint(self):
        text = 'R: restart   ESC: menu   1/2/3: difficulty'
        surf = self.hint_font.render(text, True, self.T['MENU_HINT'])
        self.surface.blit(surf,
                          surf.get_rect(centerx=MENU_WIDTH // 2, bottom=MENU_HEIGHT - 10))
