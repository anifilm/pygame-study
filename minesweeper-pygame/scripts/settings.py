import pygame

# --- 난이도 설정 ---
DIFFICULTIES = {
    'beginner':     {'cols': 9,  'rows': 9,  'mines': 10},
    'intermediate': {'cols': 16, 'rows': 16, 'mines': 40},
    'expert':       {'cols': 30, 'rows': 16, 'mines': 99},
}
DEFAULT_DIFFICULTY = 'beginner'

# --- 레이아웃 고정값 (테마와 무관) ---
CELL_SIZE      = 36
BOARD_PADDING  = 10   # 보드 사방 여백
HEADER_HEIGHT  = 72
HEADER_PADDING = 12
SMILEY_SIZE    = 36
LCD_WIDTH      = 52
LCD_HEIGHT     = 28

# --- 셀 상태 ---
STATE_HIDDEN     = 'hidden'
STATE_REVEALED   = 'revealed'
STATE_FLAGGED    = 'flagged'
STATE_QUESTION   = 'question'
STATE_EXPLODED   = 'exploded'
STATE_MINE_SHOW  = 'mine_shown'
STATE_WRONG_FLAG = 'wrong_flag'

# --- 게임 상태 ---
GAME_WAITING = 'waiting'
GAME_ACTIVE  = 'active'
GAME_WON     = 'won'
GAME_LOST    = 'lost'
