"""파이프 장애물 클래스"""

import pygame
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PIPE_WIDTH, PIPE_GAP, PIPE_SPEED,
    PIPE_GREEN, BLACK
)


class Pipe:
    """파이프 장애물을 관리하는 클래스"""

    def __init__(self, x=None):
        """
        파이프 초기화

        Args:
            x: 파이프의 X 좌표 (기본값: 화면 오른쪽 밖)
        """
        if x is None:
            x = SCREEN_WIDTH

        self.x = x
        self.passed = False  # 새가 파이프를 통과했는지 여부

        # 파이프 높이 랜덤 설정 (너무 높거나 낮지 않게 제한)
        min_pipe_height = 100
        max_pipe_height = SCREEN_HEIGHT - PIPE_GAP - min_pipe_height
        self.top_height = random.randint(min_pipe_height, max_pipe_height)

        # 위 파이프와 아래 파이프의 Rect 생성
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_height)
        self.bottom_rect = pygame.Rect(
            self.x, self.top_height + PIPE_GAP,
            PIPE_WIDTH, SCREEN_HEIGHT - self.top_height - PIPE_GAP
        )

    def update(self):
        """파이프를 왼쪽으로 이동"""
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        """파이프를 화면에 그림"""
        # 위 파이프
        pygame.draw.rect(screen, PIPE_GREEN, self.top_rect)
        pygame.draw.rect(screen, BLACK, self.top_rect, 2)

        # 아래 파이프
        pygame.draw.rect(screen, PIPE_GREEN, self.bottom_rect)
        pygame.draw.rect(screen, BLACK, self.bottom_rect, 2)

        # 파이프 캡 (장식)
        cap_height = 20
        cap_y = self.top_height - cap_height
        top_cap = pygame.Rect(self.x - 5, cap_y, PIPE_WIDTH + 10, cap_height)
        pygame.draw.rect(screen, PIPE_GREEN, top_cap)
        pygame.draw.rect(screen, BLACK, top_cap, 2)

        bottom_cap_y = self.top_height + PIPE_GAP
        bottom_cap = pygame.Rect(self.x - 5, bottom_cap_y, PIPE_WIDTH + 10, cap_height)
        pygame.draw.rect(screen, PIPE_GREEN, bottom_cap)
        pygame.draw.rect(screen, BLACK, bottom_cap, 2)

    def is_off_screen(self):
        """파이프가 화면 밖으로 나갔는지 확인"""
        return self.x + PIPE_WIDTH < 0

    def check_collision(self, bird_rect):
        """
        새와 충돌했는지 확인

        Args:
            bird_rect: 새의 Rect 객체

        Returns:
            bool: 충돌 여부
        """
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)
