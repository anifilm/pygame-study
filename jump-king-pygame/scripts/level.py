"""Level loading and drawing."""

import json
from pathlib import Path

import pygame

from settings import COLORS, LEVEL_FILE


class Level:
    """A vertical set of platforms loaded from JSON data."""

    def __init__(self, path: str = LEVEL_FILE):
        base_dir = Path(__file__).resolve().parent.parent
        level_path = base_dir / path

        with level_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self.name = data["name"]
        self.width = data["width"]
        self.height = data["height"]
        self.spawn = pygame.Vector2(data["spawn"])
        self.goal_rect = pygame.Rect(data["goal"])
        self.platforms = [
            pygame.Rect(platform)
            for platform in data["platforms"]
        ]

    def draw(self, surface: pygame.Surface, camera) -> None:
        """Draw the visible level geometry."""
        for platform in self.platforms:
            screen_rect = camera.apply(platform)
            if (
                screen_rect.bottom < 0
                or screen_rect.top > surface.get_height()
            ):
                continue

            pygame.draw.rect(
                surface,
                COLORS["platform"],
                screen_rect,
                border_radius=4,
            )
            top_rect = screen_rect.copy()
            top_rect.height = min(6, screen_rect.height)
            pygame.draw.rect(
                surface,
                COLORS["platform_top"],
                top_rect,
                border_radius=4,
            )

        goal = camera.apply(self.goal_rect)
        pygame.draw.rect(surface, COLORS["goal"], goal, border_radius=8)
        pygame.draw.circle(surface, COLORS["goal"], goal.center, 26, width=3)
