"""플레이어 새 클래스"""

import pygame
from config import (
    BIRD_X, BIRD_Y, BIRD_WIDTH, BIRD_HEIGHT,
    BIRD_JUMP_STRENGTH, BIRD_GRAVITY, BIRD_TERMINAL_VELOCITY,
    YELLOW, BLACK, WHITE
)


class Bird:
    """플레이어 새를 관리하는 클래스"""

    def __init__(self):
        """새 초기화"""
        self.rect = pygame.Rect(BIRD_X, BIRD_Y, BIRD_WIDTH, BIRD_HEIGHT)
        self.velocity = 0
        self.angle = 0

    def jump(self):
        """새를 점프시킴"""
        self.velocity = BIRD_JUMP_STRENGTH

    def update(self):
        """새의 상태 업데이트 (중력 적용)"""
        # 중력 적용
        self.velocity += BIRD_GRAVITY

        # 최대 낙하 속도 제한
        if self.velocity > BIRD_TERMINAL_VELOCITY:
            self.velocity = BIRD_TERMINAL_VELOCITY

        # Y 위치 업데이트
        self.rect.y += int(self.velocity)

        # 각도 계산 (위로 올라갈 때는 위로, 내려갈 때는 아래로)
        if self.velocity < 0:
            self.angle = max(-25, self.velocity * 3)
        else:
            self.angle = min(90, self.velocity * 3 - 20)

    def draw(self, screen):
        """새를 화면에 그림"""
        # 간단한 노란색 사각형으로 새 표현
        pygame.draw.rect(screen, YELLOW, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # 테두리

        # 눈
        eye_x = self.rect.right - 10
        eye_y = self.rect.top + 5
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 6)
        pygame.draw.circle(screen, BLACK, (eye_x + 2, eye_y), 3)

        # 부리
        beak_points = [
            (self.rect.right - 2, self.rect.centery),
            (self.rect.right + 8, self.rect.centery + 3),
            (self.rect.right - 2, self.rect.centery + 6)
        ]
        pygame.draw.polygon(screen, (255, 165, 0), beak_points)

    def reset(self):
        """새를 초기 위치로 리셋"""
        self.rect.y = BIRD_Y
        self.velocity = 0
        self.angle = 0

    def get_mask(self):
        """충돌 감지를 위한 마스크 반환"""
        mask = pygame.Mask((BIRD_WIDTH, BIRD_HEIGHT))
        mask.fill()
        return mask
