import shutil
import sys
from os import path

import pygame.math

from core.items.items import Items
from settings import *
from world.world import World


# TODO: Make new console window for console
class Console:
	def __init__(self, game):
		self.game = game
		self.running = True
		Console.event(thread="ConsoleThread", message="Console initialized")

	@staticmethod
	def log(**kwargs):
		if 'thread' in kwargs:
			print(f"[LOG] ({kwargs['thread']}) {kwargs['message']}\033[0m")
		else:
			print(f"[LOG] (UnkownThread) {kwargs['message']}\033[0m")

	@staticmethod
	def error(**kwargs):
		if 'thread' in kwargs:
			print(f"{ANSI_COLORS['red']}[ERROR] ({kwargs['thread']}) {kwargs['message']}\033[0m")
		else:
			print(f"{ANSI_COLORS['red']}[ERROR] (UnkownThread) {kwargs['message']}\033[0m")

	@staticmethod
	def warning(**kwargs):
		if 'thread' in kwargs:
			print(f"{ANSI_COLORS['red']}[WARNING] ({kwargs['thread']}) {kwargs['message']}\033[0m")
		else:
			print(f"{ANSI_COLORS['red']}[WARNING] (UnkownThread) {kwargs['message']}\033[0m")

	@staticmethod
	def debug(**kwargs):
		if not DEBUG:
			return
		if 'thread' in kwargs:
			print(f"{ANSI_COLORS['green']}[DEBUG] ({kwargs['thread']}) {kwargs['message']}\033[0m")
		else:
			print(f"{ANSI_COLORS['green']}[DEBUG] (UnkownThread) {kwargs['message']}\033[0m")

	@staticmethod
	def event(**kwargs):
		if 'thread' in kwargs:
			print(f"{ANSI_COLORS['yellow']}[EVENT] ({kwargs['thread']}) {kwargs['message']}\033[0m")
		else:
			print(f"{ANSI_COLORS['yellow']}[EVENT] (UnkownThread) {kwargs['message']}\033[0m")

	def give(self, **kwargs):
		try:
			it = Items.getItemFromName(kwargs['item'])
			if it is not None:
				self.game.player.inventory.add_new_item(it, 1 if 'quantity' not in kwargs else int(kwargs['quantity']))
				return
			print(f"Could not add {kwargs['item']} to inventory, please check your spelling and try again.")
		except ValueError:
			print("Could not convert int to string, please check if you put a valid number.")

	def spawn(self, **kwargs):
		try:
			# TODO: add all enemies with arguments
			if self.game.spawner.spawnEventLoc(float(kwargs['x']), float(kwargs['y']),
												None if 'enemy' not in kwargs else kwargs['enemy']):
				print(f"Could not spawn an enemy at ({kwargs['x']}, {kwargs['y']})")
		except KeyError as err:
			print(err)
			self.game.spawner.spawnEvent()
		except ValueError:
			print(f"Could not convert ({kwargs['x']}, {kwargs['y']}) to a position, please try again.")
		print(self.game.world.entities)

	def setpos(self, **kwargs):
		try:
			self.game.player.pos = pygame.math.Vector2(float(kwargs['x']), float(kwargs['y']))
		except ValueError:
			print(
				f"Could not convert ({kwargs['x']}. {kwargs['y']}) to a valid position, please check your values and try again")
		except KeyError:
			print(f"Expected 2 arguments, got {len(kwargs)} instead")

	def xp(self, **kwargs):
		try:
			if kwargs['operation'] == "give" or kwargs['operation'] == "add":
				try:
					if kwargs['object'].lower() == "p" or kwargs['object'].lower() == "player":
						self.game.player.lvl.xp += int(kwargs['amount'])
					# TODO: Add all induvidual skills (possibly without if chain)
				except ValueError:
					print(f"Could not convert {kwargs['amount']} to an integer, please check your values and try again")
				except IndexError:
					print(f"Expected 4 arguments, got {len(kwargs)} instead")
		except ValueError:
			print(f"Could not convert {kwargs['amount']} to an integer, please check your values and try again")
		except KeyError:
			print(f"Expected at least 2 arguments, got {len(kwargs)} instead")
		else:
			self.game.player.check_levels()

	def loadmap(self, **kwargs):
		try:
			p = path.join(GAMEDIR, f"saves/{kwargs['path']}")
			if not path.isdir(p):
				raise NotADirectoryError
			self.game.world = World(p, self.game)
			self.game.world.load()
		except IndexError:
			print(f"Expected at least 1 argument, got {len(kwargs)} instead")
		except NotADirectoryError:
			try:
				p = path.join(GAMEDIR, f"world/dungeon/dungeons/{kwargs['path'].rsplit('/')[-1]}")
				if not path.isdir(p):
					raise NotADirectoryError
				try:
					pa = kwargs['path']
					print(f"Copying {p} to {path.join(GAMEDIR, f'saves/{self.game.world.name}/{pa}')}")
					p = shutil.copytree(p, path.join(GAMEDIR, f"saves/{self.game.world.name}/{pa}"))
				except FileExistsError:
					p = path.join(GAMEDIR, f"saves/{self.game.world.name}/{kwargs['path']}")
				print(f"p: {p}")
				self.game.world = World(p, self.game)
				self.game.world.load()
			except NotADirectoryError:
				print(f"Could not open map: {kwargs['path']}")

	def run(self):
		while self.running:
			inp = sys.stdin.readline()
			s = inp.split()
			# TODO: Run methods from string without if-chain
			if s[0] == "give":
				try:
					self.give(item=s[1], quantity=s[2])
				except IndexError:
					self.give(item=s[1])
				continue
			elif s[0] == "spawn":
				try:
					self.spawn(x=s[1], y=s[2], enemy=s[3])
				except IndexError:
					if len(s) == 2:
						self.spawn(x=s[1], y=s[2])
					self.game.spawner.spawnEvent()
				continue
			elif s[0] == "debug":
				try:
					if s[1] == "pos" or s[1] == "position":
						print(self.game.player.pos)
					elif s[1] == "chunk":
						print(self.game.player.pos / TILESIZE // 16)
					elif s[1] == "ent" or s[1] == "entity":
						if s[2] == "pos" or s[2] == "position":
							for ent in self.game.world.entities:
								print(ent.pos)
				except IndexError:
					print(f"Expected at least 1 argument, got {len(s) - 1} instead")
				continue
			elif s[0] == "setpos":
				self.setpos(x=s[1], y=s[2])
				continue
			elif s[0] == "xp":
				if len(s) < 4:
					self.xp(operation=s[1], amount=s[2])
				else:
					self.xp(operation=s[1], object=s[2], amount=s[3])
				continue
			elif s[0] == "loadmap":
				self.loadmap(path=s[1])
				continue

			print(f"Could not find command {s[0]}. Please check for correct spelling")

	def kill(self):
		self.running = False
