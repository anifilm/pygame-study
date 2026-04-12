from settings import *
from random import choice
from sys import exit
from os import path
import math

from timer import Timer
from game_over import GameOverPopup

class Game:
    def __init__(self, get_next_shape, update_score, bg_music):
        # Background music
        self.bg_music = bg_music
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # Game state
        self.game_over = False
        self.game_active = True

        # Game over popup
        self.game_over_popup = GameOverPopup(self.display_surface, self.bg_music, self.reset_game)

        # game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        # lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)

        # sound setup
        self.sound_dir = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'sound')
        # sfx sound
        self.landing_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'landing.wav'))
        self.landing_sound.set_volume(0.5)  # Set volume to 50%
        self.drop_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'drop.mp3'))
        self.drop_sound.set_volume(0.5)  # Set volume to 50%

        # tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), self.sprites, self.create_new_tetromino, self.field_data, self.drop_sound)

        # timer
        self.down_speed = UPDATE_START_SPEED
        self.timers = {
            'vertical move': Timer(UPDATE_START_SPEED, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME),
            'drop': Timer(DROP_WAIT_TIME),
        }
        self.timers['vertical move'].activate()

        # score
        self.current_level = 1
        self.current_lines = 0
        self.current_score = 0

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level

        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.75
            self.timers['vertical move'].duration = self.down_speed

        self.update_score(self.current_level, self.current_lines, self.current_score)

    def check_game_over(self):
        # Check if any blocks are above the playing field
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                self.game_over = True
                # Pause background music when game is over
                self.bg_music.stop()
                return True
        return False

    def create_new_tetromino(self):
        if self.check_game_over():
            return
        self.check_finished_rows()
        self.tetromino = Tetromino(self.get_next_shape(), self.sprites, self.create_new_tetromino, self.field_data, self.drop_sound)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0, y), (self.surface.get_width(), y))

        self.surface.blit(self.line_surface, (0, 0))

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.tetromino.move_down()
                self.timers['horizontal move'].activate()

        if not self.timers['rotate'].active:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()

        if not self.timers['drop'].active:
            if keys[pygame.K_SPACE]:
                self.tetromino.move_drop()
                self.timers['drop'].activate()

    def check_finished_rows(self):
        # get the full row indexs
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:
                # delete full rows
                for block in self.field_data[delete_row]:
                    block.kill()
                # move down blocks
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1
            # rebuild the field data
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            self.landing_sound.play()
            # update score
            self.calculate_score(len(delete_rows))

    def reset_game(self):
        # Reset game state
        self.game_over = False
        self.game_active = True

        # Clear field and sprites
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.sprites.empty()

        # Reset score
        self.current_level = 1
        self.current_lines = 0
        self.current_score = 0
        self.down_speed = UPDATE_START_SPEED
        self.timers['vertical move'].duration = self.down_speed
        self.update_score(self.current_level, self.current_lines, self.current_score)

        # Restart background music
        self.bg_music.play(loops=-1)

        # Create new tetromino
        self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), self.sprites, self.create_new_tetromino, self.field_data, self.drop_sound)

    def handle_game_over_events(self, event):
        # Delegate event handling to the GameOverPopup class
        self.game_over_popup.handle_events(event)

    def run(self):
        # Always draw the game
        # update
        if not self.game_over:
            self.input()
            self.timer_update()
            self.sprites.update()

        # drawing
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

        # Draw game over screen on top if game is over
        if self.game_over:
            self.game_over_popup.draw(self.current_score)


class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data, drop_sound):
        # sound
        self.drop_sound = drop_sound
        # setup
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data
        # rotation state (0-3, representing 0, 90, 180, 270 degrees)
        self.rotation_state = 0
        # create blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    # collisions
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in blocks]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, blocks, amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in blocks]
        return True if any(collision_list) else False

    # movement
    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            self.drop_sound.play()
            self.create_new_tetromino()

    def move_drop(self):
        while not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            self.drop_sound.play()
            self.create_new_tetromino()

    # rotation
    def rotate(self, clockwise=True):
        if self.shape == 'O':
            return

        # 1. pivot point
        if (self.shape == 'I'):
            if self.rotation_state % 2 == 0:  # Horizontal (0 or 2)
                pivot_pos = pygame.Vector2(
                    (self.blocks[1].pos.x + self.blocks[2].pos.x) / 2,
                    self.blocks[1].pos.y)
            else:  # Vertical (1 or 3)
                pivot_pos = pygame.Vector2(
                    self.blocks[1].pos.x,
                    (self.blocks[1].pos.y + self.blocks[2].pos.y) / 2)
        else:
            # For other pieces, pivot is on the center block
            pivot_pos = self.blocks[2].pos

        # 2. Calculate new rotation state
        old_rotation_state = self.rotation_state
        if clockwise:
            new_rotation_state = (self.rotation_state + 1) % 4
        else:
            new_rotation_state = (self.rotation_state - 1) % 4

        # 3. Get wall kick data based on shape and rotation
        kick_type = 'JLSTZ' if self.shape in 'JLSTZ' else 'I'
        kick_key = f'{old_rotation_state}>>{new_rotation_state}'
        wall_kicks = WALL_KICK_DATA[kick_type][kick_key]

        # 4. Try each kick offset until one works
        for kick_offset in wall_kicks:
            # Calculate new positions with the current kick offset
            test_positions = []
            for block in self.blocks:
                # First rotate
                rotated_pos = block.rotate(pivot_pos, clockwise)

                if (self.shape == 'I'): # fixed 'I' tetromino offset
                    if self.rotation_state == 0:
                        rotated_pos.x = math.ceil(rotated_pos.x)
                        rotated_pos.y = math.floor(rotated_pos.y)
                    elif self.rotation_state == 1:
                        rotated_pos.x = math.floor(rotated_pos.x)
                        rotated_pos.y = math.floor(rotated_pos.y)
                    elif self.rotation_state == 2:
                        rotated_pos.x = math.floor(rotated_pos.x)
                        rotated_pos.y = math.ceil(rotated_pos.y)
                    elif self.rotation_state == 3:
                        rotated_pos.x = math.ceil(rotated_pos.x)
                        rotated_pos.y = math.ceil(rotated_pos.y)

                # Then apply kick offset
                kicked_pos = pygame.Vector2(rotated_pos.x + kick_offset[0], rotated_pos.y + kick_offset[1])
                test_positions.append(kicked_pos)

            # Check if these positions are valid
            valid_positions = True
            for pos in test_positions:
                # Check boundaries
                if pos.x < 0 or pos.x >= COLUMNS or pos.y >= ROWS:
                    valid_positions = False
                    break
                # Check collision with existing blocks (only if position is within field)
                if pos.y >= 0 and self.field_data[int(pos.y)][int(pos.x)]:
                    valid_positions = False
                    break

            # If valid, apply the rotation and kick
            if valid_positions:
                # Update rotation state
                self.rotation_state = new_rotation_state
                # Apply new positions
                for i, block in enumerate(self.blocks):
                    block.pos = test_positions[i]
                return True  # Rotation successful

        # If we get here, no valid kick was found
        return False

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        # general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)
        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft=(self.pos * CELL_SIZE))

    def rotate(self, pivot_pos, clockwise):
        return pivot_pos + (self.pos - pivot_pos).rotate(-90 if clockwise else 90)

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS:
            return True

        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if y >= ROWS:
            return True

        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE
