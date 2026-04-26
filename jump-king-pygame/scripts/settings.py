"""Shared settings for the Jump King inspired prototype."""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

TITLE = "Pygame Jump King"
FONT_NAME = None
FONT_SIZE = 28
BIG_FONT_SIZE = 64

PLAYER_WIDTH = 34
PLAYER_HEIGHT = 48
PLAYER_ACCEL = 2400
PLAYER_AIR_ACCEL = 650
PLAYER_MAX_SPEED = 260
PLAYER_FRICTION = 2100
GRAVITY = 1700
MAX_FALL_SPEED = 1250

JUMP_MIN_SPEED = 560
JUMP_MAX_SPEED = 980
JUMP_HORIZONTAL_SPEED = 420
JUMP_CHARGE_TIME = 1.05
WALL_BOUNCE = 0.35

CAMERA_DEADZONE_TOP = 190
CAMERA_DEADZONE_BOTTOM = 390
CAMERA_SMOOTHING = 9.0

SAVE_FILE = "data/save_data.json"
LEVEL_FILE = "data/level_01.json"

COLORS = {
    "background_top": (29, 35, 57),
    "background_bottom": (88, 72, 94),
    "platform": (91, 67, 53),
    "platform_top": (150, 112, 75),
    "player": (239, 201, 130),
    "player_shadow": (86, 55, 45),
    "goal": (242, 220, 120),
    "text": (245, 241, 222),
    "muted_text": (185, 181, 171),
    "panel": (18, 22, 34),
    "panel_alpha": (18, 22, 34, 180),
    "charge_bg": (43, 48, 64),
    "charge_fill": (238, 149, 79),
    "danger": (220, 85, 70),
}
