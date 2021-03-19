import pygame
from pygame.locals import *
from settings import *
from sprites import *
from os import path
import sys
import getopt
import tilemap
# from os import system
# system('cls')

# TODO: make this better lol
# Check arguments
try:
	opts, args = getopt.getopt(sys.argv[1:], 'f', ["fps="])
except getopt.GetoptError as err:
	print(err)
for o, a in opts:
	if o == '--fps':
		FPS = a

print('FPS is: ', FPS)


class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		pygame.key.set_repeat(1, 100)
		self.load_data()

	def load_data(self):
		game_folder = path.dirname(__file__)
		self.map = tilemap.Map(path.join(game_folder+'/saves/', 'map2.txt'))

	def new(self):
		# initialize all variables and do all the setup for a new game
		self.sprites = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()
		for row, tiles in enumerate(self.map.data):
			for col, tile in enumerate(tiles):
				if tile == '1':
					Wall(self, col, row)
				if tile == 'P':
					self.player = Player(self, col, row)
		# Initialize camera map specific
		# TODO: might have to change the camera's settings
		self.camera = tilemap.Camera(self.map.width, self.map.height)

	def run(self):
		# game loop - set self.playing = False to end the game
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.update()
			self.draw()

	def quit(self):
		pygame.quit()
		sys.exit()

	def update(self):
		# update portion of the game loop
		self.sprites.update()
		self.camera.update(self.player)

	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):
			pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

	def draw(self):
		self.screen.fill(BGCOLOR)
		self.draw_grid()
		for sprite in self.sprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		pygame.display.flip()

	def events(self):
		# catch all events here
		for event in pygame.event.get():
			if event.type == QUIT:
				self.quit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.quit()

	def show_start_screen(self):
		pass

	def show_go_screen(self):
		pass


# create the game object
g = Game()
g.show_start_screen()
while True:
	g.new()
	g.run()
	g.show_go_screen()
