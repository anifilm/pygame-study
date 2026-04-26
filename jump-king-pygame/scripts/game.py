"""Main game loop and state management."""

import sys
import time

import pygame

from camera import Camera
from level import Level
from player import Player
from settings import (
    BIG_FONT_SIZE,
    COLORS,
    FONT_NAME,
    FONT_SIZE,
    FPS,
    JUMP_CHARGE_TIME,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
)
from storage import SaveData


class Game:
    """Coordinates input, updates, rendering, and game state."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.big_font = pygame.font.Font(FONT_NAME, BIG_FONT_SIZE)
        self.small_font = pygame.font.Font(FONT_NAME, 22)

        self.level = Level()
        self.camera = Camera(self.level.width, self.level.height)
        self.player = Player(self.level.spawn)
        self.save_data = SaveData()

        self.state = "START"
        self.started_at = None
        self.elapsed = 0.0
        self.message = "Hold SPACE to charge, release to jump"
        self.reset_game()

    def reset_game(self) -> None:
        self.player.reset()
        self.camera.reset(self.player.rect)
        self.state = "START"
        self.started_at = None
        self.elapsed = 0.0

    def start_game(self) -> None:
        if self.state == "START":
            self.state = "PLAYING"
            self.started_at = time.monotonic()
        elif self.state == "PAUSED":
            self.state = "PLAYING"
            self.started_at = time.monotonic() - self.elapsed

    def run(self) -> None:
        running = True
        while running:
            dt = min(self.clock.tick(FPS) / 1000, 1 / 30)
            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "PLAYING":
                        self.state = "PAUSED"
                    else:
                        return False
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.start_game()
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_SPACE:
                    if self.state in ("START", "PAUSED"):
                        self.start_game()
                        self.player.start_charge()
                    elif self.state == "WON":
                        self.reset_game()
                    else:
                        self.player.start_charge()

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if self.state == "PLAYING":
                    self.player.release_charge(pygame.key.get_pressed())

        return True

    def update(self, dt: float) -> None:
        if self.state != "PLAYING":
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.player.start_charge()

        self.player.update(
            dt,
            keys,
            self.level.platforms,
            self.level.width,
            self.level.height,
        )
        self.camera.update(self.player.rect, dt)

        self.elapsed = time.monotonic() - self.started_at
        climbed = max(0, self.level.height - self.player.rect.bottom)
        self.save_data.update_height(climbed)

        if self.player.rect.colliderect(self.level.goal_rect):
            self.state = "WON"
            self.save_data.update_clear_time(self.elapsed)

    def draw(self) -> None:
        self._draw_background()
        self._draw_world(self.screen)
        self._draw_hud()

        if self.state == "START":
            self._draw_overlay(
                "Pygame Jump King",
                ["Press ENTER or SPACE to start", "Move: A/D or Arrow keys", self.message],
            )
        elif self.state == "PAUSED":
            self._draw_overlay("Paused", ["Press ENTER to continue", "Press R to restart"])
        elif self.state == "WON":
            self._draw_overlay(
                "You Reached The Crown!",
                [f"Time: {self.elapsed:.2f}s", "Press SPACE or R to restart"],
            )

        pygame.display.flip()

    def _draw_world(self, surface: pygame.Surface) -> None:
        self._draw_height_markers(surface)
        self.level.draw(surface, self.camera)
        self.player.draw(surface, self.camera)

    def _draw_background(self) -> None:
        top = COLORS["background_top"]
        bottom = COLORS["background_bottom"]
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            color = (
                round(top[0] + (bottom[0] - top[0]) * ratio),
                round(top[1] + (bottom[1] - top[1]) * ratio),
                round(top[2] + (bottom[2] - top[2]) * ratio),
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))

    def _draw_height_markers(self, surface: pygame.Surface) -> None:
        section_height = SCREEN_HEIGHT
        first = int(self.camera.offset.y // section_height) * section_height
        y = first
        while y < self.camera.offset.y + SCREEN_HEIGHT:
            screen_y = round(y - self.camera.offset.y)
            pygame.draw.line(surface, (255, 255, 255, 35), (0, screen_y), (SCREEN_WIDTH, screen_y))
            label = self.small_font.render(f"{self.level.height - y}m", True, COLORS["muted_text"])
            surface.blit(label, (12, screen_y + 8))
            y += section_height

    def _draw_hud(self) -> None:
        panel = pygame.Surface((SCREEN_WIDTH, 78), pygame.SRCALPHA)
        panel.fill(COLORS["panel_alpha"])
        self.screen.blit(panel, (0, 0))

        height = max(0, self.level.height - self.player.rect.bottom)
        best = self.save_data.best_height
        timer = self.elapsed if self.state != "START" else 0
        stats = f"Height {height}m   Best {best}m   Time {timer:.1f}s"
        text = self.small_font.render(stats, True, COLORS["text"])
        self.screen.blit(text, (20, 14))

        controls = "SPACE charge/jump   A/D move   R reset   ESC pause/quit"
        controls_text = self.small_font.render(controls, True, COLORS["muted_text"])
        self.screen.blit(controls_text, (20, 43))

        self._draw_charge_bar()

    def _draw_charge_bar(self) -> None:
        bar_width = 190
        bar_height = 18
        x = SCREEN_WIDTH - bar_width - 24
        y = 26
        rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(self.screen, COLORS["charge_bg"], rect, border_radius=8)

        fill_width = round(bar_width * self.player.charge_ratio)
        if fill_width > 0:
            fill = pygame.Rect(x, y, fill_width, bar_height)
            pygame.draw.rect(self.screen, COLORS["charge_fill"], fill, border_radius=8)

        label = self.small_font.render(f"Charge {self.player.charge / JUMP_CHARGE_TIME:.0%}", True, COLORS["text"])
        self.screen.blit(label, (x, y + 24))

    def _draw_overlay(self, title: str, lines: list[str]) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        title_surface = self.big_font.render(title, True, COLORS["text"])
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 95))
        self.screen.blit(title_surface, title_rect)

        for index, line in enumerate(lines):
            surface = self.font.render(line, True, COLORS["text"])
            rect = surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + index * 38))
            self.screen.blit(surface, rect)

        if self.save_data.best_time is not None:
            best = self.small_font.render(
                f"Best clear: {self.save_data.best_time:.2f}s",
                True,
                COLORS["muted_text"],
            )
            self.screen.blit(best, best.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130)))

