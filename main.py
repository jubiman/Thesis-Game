import pygame
from pygame.locals import *
from settings import *
from sprites import *
from os import path
import sys
import getopt
import tilemap
import assets
# from os import system
# system('cls')

# TODO: make this better lol
# Check arguments
try:
	opts, args = getopt.getopt(sys.argv[1:], 'f', ["fps="])
except getopt.GetoptError as err:
	print(err)
	sys.exit()
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
		self.graphics = assets.populate_assets()
		# TODO: for loop to populate assets

	def load_data(self):
		game_folder = path.dirname(__file__)
		assets_folder = path.join(game_folder, 'assets')
		self.map = tilemap.Map(path.join(game_folder, 'saves/map3.txt'))
		# self.player_img = pygame.image.load(path.join(assets_folder, 'visual/')).convert_alpha()
		# self.player_img = pygame.transform.scale(assets.get_asset_from_name(self.graphics, 'player1').image, (64, 64))

	def new(self):
		# initialize all variables and do all the setup for a new game
		self.sprites = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()
		self.trees = pygame.sprite.Group()
		for row, tiles in enumerate(self.map.data):
			for col, tile in enumerate(tiles):
				if tile == '1':
					Wall(self, col, row)
				if tile == 'P':
					self.player = Player(self, 20, 20, 0, 350, col, row)
				if tile == 'T':
					Tree(self, col, row)
		Enemy_standard(self, 20, 20, 0, 350, 4, 4)
		# Initialize camera map specific
		# TODO: might have to change the camera's settings
		self.camera = tilemap.Camera(self.map.width, self.map.height)
		self.items = item.populate_items()

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
		pygame.display.set_caption(TITLE + " - " + "{:.2f}".format(self.clock.get_fps()))
		self.screen.fill(BGCOLOR)
		self.draw_grid()
		for sprite in self.sprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		pygame.draw.rect(self.screen, (255, 255, 255), self.camera.apply(self.player), 2)
		pygame.draw.rect(self.screen, (255, 255, 255), self.player.collision_rect, 2)
		pygame.display.flip()

	def events(self):
		# catch all events here
		for event in pygame.event.get():
			if event.type == QUIT:
				self.quit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.show_start_screen()

	def show_start_screen(self):
		# Placeholder for an actual main menu
		tQuit = pygame.font.SysFont('Corbel', 35).render('QUIT', True, (255, 255, 255))
		tPlay = pygame.font.SysFont('Corbel', 35).render('PLAY', True, (255, 255, 255))
		tOptions = pygame.font.SysFont('Corbel', 35).render('OPTIONS', True, (255, 255, 255))

		while True:
			bQuit = pygame.Rect(WIDTH / 2 - 75, HEIGHT / 2, 140, 40)
			bPlay = pygame.Rect(WIDTH / 2 - 75, HEIGHT / 2 - 175, 140, 40)
			bOptions = pygame.Rect(WIDTH / 2 - 75, HEIGHT / 2 - 75, 140, 40)

			mouse = pygame.mouse.get_pos()
			for ev in pygame.event.get():
				if ev.type == QUIT:
					self.quit()

				# checks if a mouse is clicked
				if ev.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:

					# if the mouse is clicked on the
					# button the game is terminated
					if bQuit.collidepoint(mouse):
						self.quit()
					if bPlay.collidepoint(mouse):
						return
					if bOptions.collidepoint(mouse):
						self.show_options_screen()

			self.screen.fill((255, 255, 255))
			if bQuit.collidepoint(mouse):
				pygame.draw.rect(self.screen, (170, 170, 170), bQuit)
			else:
				pygame.draw.rect(self.screen, (100, 100, 100), bQuit)
			if bPlay.collidepoint(mouse):
				pygame.draw.rect(self.screen, (170, 170, 170), bPlay)
			else:
				pygame.draw.rect(self.screen, (100, 100, 100), bPlay)
			if bOptions.collidepoint(mouse):
				pygame.draw.rect(self.screen, (170, 170, 170), bOptions)
			else:
				pygame.draw.rect(self.screen, (100, 100, 100), bOptions)

			self.screen.blit(tQuit, (bQuit.x+30, bQuit.y+5))
			self.screen.blit(tPlay, (bPlay.x+30, bPlay.y+5))
			self.screen.blit(tOptions, (bOptions.x, bOptions.y+5))
			pygame.display.update()
			self.clock.tick(60)

	def show_options_screen(self):
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
