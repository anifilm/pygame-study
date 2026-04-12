import pygame
from settings import *


class Barrier:
    def __init__(self, x, y):
        self.blocks = pygame.sprite.Group()
        self._create_barrier(x, y)

    def _create_barrier(self, start_x, start_y):
        shape = [
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        ]

        for row_i, row in enumerate(shape):
            for col_i, cell in enumerate(row):
                if cell:
                    block = BarrierBlock(
                        start_x + col_i * BARRIER_BLOCK_SIZE,
                        start_y + row_i * BARRIER_BLOCK_SIZE
                    )
                    self.blocks.add(block)

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)


class BarrierBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(
            (BARRIER_BLOCK_SIZE, BARRIER_BLOCK_SIZE), pygame.SRCALPHA
        )
        self.image.fill(pygame.Color(COLORS['barrier']))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = BARRIER_HEALTH

    def hit(self):
        self.health -= 1
        alpha = int(255 * (self.health / BARRIER_HEALTH))
        color = pygame.Color(COLORS['barrier'])
        color.a = alpha
        self.image.fill(color)
        if self.health <= 0:
            self.kill()
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BarrierManager:
    def __init__(self):
        self.barriers = []
        self._create_barriers()

    def _create_barriers(self):
        self.barriers = []
        barrier_width = 15 * BARRIER_BLOCK_SIZE
        total_width = BARRIER_COUNT * barrier_width
        spacing = (WINDOW_WIDTH - total_width) / (BARRIER_COUNT + 1)
        barrier_y = GAME_BOTTOM - 80

        for i in range(BARRIER_COUNT):
            x = spacing + i * (barrier_width + spacing)
            self.barriers.append(Barrier(x, barrier_y))

    def reset(self):
        self._create_barriers()

    def get_all_blocks(self):
        all_blocks = pygame.sprite.Group()
        for barrier in self.barriers:
            for block in barrier.blocks:
                all_blocks.add(block)
        return all_blocks

    def draw(self, surface):
        for barrier in self.barriers:
            barrier.draw(surface)