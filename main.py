import getopt
import sys
import threading
from os import path
from configparser import ConfigParser


import console
from core.controller.camera import Camera
from core.prefabs.sprites import *
from world.chunk import Chunk
from world.material import Material
from world.entity.materials import Materials
from world.world import World
from world.spawner import Spawner
from world.entity.entitytypes import EntityTypes
from cfg.cfgparser import CfgParser


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
		self.graphics = assets.populate_assets()
		self.load_data()
		self.world = None

		# Make console
		self.console = console.Console(self)
		self.consoleThread = threading.Thread(target=self.console.run, daemon=True)

	def load_data(self):
		game_folder = path.dirname(__file__)
		assets_folder = path.join(game_folder, 'assets')
		Materials.load(self)
		EntityTypes.load(self)

		# Initialize config
		self.cpc = ConfigParser()  # ConfigParserControls
		self.cpc = ConfigParser()  # ConfigParserControls
		self.cpc.read(path.join(path.dirname(__file__), 'cfg/controls.ini'))
		cfgp = CfgParser(self, path.join(game_folder, 'cfg/autoexec.cfg'))
		cfgp.read()

	def new(self):
		# Initialize all variables and do all the setup for a new game
		self.sprites = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()
		self.trees = pygame.sprite.Group()
		self.world = World(path.join(path.dirname(__file__), "saves/world1"))
		self.world.load()
		self.player = Player(self, 20, 20, 0, 350, 0, 0)
		self.spawner = Spawner(self, 64, 1)

		# Initialize camera map specific
		# TODO: might have to change the camera's settings
		self.camera = Camera(48, 16)
		# self.items = item.populate_items(self.graphics)

		self.consoleThread.start()
		print("Reading console input")

	def run(self):
		# game loop - set self.playing = False to end the game
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.update()
			self.draw()

	def quit(self):
		self.console.kill()
		pygame.quit()
		sys.exit()

	def update(self):
		# update portion of the game loop
		self.sprites.update()
		self.camera.update(self.player)

	def draw(self):
		pygame.display.set_caption(TITLE + " - " + "{:.2f}".format(self.clock.get_fps()))
		self.screen.fill(BGCOLOR)

		px = self.player.pos.x / TILESIZE // 16
		py = self.player.pos.y / TILESIZE // 16

		# print(f"Player pos: {self.player.pos.x / TILESIZE:.2f}, {self.player.pos.y / TILESIZE:.2f}")
		# TODO: add setting for "render distance"
		for cy in range(-2, 2):
			for cx in range(-2, 2):
				chunk: Chunk = self.world.getChunkAt(px + cx, py + cy)
				# print(f"Rendering chunk: {px+cx},{py+cy}")
				for y in range(16):
					for x in range(16):
						mat: Material = chunk.getBlock(x, y).material
						if mat is not None and mat.image is not None:
							self.screen.blit(mat.image, self.camera.applyraw(
								mat.rect.move(((px + cx) * 16 + x) * TILESIZE, ((py + cy) * 16 + y) * TILESIZE)))

				for ent in self.world.entities:
					if ent is not None and ent.entitytype.image is not None:
						self.screen.blit(ent.entitytype.image, self.camera.applyraw(
							ent.entitytype.rect.move((ent.chunk[0] * 16 + (ent.pos.x / TILESIZE)) * TILESIZE,
											(ent.chunk[1] * 16 + (ent.pos.y / TILESIZE)) * TILESIZE)
						))

		self.screen.blit(self.player.image, self.camera.apply(self.player))

		# Healthbar van de speler
		currenthealthB = pygame.Rect(50, 50, 180, 50)
		pygame.draw.rect(self.screen, (0, 200, 0), currenthealthB)
		currenthealthT = pygame.font.SysFont('Corbel', 40).render('100', True, (255, 255, 255))
		self.screen.blit(currenthealthT, (currenthealthB.x + 60, currenthealthB.y))

		# Collision debug rects

		# self.screen.blit(Materials.GRASS.value.image,self.camera.apply(self.player))
		# for sprite in self.sprites:
		#	self.screen.blit(sprite.image, self.camera.apply(sprite))

		# Collision debug rects
		# pygame.draw.rect(self.screen, (255, 255, 255), self.camera.apply(self.player), 2)
		# pygame.draw.rect(self.screen, (255, 255, 255), self.player.collision_rect, 2)
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

			self.screen.blit(tQuit, (bQuit.x + 30, bQuit.y + 5))
			self.screen.blit(tPlay, (bPlay.x + 30, bPlay.y + 5))
			self.screen.blit(tOptions, (bOptions.x, bOptions.y + 5))
			pygame.display.update()
			self.clock.tick(60)

	def show_options_screen(self):
		pass

	def show_go_screen(self):
		pass


# create the game object
g = Game()
g.show_start_screen()
g.new()
while True:
	try:
		g.run()
	except pygame.error as err:
		print(err)
	g.show_go_screen()
