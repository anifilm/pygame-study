"""Camera behavior for the vertical level."""

import pygame

from settings import (
    CAMERA_DEADZONE_BOTTOM,
    CAMERA_DEADZONE_TOP,
    CAMERA_SMOOTHING,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Camera:
    """Tracks the player through a tall level with a small dead zone."""

    def __init__(self, level_width: int, level_height: int):
        self.level_width = level_width
        self.level_height = level_height
        self.offset = pygame.Vector2(0, max(0, level_height - SCREEN_HEIGHT))

    def reset(self, target_rect: pygame.Rect) -> None:
        self.offset.y = self._target_y(target_rect)

    def update(self, target_rect: pygame.Rect, dt: float) -> None:
        target_y = self._target_y(target_rect)
        blend = min(1.0, CAMERA_SMOOTHING * dt)
        self.offset.y += (target_y - self.offset.y) * blend
        self.offset.x = 0

    def _target_y(self, target_rect: pygame.Rect) -> float:
        top_line = self.offset.y + CAMERA_DEADZONE_TOP
        bottom_line = self.offset.y + CAMERA_DEADZONE_BOTTOM
        target_y = self.offset.y

        if target_rect.top < top_line:
            target_y = target_rect.top - CAMERA_DEADZONE_TOP
        elif target_rect.bottom > bottom_line:
            target_y = target_rect.bottom - CAMERA_DEADZONE_BOTTOM

        return max(0, min(target_y, self.level_height - SCREEN_HEIGHT))

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(-round(self.offset.x), -round(self.offset.y))

    @property
    def viewport(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.offset.x),
            round(self.offset.y),
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
        )
