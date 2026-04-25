"""게임 메인 로직 모듈."""

import sys
from typing import Set, Tuple

import pygame

from constants import (
    BASE_SCORE,
    BIG_FONT_SIZE,
    COLOR_BG,
    COLOR_EXIT,
    COLOR_HUD_BG,
    COLOR_PATH,
    COLOR_PLAYER,
    COLOR_START,
    COLOR_TEXT,
    COLOR_TREASURE,
    COLOR_WALL,
    FONT_NAME,
    FONT_SIZE,
    FPS,
    MOVE_DELAY,
    MOVE_PENALTY,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
    TREASURE_SCORE,
)
from maze import generate_maze, get_exit_position, place_treasures
from player import Player


class Game:
    """미로 탈출 게임 메인 클래스."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.big_font = pygame.font.SysFont(FONT_NAME, BIG_FONT_SIZE)

        self.reset_game()

    def reset_game(self):
        """게임 상태를 초기화합니다."""
        self.maze = generate_maze()
        self.exit_pos = get_exit_position(self.maze)
        self.treasures: Set[Tuple[int, int]] = place_treasures(self.maze)
        self.player = Player(1, 1)
        self.collected = 0
        self.state = "playing"  # "playing" 또는 "won"
        self.move_timer = 0.0  # 연속 이동 타이머

    def calculate_score(self) -> int:
        """현재 점수를 계산합니다."""
        score = BASE_SCORE - (self.player.moves * MOVE_PENALTY)
        score += self.collected * TREASURE_SCORE
        return max(score, 0)

    def handle_events(self):
        """이벤트를 처리합니다."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.state == "won":
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def handle_continuous_movement(self, dt: float):
        """키를 누르고 있을 때 연속 이동을 처리합니다."""
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1
        elif keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1

        if dx == 0 and dy == 0:
            self.move_timer = 0.0
            return

        # 이동 중이 아니거나 타이머가 다 되면 이동
        if not self.player.is_moving or self.move_timer <= 0:
            moved = self.player.move(dx, dy, self.maze)
            if moved:
                self.check_treasure()
                self.check_win()
                self.move_timer = MOVE_DELAY
        else:
            self.move_timer -= dt

    def check_treasure(self):
        """보물 획득을 확인합니다."""
        pos = self.player.get_position()
        if pos in self.treasures:
            self.treasures.remove(pos)
            self.collected += 1

    def check_win(self):
        """탈출 조건을 확인합니다."""
        if self.player.get_position() == self.exit_pos:
            self.state = "won"

    def draw_maze(self):
        """미로를 그립니다."""
        maze_height = len(self.maze)
        maze_width = len(self.maze[0])

        # 미로 중앙 정렬을 위한 오프셋
        offset_x = (SCREEN_WIDTH - maze_width * TILE_SIZE) // 2
        offset_y = 80  # HUD 공간 확보

        for y in range(maze_height):
            for x in range(maze_width):
                rect = pygame.Rect(
                    offset_x + x * TILE_SIZE,
                    offset_y + y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE,
                )
                if self.maze[y][x] == 1:
                    pygame.draw.rect(self.screen, COLOR_WALL, rect)
                else:
                    pygame.draw.rect(self.screen, COLOR_PATH, rect)

                # 시작점 표시
                if (x, y) == (1, 1):
                    pygame.draw.rect(self.screen, COLOR_START, rect)
                # 탈출 지점 표시
                elif (x, y) == self.exit_pos:
                    pygame.draw.rect(self.screen, COLOR_EXIT, rect)

        # 보물 그리기
        for tx, ty in self.treasures:
            center = (
                offset_x + tx * TILE_SIZE + TILE_SIZE // 2,
                offset_y + ty * TILE_SIZE + TILE_SIZE // 2,
            )
            radius = TILE_SIZE // 3
            pygame.draw.circle(self.screen, COLOR_TREASURE, center, radius)

        # 플레이어 그리기 (픽셀 위치 기반 부드러운 이동)
        px, py = self.player.get_pixel_position()
        player_rect = pygame.Rect(
            offset_x + px + 4,
            offset_y + py + 4,
            TILE_SIZE - 8,
            TILE_SIZE - 8,
        )
        pygame.draw.rect(self.screen, COLOR_PLAYER, player_rect, border_radius=4)

    def draw_hud(self):
        """상단 HUD를 그립니다."""
        hud_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 70)
        pygame.draw.rect(self.screen, COLOR_HUD_BG, hud_rect)

        score = self.calculate_score()
        texts = [
            f"이동: {self.player.moves}",
            f"보물: {self.collected}/{self.collected + len(self.treasures)}",
            f"점수: {score}",
        ]

        x_offset = 20
        for text in texts:
            surface = self.font.render(text, True, COLOR_TEXT)
            self.screen.blit(surface, (x_offset, 20))
            x_offset += 200

    def draw_win_screen(self):
        """승리 화면을 그립니다."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        final_score = self.calculate_score()
        lines = [
            "탈출 성공!",
            f"최종 점수: {final_score}",
            f"이동 횟수: {self.player.moves}",
            f"획득 보물: {self.collected}",
            "",
            "R - 재시작",
            "Q - 종료",
        ]

        y_offset = SCREEN_HEIGHT // 2 - len(lines) * 30
        for line in lines:
            surface = self.big_font.render(line, True, COLOR_TEXT)
            rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(surface, rect)
            y_offset += 50

    def update(self, dt: float):
        """화면을 업데이트합니다."""
        self.handle_continuous_movement(dt)
        self.player.update(dt, PLAYER_SPEED * TILE_SIZE)

        self.screen.fill(COLOR_BG)
        self.draw_maze()
        self.draw_hud()

        if self.state == "won":
            self.draw_win_screen()

        pygame.display.flip()

    def run(self):
        """메인 게임 루프."""
        while True:
            dt = self.clock.tick(FPS) / 1000.0  # 초 단위 delta time
            self.handle_events()
            self.update(dt)
