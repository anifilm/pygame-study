"""미로 생성 및 보물 배치 모듈."""

import random
from typing import List, Tuple, Set

from constants import MAZE_WIDTH, MAZE_HEIGHT, TREASURE_COUNT


def generate_maze(width: int = MAZE_WIDTH, height: int = MAZE_HEIGHT) -> List[List[int]]:
    """DFS 백트래킹으로 미로를 생성합니다.

    0: 통로, 1: 벽
    """
    # 홀수 크기 보장
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    # 전체를 벽으로 초기화
    maze = [[1 for _ in range(width)] for _ in range(height)]

    # 시작점 (1, 1)에서 DFS 시작
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0

    stack = [(start_x, start_y)]
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]  # 상, 하, 좌, 우 (2칸씩)

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        found = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == 1:
                # 벽을 허물고 중간 지점도 통로로 만듦
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0
                stack.append((nx, ny))
                found = True
                break

        if not found:
            stack.pop()

    return maze


def place_treasures(
    maze: List[List[int]],
    count: int = TREASURE_COUNT,
) -> Set[Tuple[int, int]]:
    """미로 내 통로에 보물을 랜덤 배치합니다.

    시작점(1,1)과 탈출 지점(width-2, height-2)은 제외합니다.
    """
    height = len(maze)
    width = len(maze[0])

    # 모든 통로 위치 수집
    paths = []
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 0:
                # 시작점과 탈출 지점 제외
                if (x, y) != (1, 1) and (x, y) != (width - 2, height - 2):
                    paths.append((x, y))

    # 보물 개수 조정
    count = min(count, len(paths))
    return set(random.sample(paths, count))


def get_exit_position(maze: List[List[int]]) -> Tuple[int, int]:
    """탈출 지점 좌표를 반환합니다."""
    return (len(maze[0]) - 2, len(maze) - 2)
