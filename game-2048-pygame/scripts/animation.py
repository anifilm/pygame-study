import pygame


def ease_out(t):
    return 1 - (1 - t) ** 2


class AnimationManager:
    SLIDE_DURATION = 100
    SPAWN_DURATION = 120

    def __init__(self):
        self.state = 'idle'
        self.slide_animations = []
        self.merge_positions = []
        self.spawn_info = None
        self.progress = 0.0
        self.start_time = 0

    def start(self, animations, merges, spawn_info):
        if not animations and not spawn_info:
            return
        self.slide_animations = animations
        self.merge_positions = merges
        self.spawn_info = spawn_info
        self.progress = 0.0
        self.start_time = pygame.time.get_ticks()
        if animations:
            self.state = 'sliding'
        elif spawn_info:
            self.state = 'spawning'

    def update(self):
        if self.state == 'idle':
            return

        elapsed = pygame.time.get_ticks() - self.start_time

        if self.state == 'sliding':
            self.progress = min(1.0, elapsed / self.SLIDE_DURATION)
            if self.progress >= 1.0:
                if self.spawn_info:
                    self.state = 'spawning'
                    self.progress = 0.0
                    self.start_time = pygame.time.get_ticks()
                else:
                    self.state = 'idle'

        elif self.state == 'spawning':
            self.progress = min(1.0, elapsed / self.SPAWN_DURATION)
            if self.progress >= 1.0:
                self.state = 'idle'

    def is_animating(self):
        return self.state != 'idle'

    def get_slide_progress(self):
        if self.state == 'sliding':
            return ease_out(self.progress)
        return 1.0

    def get_spawn_progress(self):
        if self.state == 'spawning':
            return ease_out(self.progress)
        return 1.0