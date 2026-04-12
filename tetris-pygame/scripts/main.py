from settings import *
from sys import exit
from os import path
from random import choice

# components
from game import Game
from score import Score
from preview import Preview

class Main:
	def __init__(self):
		# general
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption('Tetris')

		# sound setup
		self.sound_dir = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'sound')
		# background music
		self.bg_music = pygame.mixer.Sound(path.join(self.sound_dir, 'music.wav'))
		self.bg_music.set_volume(0.2)  # Set volume to 20%
		self.bg_music.play(loops=-1)  # Play on loop

		# shapes
		self.next_shapes = [choice(list(TETROMINOS.keys())) for _ in range(3)]

		# components
		self.preview = Preview()
		self.score = Score()
		self.game = Game(self.get_next_shape, self.update_score, self.bg_music)

	def update_score(self, level, lines, score):
		self.score.level = level
		self.score.lines = lines
		self.score.score = score

	def get_next_shape(self):
		next_shape = self.next_shapes.pop(0)
		self.next_shapes.append(choice(list(TETROMINOS.keys())))
		return next_shape

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

				# Handle game over events if game is over
				if self.game.game_over:
					self.game.handle_game_over_events(event)

			# display
			self.display_surface.fill(GRAY)

			self.preview.run(self.next_shapes)
			self.score.run()
			self.game.run()

			# updating the game
			pygame.display.update()
			self.clock.tick()


if __name__ == '__main__':
	main = Main()
	main.run()
