"""게임 상수 모듈."""

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
FPS = 60

# 미로 설정
MAZE_WIDTH = 21   # 홀수
MAZE_HEIGHT = 21  # 홀수
TILE_SIZE = 30

# 보물 설정
TREASURE_COUNT = 5
TREASURE_SCORE = 100

# 점수 설정
BASE_SCORE = 1000
MOVE_PENALTY = 10

# 색상 (R, G, B)
COLOR_WALL = (30, 30, 30)
COLOR_PATH = (240, 240, 240)
COLOR_START = (0, 200, 0)
COLOR_EXIT = (200, 0, 0)
COLOR_TREASURE = (255, 215, 0)
COLOR_PLAYER = (0, 100, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_BG = (20, 20, 20)
COLOR_HUD_BG = (40, 40, 40)

# 폰트 설정 (macOS 한글 폰트)
FONT_NAME = "AppleGothic"
FONT_SIZE = 24
BIG_FONT_SIZE = 48

# 이동 설정 (초당 타일 수)
PLAYER_SPEED = 8  # 초당 8칸 이동 (약 0.125초에 한 칸)
MOVE_DELAY = 0.12  # 키 누르고 있을 때 연속 이동 간격(초)
