"""플레이어 모듈."""

from typing import List, Tuple

from constants import TILE_SIZE


class Player:
    """플레이어 캐릭터 (픽셀 단위 부드러운 이동)."""

    def __init__(self, x: int, y: int):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = float(x * TILE_SIZE)
        self.pixel_y = float(y * TILE_SIZE)
        self.moves = 0
        self.target_pixel_x = self.pixel_x
        self.target_pixel_y = self.pixel_y
        self.is_moving = False

    def move(self, dx: int, dy: int, maze: List[List[int]]) -> bool:
        """방향(dx, dy)으로 이동을 시도합니다.

        벽이면 이동하지 않고 False를 반환합니다.
        """
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        # 범위 및 벽 체크
        if (
            0 <= new_x < len(maze[0])
            and 0 <= new_y < len(maze)
            and maze[new_y][new_x] == 0
        ):
            self.grid_x = new_x
            self.grid_y = new_y
            self.target_pixel_x = float(new_x * TILE_SIZE)
            self.target_pixel_y = float(new_y * TILE_SIZE)
            self.is_moving = True
            self.moves += 1
            return True
        return False

    def update(self, dt: float, speed: float):
        """픽셀 위치를 목표 위치로 부드럽게 이동시킵니다."""
        if not self.is_moving:
            return

        # 선형 보간으로 부드럽게 이동
        step = speed * dt
        dx = self.target_pixel_x - self.pixel_x
        dy = self.target_pixel_y - self.pixel_y

        if abs(dx) <= step and abs(dy) <= step:
            self.pixel_x = self.target_pixel_x
            self.pixel_y = self.target_pixel_y
            self.is_moving = False
        else:
            if abs(dx) > 0:
                self.pixel_x += step if dx > 0 else -step
            if abs(dy) > 0:
                self.pixel_y += step if dy > 0 else -step

    def get_position(self) -> Tuple[int, int]:
        """현재 그리드 좌표를 반환합니다."""
        return (self.grid_x, self.grid_y)

    def get_pixel_position(self) -> Tuple[int, int]:
        """화면 픽셀 좌표를 반환합니다."""
        return (int(self.pixel_x), int(self.pixel_y))
