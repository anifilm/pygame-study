CLASSIC = {
    'name': 'classic',

    # 레이아웃 오버라이드
    'CELL_INSET':   0,
    'CELL_RADIUS':  0,
    'BORDER_WIDTH': 3,

    # 색상
    'COLOR_BG':            (192, 192, 192),
    'COLOR_HEADER_BG':     (192, 192, 192),
    'COLOR_HEADER_BORDER': (128, 128, 128),
    'COLOR_CELL_HIDDEN':   (192, 192, 192),
    'COLOR_CELL_LIGHT':    (255, 255, 255),
    'COLOR_CELL_SHADOW':   (128, 128, 128),
    'COLOR_CELL_REVEALED': (192, 192, 192),
    'COLOR_EXPLODED_BG':   (255,   0,   0),
    'LCD_COLOR_ON':        (255,   0,   0),
    'LCD_BG_COLOR':        (  0,   0,   0),
    'NUMBER_COLORS': {
        1: (  0,   0, 255),
        2: (  0, 128,   0),
        3: (255,   0,   0),
        4: (  0,   0, 128),
        5: (128,   0,   0),
        6: (  0, 128, 128),
        7: (  0,   0,   0),
        8: (128, 128, 128),
    },
    'MINE_COLOR': (  0,   0,   0),
    'FLAG_COLOR': (255,   0,   0),
    'FLAG_POLE':  (  0,   0,   0),
    'X_COLOR':    (255,   0,   0),

    # 메뉴
    'MENU_BG':         (192, 192, 192),
    'MENU_CARD_BG':    (202, 202, 202),
    'MENU_CARD_HOVER': (212, 212, 212),
    'MENU_TITLE':      (  0,   0,   0),
    'MENU_LABEL':      (  0,   0,   0),
    'MENU_DETAIL':     ( 55,  55,  55),
    'MENU_HINT':       ( 70,  70,  70),
    'MENU_ACCENT':     (  0,   0, 128),
}

DARK = {
    'name': 'dark',

    # 레이아웃 오버라이드
    'CELL_INSET':   1,
    'CELL_RADIUS':  0,
    'BORDER_WIDTH': 3,

    # 색상
    'COLOR_BG':            ( 15,  15,  26),
    'COLOR_HEADER_BG':     ( 24,  24,  42),
    'COLOR_HEADER_BORDER': ( 38,  38,  66),
    'COLOR_CELL_HIDDEN':   ( 50,  50,  88),
    'COLOR_CELL_LIGHT':    ( 70,  70, 115),
    'COLOR_CELL_SHADOW':   ( 28,  28,  52),
    'COLOR_CELL_REVEALED': ( 38,  38,  58),
    'COLOR_EXPLODED_BG':   ( 90,  20,  20),
    'LCD_COLOR_ON':        ( 74, 222, 128),
    'LCD_BG_COLOR':        (  8,   8,  18),
    'NUMBER_COLORS': {
        1: ( 96, 165, 250),
        2: ( 74, 222, 128),
        3: (248, 113, 113),
        4: (167, 139, 250),
        5: (251, 146,  60),
        6: ( 34, 211, 238),
        7: (226, 232, 240),
        8: (148, 163, 184),
    },
    'MINE_COLOR': (220, 220, 220),
    'FLAG_COLOR': (248, 113, 113),
    'FLAG_POLE':  (200, 200, 200),
    'X_COLOR':    (248, 113, 113),

    # 메뉴
    'MENU_BG':         ( 15,  15,  26),
    'MENU_CARD_BG':    ( 28,  28,  48),
    'MENU_CARD_HOVER': ( 38,  38,  62),
    'MENU_TITLE':      (230, 230, 245),
    'MENU_LABEL':      (225, 225, 240),
    'MENU_DETAIL':     (160, 160, 195),
    'MENU_HINT':       (120, 120, 155),
    'MENU_ACCENT':     ( 74, 222, 128),
}

THEMES = {'classic': CLASSIC, 'dark': DARK}
DEFAULT_THEME = 'dark'
