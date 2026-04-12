from settings import *
from os import path
import pygame

class GameOverPopup:
    def __init__(self, display_surface, bg_music, reset_game_callback):
        # General setup
        self.display_surface = display_surface
        self.bg_music = bg_music
        self.reset_game_callback = reset_game_callback

        # Popup dimensions
        self.popup_width, self.popup_height = 400, 300

        # Font setup
        self.font_path = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'graphics', 'Russo_One.ttf')
        self.font_large = pygame.font.Font(self.font_path, 50)
        self.font_medium = pygame.font.Font(self.font_path, 30)
        self.font_small = pygame.font.Font(self.font_path, 20)

        # Button rectangles (will be set in draw method)
        self.yes_button = None
        self.no_button = None

    def draw(self, score):
        # Create a semi-transparent overlay for the entire window
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        self.display_surface.blit(overlay, (0, 0))

        # Create a popup panel in the center of the screen
        popup = pygame.Surface((self.popup_width, self.popup_height))
        popup.fill(GRAY)  # Match the game background

        # Add a border to the popup
        popup_rect = popup.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        # Game Over text
        game_over_text = self.font_large.render('GAME OVER', True, 'white')
        game_over_rect = game_over_text.get_rect(center=(self.popup_width // 2, 70))
        popup.blit(game_over_text, game_over_rect)

        # Score display
        score_text = self.font_small.render(f'Score: {score}', True, 'white')
        score_rect = score_text.get_rect(center=(self.popup_width // 2, 120))
        popup.blit(score_text, score_rect)

        # Retry text
        retry_text = self.font_medium.render('Retry?', True, 'white')
        retry_rect = retry_text.get_rect(center=(self.popup_width // 2, 170))
        popup.blit(retry_text, retry_rect)

        # Calculate absolute positions for buttons
        mouse_pos = pygame.mouse.get_pos()

        # No button (on the left)
        no_button_rect = pygame.Rect(0, 0, 100, 50)
        no_button_rect.center = (self.popup_width // 2 - 70, 230)  # Left position

        # Calculate absolute position for collision detection
        no_button_abs = pygame.Rect(
            popup_rect.x + no_button_rect.x,
            popup_rect.y + no_button_rect.y,
            no_button_rect.width,
            no_button_rect.height
        )

        # Check if mouse is over the No button
        no_hovering = no_button_abs.collidepoint(mouse_pos)
        no_color = 'red' if no_hovering else '#eb6466'  # Bright red when hovering

        pygame.draw.rect(popup, no_color, no_button_rect, border_radius=10)
        no_text = self.font_medium.render('No', True, 'white')
        no_text_rect = no_text.get_rect(center=no_button_rect.center)
        popup.blit(no_text, no_text_rect)

        # Yes button (on the right)
        yes_button_rect = pygame.Rect(0, 0, 100, 50)
        yes_button_rect.center = (self.popup_width // 2 + 70, 230)  # Right position

        # Calculate absolute position for collision detection
        yes_button_abs = pygame.Rect(
            popup_rect.x + yes_button_rect.x,
            popup_rect.y + yes_button_rect.y,
            yes_button_rect.width,
            yes_button_rect.height
        )

        # Check if mouse is over the Yes button
        yes_hovering = yes_button_abs.collidepoint(mouse_pos)
        yes_color = 'green' if yes_hovering else '#65c421'  # Bright green when hovering
        pygame.draw.rect(popup, yes_color, yes_button_rect, border_radius=10)
        yes_text = self.font_medium.render('Yes', True, 'white')
        yes_text_rect = yes_text.get_rect(center=yes_button_rect.center)
        popup.blit(yes_text, yes_text_rect)

        # Draw popup on screen
        self.display_surface.blit(popup, popup_rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, popup_rect, 3, 2)

        # Store button positions for event handling
        self.yes_button = pygame.Rect(popup_rect.x + yes_button_rect.x, popup_rect.y + yes_button_rect.y,
                                     yes_button_rect.width, yes_button_rect.height)
        self.no_button = pygame.Rect(popup_rect.x + no_button_rect.x, popup_rect.y + no_button_rect.y,
                                    no_button_rect.width, no_button_rect.height)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.yes_button.collidepoint(event.pos):
                # Reset game when Yes is clicked
                self.reset_game_callback()
                return True
            elif self.no_button.collidepoint(event.pos):
                # Stop music and exit when No is clicked
                self.bg_music.stop()
                pygame.quit()
                exit()
        return False
