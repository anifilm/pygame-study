"""게임 로직 관리 클래스"""

import pygame
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    SKY_BLUE, WHITE, BLACK, GROUND_BROWN,
    PIPE_SPAWN_INTERVAL
)
from bird import Bird
from pipe import Pipe


class Game:
    """게임 상태를 관리하는 클래스"""

    def __init__(self):
        """게임 초기화"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)

        # 게임 상태
        self.state = "START"  # START, PLAYING, GAME_OVER
        self.score = 0
        self.high_score = 0

        # 게임 객체
        self.bird = Bird()
        self.pipes = []
        self.last_pipe_time = pygame.time.get_ticks()

        # 바닥
        self.ground_y = SCREEN_HEIGHT - 50

    def reset(self):
        """게임을 초기 상태로 리셋"""
        self.bird.reset()
        self.pipes = []
        self.score = 0
        self.last_pipe_time = pygame.time.get_ticks()
        self.state = "START"

    def spawn_pipe(self):
        """새 파이프 생성"""
        self.pipes.append(Pipe())

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == "START":
                        self.state = "PLAYING"
                        self.bird.jump()
                    elif self.state == "PLAYING":
                        self.bird.jump()
                    elif self.state == "GAME_OVER":
                        self.reset()

                if event.key == pygame.K_ESCAPE:
                    return False

        return True

    def update(self):
        """게임 상태 업데이트"""
        if self.state == "PLAYING":
            # 새 업데이트
            self.bird.update()

            # 파이프 생성
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe_time > PIPE_SPAWN_INTERVAL:
                self.spawn_pipe()
                self.last_pipe_time = current_time

            # 파이프 업데이트
            for pipe in self.pipes[:]:
                pipe.update()

                # 파이프 제거
                if pipe.is_off_screen():
                    self.pipes.remove(pipe)

                # 점수 확인 (파이프 통과)
                if not pipe.passed and pipe.x + 60 < self.bird.rect.left:
                    pipe.passed = True
                    self.score += 1

                # 충돌 확인
                if pipe.check_collision(self.bird.rect):
                    self.state = "GAME_OVER"
                    if self.score > self.high_score:
                        self.high_score = self.score

            # 바닥/천장 충돌 확인
            if self.bird.rect.top <= 0 or self.bird.rect.bottom >= self.ground_y:
                self.state = "GAME_OVER"
                if self.score > self.high_score:
                    self.high_score = self.score

    def draw(self):
        """화면 그리기"""
        # 배경
        self.screen.fill(SKY_BLUE)

        # 파이프 그리기
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # 바닥 그리기
        ground_rect = pygame.Rect(0, self.ground_y, SCREEN_WIDTH, 50)
        pygame.draw.rect(self.screen, GROUND_BROWN, ground_rect)
        pygame.draw.line(self.screen, BLACK, (0, self.ground_y), (SCREEN_WIDTH, self.ground_y), 2)

        # 새 그리기
        self.bird.draw(self.screen)

        # 점수 표시
        score_text = self.font.render(str(self.score), True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        pygame.draw.rect(self.screen, BLACK, score_rect.inflate(20, 10))
        self.screen.blit(score_text, score_rect)

        # 상태별 메시지
        if self.state == "START":
            self._draw_start_screen()
        elif self.state == "GAME_OVER":
            self._draw_game_over_screen()

        pygame.display.flip()

    def _draw_start_screen(self):
        """시작 화면 그리기"""
        # 반투명 오버레이
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("Flappy Bird", True, WHITE)
        start_msg = self.small_font.render("Press SPACE to Start", True, WHITE)
        instruct = self.small_font.render("Press ESC to Quit", True, WHITE)

        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
        self.screen.blit(start_msg, start_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))
        self.screen.blit(instruct, instruct.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))

    def _draw_game_over_screen(self):
        """게임 오버 화면 그리기"""
        # 반투명 오버레이
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        game_over = self.font.render("Game Over", True, WHITE)
        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        high_score_text = self.small_font.render(f"Best: {self.high_score}", True, WHITE)
        restart_msg = self.small_font.render("Press SPACE to Restart", True, WHITE)

        self.screen.blit(game_over, game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
        self.screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        self.screen.blit(high_score_text, high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))
        self.screen.blit(restart_msg, restart_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)))

    def run(self):
        """게임 루프 실행"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
