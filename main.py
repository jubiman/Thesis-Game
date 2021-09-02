import ctypes
import getopt
import sys
import threading
from configparser import ConfigParser
from os import path, mkdir

from cfg.cfgparser import CfgParser
from core.assets.assets import Assets
from core.console.consolefunctions import ConsoleFunctions
from core.console.console import Console
from core.controller.camera import Camera
from core.input.inputhandler import InputHandler
from core.items.items import Items
from core.UI.ui import UI
from core.utils.colors import Colors
from core.utils.settings import Settings
from world.chunk import Chunk
from world.entity.entities.player import Player
from world.entity.entitytypes import EntityTypes
from world.material.material import Material
from world.material.materials import Materials
from world.spawner import Spawner
from world.world import World

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN


class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((Settings.Game.WIDTH, Settings.Game.HEIGHT))
		pygame.display.set_caption(Settings.Game.TITLE)
		self.clock = pygame.time.Clock()
		pygame.key.set_repeat(1, 100)
		self.load_data()

		self.world = None
		self.camera = None

		# Make input handler
		self.inputHandler = InputHandler(self)

		# Make console
		self.console = ConsoleFunctions(self)
		self.consoleThread = threading.Thread(name="console", target=self.console.run, daemon=True)

	def change_world(self, newworld: World) -> None:
		"""
		Safely change the world to another world.

		:param newworld: The world to change to.
		:return: None
		"""
		self.world.unload_all()
		newworld.load()
		self.world = newworld

	def load_data(self) -> None:
		"""
		Pre-init for the game.

		:return: None
		"""
		game_folder = path.dirname(__file__)

		# Load assets
		Assets.load()
		Materials.load()
		EntityTypes.load()
		Items.load()

		# Initialize config
		self.cpc = ConfigParser()  # ConfigParserControls
		self.cpc.read(path.join(path.dirname(__file__), 'cfg/settings.ini'))
		cfgp = CfgParser(self, path.join(game_folder, 'cfg/autoexec.cfg'))
		cfgp.read()

	def new(self) -> None:
		"""
		Post-init for the game object.

		:return: None.
		"""
		# Initialize all variables and do all the setup for a new game
		self.world = World(path.join(path.dirname(__file__), "saves/world1"), self)
		self.player = Player(self, 100, 100, 0, 350, 0.5, 0.5, EntityTypes.PLAYER.value, 5)
		self.world.load()
		self.spawner = Spawner(self, 64, 1)

		# Initialize camera
		self.camera = Camera()

		UI.load(self)

		# Start the console
		self.consoleThread.start()
		Console.log(thread="MAIN", message="Reading console input.")

	def run(self):
		# game loop - set self.playing to False to end the game
		self.playing = True
		self.paused = False
		while self.playing and self.paused:
			try:
				self.dt = self.clock.tick(Settings.Game.FPS) / 1000
			except pygame.error:
				# TODO: Improve error handling to not skip steps on error
				Console.error(thread="UnknownThread", message=pygame.get_error())
		while self.playing and not self.paused:
			try:
				self.dt = self.clock.tick(Settings.Game.FPS) / 1000
				self.events()
				self.update()
				self.draw()
			except pygame.error:
				# TODO: Improve error handling to not skip steps on error
				Console.error(thread="UnknownThread", message=pygame.get_error())

		# We are now paused or we stopped playing
		if self.playing:  # We are still playing, but just paused
			while self.paused:  # Hold until we stop pausing
				pass  # Nothing to do
			if self.playing:  # If we did not pause and quit, run the game again
				return self.run()

	def quit(self):
		Console.log("Quiting...")
		self.world.unload_all()
		self.console.kill()
		pygame.quit()
		sys.exit()

	def update(self) -> None:
		"""
		The update() function is called every frame. This function handles rendering and user input.
		Also updates player client-side.

		:return: None.
		"""
		self.inputHandler.handleInput()
		self.player.update()
		self.camera.update(self.player.entitytype)
		self.world.tick()

	def draw(self):
		pygame.display.set_caption(Settings.Game.TITLE + " - " + "{:.2f}".format(self.clock.get_fps()) +
									" - ({:.4f}, {:.4f})".format(*self.player.pos))
		self.screen.fill(Colors.BGCOLOR)

		pcx = self.player.pos.x // 16
		pcy = self.player.pos.y // 16

		# Console.debug((self.player.pos.x / Settings.Game.TILESIZE, self.player.pos.y / Settings.Game.TILESIZE))

		# print(f"Player pos: {self.player.pos.x / Settings.Game.TILESIZE:.2f}, {self.player.pos.y / Settings.Game.TILESIZE:.2f}")
		# TODO: add setting for "render distance"
		for cy in range(-2, 3):
			for cx in range(-2, 3):
				# Console.debug(f"Rendering {pcx + cx, pcy + cy}")
				chunk: Chunk = self.world.getChunkAt(pcx + cx, pcy + cy)
				# print(f"Rendering chunk: {px+cx},{py+cy}")
				for y in range(16):
					for x in range(16):
						mat: Material = chunk.getBlock(x, y).material
						if mat is not None and mat.image is not None:
							self.screen.blit(mat.image, self.camera.applyraw(
								mat.rect.move(((pcx + cx) * 16 + x) * Settings.Game.TILESIZE, ((pcy + cy) * 16 + y) * Settings.Game.TILESIZE)))

		# pygame.draw.rect(self.screen, (255, 255, 255), self.camera.applyraw(self.player.collision_rect), 1)

		for ent in self.world.entities:
			if ent is not None and ent.entitytype.image is not None:
				# Console.debug(f"ent: {ent.pos}, {ent.chunk}")
				self.screen.blit(ent.entitytype.image, self.camera.applyraw(
					ent.entitytype.rect.move((ent.chunk[0] * 16 + ent.pos.x) * Settings.Game.TILESIZE,
												(ent.chunk[1] * 16 + ent.pos.y) * Settings.Game.TILESIZE)
				))

		self.screen.blit(self.player.entitytype.image, self.camera.apply(self.player.entitytype))

		# Display UI
		UI.draw()

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
					self.paused = True
					# TODO: maybe make a in-game pause menu?
					self.show_start_screen()

	def show_start_screen(self):
		# Placeholder for an actual main menu
		tQuit = pygame.font.SysFont('Corbel', 35).render('QUIT', True, (255, 255, 255))
		tPlay = pygame.font.SysFont('Corbel', 35).render('PLAY', True, (255, 255, 255))
		tOptions = pygame.font.SysFont('Corbel', 35).render('OPTIONS', True, (255, 255, 255))

		while True:
			bQuit = pygame.Rect(Settings.Game.WIDTH / 2 - 75, Settings.Game.HEIGHT / 2, 140, 40)
			bPlay = pygame.Rect(Settings.Game.WIDTH / 2 - 75, Settings.Game.HEIGHT / 2 - 175, 140, 40)
			bOptions = pygame.Rect(Settings.Game.WIDTH / 2 - 75, Settings.Game.HEIGHT / 2 - 75, 140, 40)

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


def main(argv):
	# TODO: make this better lol
	# Check console-line arguments
	try:
		opts, args = getopt.getopt(argv[1:], 'f', ["fps="])
	except getopt.GetoptError as err:
		Console.log(thread="Player",
					message=err)
		sys.exit()
	for o, a in opts:
		if o == '--fps':
			Settings.FPS = a

	# If the platform is Windows (win32) we need to load a kernal module and set the mode so we can have colored output
	if sys.platform == "win32":
		kernel32 = ctypes.windll.kernel32
		kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

	if not path.isdir("saves"):
		mkdir("saves")

	# Create the game object
	g = Game()
	# g.show_start_screen()
	g.new()
	while True:
		try:
			g.run()
		except pygame.error as err:
			# TODO: Decide where to do error handling
			Console.error(message=err)
		g.show_go_screen()


if __name__ == "__main__":
	main(sys.argv)
