"""Player movement and charge-jump physics."""

import pygame

from settings import (
    COLORS,
    GRAVITY,
    JUMP_CHARGE_TIME,
    JUMP_HORIZONTAL_SPEED,
    JUMP_MAX_SPEED,
    JUMP_MIN_SPEED,
    MAX_FALL_SPEED,
    PLAYER_ACCEL,
    PLAYER_AIR_ACCEL,
    PLAYER_FRICTION,
    PLAYER_HEIGHT,
    PLAYER_MAX_SPEED,
    PLAYER_WIDTH,
    WALL_BOUNCE,
)


class Player:
    """A simple physics body tuned around charged jumps."""

    def __init__(self, spawn: pygame.Vector2):
        self.spawn = pygame.Vector2(spawn)
        self.pos = pygame.Vector2(spawn)
        self.vel = pygame.Vector2(0, 0)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.grounded = False
        self.charging = False
        self.charge = 0.0
        self.last_landed = False

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.pos.x),
            round(self.pos.y),
            self.width,
            self.height,
        )

    @property
    def charge_ratio(self) -> float:
        return min(1.0, self.charge / JUMP_CHARGE_TIME)

    def reset(self) -> None:
        self.pos = pygame.Vector2(self.spawn)
        self.vel.update(0, 0)
        self.grounded = False
        self.charging = False
        self.charge = 0.0
        self.last_landed = False

    def start_charge(self) -> None:
        if self.grounded and not self.charging:
            self.charging = True
            self.charge = 0.0
            self.vel.x = 0

    def release_charge(self, keys) -> None:
        if not self.charging:
            return

        direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction += 1

        ratio = self.charge_ratio
        jump_speed = JUMP_MIN_SPEED + (JUMP_MAX_SPEED - JUMP_MIN_SPEED) * ratio
        horizontal_speed = JUMP_HORIZONTAL_SPEED * (0.45 + 0.55 * ratio)

        self.vel.y = -jump_speed
        self.vel.x = horizontal_speed * direction
        self.grounded = False
        self.charging = False
        self.charge = 0.0

    def update(
        self,
        dt: float,
        keys,
        platforms,
        level_width: int,
        level_height: int,
    ) -> None:
        was_grounded = self.grounded
        self.last_landed = False

        if self.charging:
            self.charge = min(JUMP_CHARGE_TIME, self.charge + dt)
            self._apply_friction(dt)
        else:
            self._apply_horizontal_input(dt, keys)

        self.vel.y = min(MAX_FALL_SPEED, self.vel.y + GRAVITY * dt)

        self._move_x(dt, platforms, level_width)
        self._move_y(dt, platforms, level_height)

        self.last_landed = not was_grounded and self.grounded

    def _apply_horizontal_input(self, dt: float, keys) -> None:
        direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction += 1

        if direction:
            accel = PLAYER_ACCEL if self.grounded else PLAYER_AIR_ACCEL
            self.vel.x += direction * accel * dt
            self.vel.x = max(
                -PLAYER_MAX_SPEED,
                min(PLAYER_MAX_SPEED, self.vel.x),
            )
        elif self.grounded:
            self._apply_friction(dt)

    def _apply_friction(self, dt: float) -> None:
        if self.vel.x > 0:
            self.vel.x = max(0, self.vel.x - PLAYER_FRICTION * dt)
        elif self.vel.x < 0:
            self.vel.x = min(0, self.vel.x + PLAYER_FRICTION * dt)

    def _move_x(self, dt: float, platforms, level_width: int) -> None:
        self.pos.x += self.vel.x * dt
        rect = self.rect

        if rect.left < 0:
            rect.left = 0
            self.vel.x = abs(self.vel.x) * WALL_BOUNCE
        elif rect.right > level_width:
            rect.right = level_width
            self.vel.x = -abs(self.vel.x) * WALL_BOUNCE

        for platform in platforms:
            if not rect.colliderect(platform):
                continue
            if self.vel.x > 0:
                rect.right = platform.left
                self.vel.x = -abs(self.vel.x) * WALL_BOUNCE
            elif self.vel.x < 0:
                rect.left = platform.right
                self.vel.x = abs(self.vel.x) * WALL_BOUNCE

        self.pos.x = rect.x

    def _move_y(self, dt: float, platforms, level_height: int) -> None:
        self.pos.y += self.vel.y * dt
        rect = self.rect
        self.grounded = False

        for platform in platforms:
            if not rect.colliderect(platform):
                continue
            if self.vel.y > 0:
                rect.bottom = platform.top
                self.vel.y = 0
                self.grounded = True
            elif self.vel.y < 0:
                rect.top = platform.bottom
                self.vel.y = 0

        if rect.bottom > level_height:
            rect.bottom = level_height
            self.vel.y = 0
            self.grounded = True

        self.pos.y = rect.y

    def draw(self, surface: pygame.Surface, camera) -> None:
        rect = camera.apply(self.rect)
        shadow = rect.move(4, 6)
        pygame.draw.rect(
            surface,
            COLORS["player_shadow"],
            shadow,
            border_radius=8,
        )
        pygame.draw.rect(surface, COLORS["player"], rect, border_radius=8)

        eye_y = rect.y + 14
        pygame.draw.circle(surface, COLORS["panel"], (rect.x + 11, eye_y), 3)
        pygame.draw.circle(
            surface,
            COLORS["panel"],
            (rect.right - 11, eye_y),
            3,
        )
