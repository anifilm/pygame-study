import pygame
from settings import *
from player import Player
from alien import AlienGroup
from bullet import BulletManager
from barrier import BarrierManager
from score import Score
from explosion import ExplosionManager
from game_over import GameOver


class Game:
    STATE_START = 0
    STATE_PLAYING = 1
    STATE_GAME_OVER = 2
    STATE_LEVEL_CLEAR = 3
    STATE_PAUSED = 4

    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Space Invaders')

        self.score = Score()
        self.game_over_screen = GameOver()
        self.explosion_manager = ExplosionManager()
        self.bullet_manager = BulletManager()
        self.barrier_manager = BarrierManager()
        self.alien_group = AlienGroup(self)
        self.player = Player(self)

        self.state = self.STATE_START

    def reset_game(self):
        self.player = Player(self)
        self.alien_group = AlienGroup(self)
        self.bullet_manager = BulletManager()
        self.barrier_manager = BarrierManager()
        self.explosion_manager = ExplosionManager()
        self.score.reset()
        self.alien_group.create_aliens()
        self.state = self.STATE_PLAYING

    def next_level(self):
        self.score.next_level()
        self.alien_group = AlienGroup(self)
        self.alien_group.alien_fire_rate += LEVEL_FIRE_INCREASE
        self.alien_group.speed += LEVEL_SPEED_INCREASE
        self.alien_group.create_aliens()
        self.bullet_manager = BulletManager()
        self.barrier_manager.reset()
        self.explosion_manager = ExplosionManager()
        self.player.rect.centerx = WINDOW_WIDTH // 2
        self.player.rect.bottom = GAME_BOTTOM - 10
        self.state = self.STATE_PLAYING

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if self.state == self.STATE_START:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()

                elif self.state == self.STATE_PLAYING:
                    if event.key == pygame.K_p:
                        self.state = self.STATE_PAUSED

                elif self.state == self.STATE_PAUSED:
                    if event.key == pygame.K_p:
                        self.state = self.STATE_PLAYING

                elif self.state == self.STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

                elif self.state == self.STATE_LEVEL_CLEAR:
                    if event.key == pygame.K_SPACE:
                        self.next_level()

    def update(self):
        if self.state != self.STATE_PLAYING:
            return

        self.player.update()
        self.alien_group.update()
        self.bullet_manager.update()
        self.explosion_manager.update()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.player.shoot():
                self.bullet_manager.player_shoot(
                    self.player.rect.centerx,
                    self.player.rect.top
                )

        self._check_collisions()

        if len(self.alien_group.aliens) == 0:
            self.state = self.STATE_LEVEL_CLEAR

        if self.alien_group.check_reach_bottom():
            self.state = self.STATE_GAME_OVER

        if self.player.lives <= 0:
            self.state = self.STATE_GAME_OVER

    def _check_collisions(self):
        for bullet in self.bullet_manager.player_bullets:
            hit_aliens = pygame.sprite.spritecollide(
                bullet, self.alien_group.aliens, True
            )
            for alien in hit_aliens:
                self.score.add_score(alien.score)
                self.explosion_manager.add(
                    alien.rect.centerx, alien.rect.centery,
                    alien.alien_type
                )
                bullet.kill()

        for bullet in self.bullet_manager.alien_bullets:
            if self.player.rect.colliderect(bullet.rect):
                if self.player.hit():
                    self.explosion_manager.add(
                        self.player.rect.centerx,
                        self.player.rect.centery,
                        'cyan'
                    )
                    bullet.kill()

            blocks = self.barrier_manager.get_all_blocks()
            hit_blocks = pygame.sprite.spritecollide(bullet, blocks, False)
            for block in hit_blocks:
                block.hit()
                bullet.kill()
                break

        blocks = self.barrier_manager.get_all_blocks()
        for bullet in self.bullet_manager.player_bullets:
            hit_blocks = pygame.sprite.spritecollide(bullet, blocks, False)
            for block in hit_blocks:
                block.hit()
                bullet.kill()
                break

        for alien in self.alien_group.aliens:
            hit_blocks = pygame.sprite.spritecollide(alien, blocks, True)
            if hit_blocks:
                for block in hit_blocks:
                    block.kill()

    def draw(self):
        self.display_surface.fill(pygame.Color(COLORS['bg']))

        if self.state == self.STATE_START:
            self.game_over_screen.draw_start_screen(self.display_surface)
        elif self.state == self.STATE_PLAYING or self.state == self.STATE_PAUSED:
            self.player.draw(self.display_surface)
            self.alien_group.draw(self.display_surface)
            self.bullet_manager.draw(self.display_surface)
            self.barrier_manager.draw(self.display_surface)
            self.explosion_manager.draw(self.display_surface)
            self.score.draw(self.display_surface, self.player.lives)

            if self.state == self.STATE_PAUSED:
                overlay = pygame.Surface(
                    (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA
                )
                overlay.fill((0, 0, 0, 128))
                self.display_surface.blit(overlay, (0, 0))
                font = pygame.font.SysFont('arial', 48, bold=True)
                text = font.render('PAUSED', True, pygame.Color(COLORS['white']))
                self.display_surface.blit(
                    text,
                    (WINDOW_WIDTH // 2 - text.get_width() // 2,
                     WINDOW_HEIGHT // 2 - text.get_height() // 2)
                )

        elif self.state == self.STATE_GAME_OVER:
            self.player.draw(self.display_surface)
            self.alien_group.draw(self.display_surface)
            self.barrier_manager.draw(self.display_surface)
            self.score.draw(self.display_surface, self.player.lives)
            self.game_over_screen.draw_game_over(
                self.display_surface, self.score.score
            )

        elif self.state == self.STATE_LEVEL_CLEAR:
            self.score.draw(self.display_surface, self.player.lives)
            self.game_over_screen.draw_victory(
                self.display_surface, self.score.score, self.score.level
            )

        pygame.display.update()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)