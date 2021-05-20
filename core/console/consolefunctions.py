import shutil
import sys
from os import path

import pygame.math

from core.items.items import Items
from settings import *
from world.world import World
from core.console.console import Console
from core.errors.exceptions import *
from world.entity.entitytypes import EntityTypes


# TODO: Make new console window for console
# TODO: Make every function compatible with kwargs
# TODO: Change input to query with getch()
class ConsoleFunctions(Console):
	def __init__(self, game):
		self.game = game
		self.running = True
		Console.event(thread="CONSOLE", message="Console initialized.")

	def give(self, *args, **kwargs):
		try:
			it = Items.getItemFromName(kwargs['item'])
			if it is not None:
				self.game.player.inventory.add_new_item(it, 1 if 'quantity' not in kwargs else int(kwargs['quantity']))
				return
			Console.error(thread="CONSOLE",
							message=f"Could not add {kwargs['item']} to inventory, please check your spelling and try again.")
		except KeyError as key:
			try:
				if len(args) == 0:
					raise ArgumentException
				it = Items.getItemFromName(args[0])
				if it is not None:
					self.game.player.inventory.add_new_item(it, 1 if len(args) < 2 else int(args[1]))
					return
				Console.error(thread="CONSOLE",
								message=f"Could not add {args[0]} to inventory, please check your spelling and try again.")
			except ValueError:
				Console.error(thread="CONSOLE", message="Could not convert int to string, please check if you put a valid number.")
			except ArgumentException as ae:
				Console.error(thread="CONSOLE", message=ae)
			else:
				Console.error(thread="CONSOLE", message=f"Could not get item '{key}', please check your spelling and try again.")

	def spawn(self, *args, **kwargs):
		try:
			# TODO: add all enemies with arguments
			en = None if len(args) < 3 and 'enemy' not in kwargs else args[2] if 'enemy' not in kwargs else kwargs['enemy']
			if en:
				try:
					enemy = EntityTypes[en.upper()]
				except KeyError:
					Console.error(thread="CONSOLE", message=f"Could not find enemy {en}.")
					return
			else:
				enemy = None

			if self.game.spawner.spawnEventLoc(float(args[0]), float(args[1]), enemy):
				Console.error(thread="CONSOLE", message=f"Could not spawn an enemy at ({kwargs['x']}, {kwargs['y']}).")
		except KeyError as err:
			# TODO: Placeholder
			print(err)
			print("keyerror")
			self.game.spawner.spawnEvent()
		except ValueError:
			Console.error(thread="CONSOLE", message=f"Could not convert ({args[0]}, {args[1]}) to a position, please try again.")
		except TypeError:
			en = None if len(args) < 3 else args[2] if 'enemy' not in kwargs else kwargs['enemy']
			Console.error(thread="CONSOLE", message=f"Could not find enemy {en}.")

	def setpos(self, *args, **kwargs):
		try:
			self.game.player.pos = pygame.math.Vector2(float(kwargs['x']), float(kwargs['y']))
		except ValueError:
			Console.error(thread="CONSOLE",
							message=f"Could not convert ({kwargs['x']}. {kwargs['y']}) to a valid position, please check your "
									f"values and try again.")
		except KeyError:
			try:
				self.game.player.pos = pygame.math.Vector2(float(args[0]), float(args[1]))
			except ValueError:
				Console.error(thread="CONSOLE", message=f"Could not convert ({args[0]}, {args[1]}) to a valid "
														f"position, please check your values and try again.")
				return
			except IndexError:
				Console.error(thread="CONSOLE", message=f"Expected 2 arguments, got {len(args) + len(kwargs)} instead.")

	def xp(self, *args, **kwargs):
		try:
			if kwargs['operation'] == "give" or kwargs['operation'] == "add":
				try:
					if kwargs['object'].lower() == "p" or kwargs['object'].lower() == "player":
						self.game.player.lvl.xp += int(kwargs['amount'])
					# TODO: Add all induvidual skills (possibly without if chain)
				except ValueError:
					Console.error(thread="CONSOLE", message="Could not convert {kwargs['amount']} to an integer, "
															"please check your values and try again.")
				except KeyError as key:
					Console.error(thread="CONSOLE", message=f"Could not get item '{key}', please check your spelling and try again.")
		except ValueError:
			print(f"Could not convert {kwargs['amount']} to an integer, please check your values and try again.")
		except KeyError:
			try:
				if args[0] == "give" or args[0] == "add":
					try:
						if args[1].lower() == "p" or args[1].lower() == "player":
							self.game.player.lvl.xp += int(args[2])
						# TODO: Add all induvidual skills (possibly without if chain)
					except ValueError:
						Console.error(thread="CONSOLE", message=f"Could not convert {args[2]} to an integer, please check "
															f"your values and try again.")
					except IndexError:
						Console.error(thread="CONSOLE", message=f"Expected 4 arguments, got {len(args)} instead.")
					else:
						self.game.player.check_levels()
			except IndexError:
				Console.error(thread="CONSOLE", message=f"Expected 4 arguments, got {len(args)} instead.")
			# print(f"Expected at least 2 arguments, got {len(kwargs) + len(args)} instead")
		else:
			self.game.player.check_levels()

	def loadmap(self, *args, **kwargs):
		try:
			p = path.join(GAMEDIR, f"saves/{kwargs['path']}")
			if not path.isdir(p):
				raise NotADirectoryError
			self.game.world = World(p, self.game)
			self.game.world.load()
		except KeyError as key:
			try:
				p = path.join(GAMEDIR, f"saves/{args[0]}")
				if not path.isdir(p):
					raise NotADirectoryError
				self.game.world = World(p, self.game)
				self.game.world.load()
			except IndexError:
				Console.error(thread="CONSOLE", message=f"Expected at least 1 argument, got {len(args)} instead.")
			except NotADirectoryError:
				try:
					p = path.join(GAMEDIR, f"world/dungeon/dungeons/{args[0].rsplit('/')[-1]}")
					if not path.isdir(p):
						raise NotADirectoryError
					try:
						pa = args[0]
						Console.debug(thread="CONSOLE",
										message=f"Copying {p} to {path.join(GAMEDIR, f'saves/{self.game.world.name}/{pa}')}.")
						p = shutil.copytree(p, path.join(GAMEDIR, f"saves/{self.game.world.name}/{pa}"))
					except FileExistsError:
						p = path.join(GAMEDIR, f"saves/{self.game.world.name}/{args[0]}")
					self.game.world = World(p, self.game)
					self.game.world.load()
				except NotADirectoryError:
					Console.error(thread="CONSOLE", message=f"Could not open map: {args[0]}.")
			else:
				Console.error(thread="CONSOLE", message=f"Could not get item '{key}', please check your spelling and try again.")
		except NotADirectoryError:
			try:
				p = path.join(GAMEDIR, f"world/dungeon/dungeons/{kwargs['path'].rsplit('/')[-1]}")
				if not path.isdir(p):
					raise NotADirectoryError
				try:
					pa = kwargs['path']
					Console.log(thread="CONSOLE", message=f"Copying {p} to {path.join(GAMEDIR, f'saves/{self.game.world.name}/{pa}')}.")
					p = shutil.copytree(p, path.join(GAMEDIR, f"saves/{self.game.world.name}/{pa}"))
				except FileExistsError:
					p = path.join(GAMEDIR, f"saves/{self.game.world.name}/{kwargs['path']}")
				self.game.world = World(p, self.game)
				self.game.world.load()
			except NotADirectoryError:
				Console.error(thread="CONSOLE", message=f"Could not open map: {kwargs['path']}.")

	def run(self):
		while self.running:
			inp = sys.stdin.readline()
			s = inp.split()
			# Algorithm to divide args and kwargs
			kwargs = {}
			for index, arg in enumerate(s[1:]):
				if '=' in s[index+1].replace(' ', ''):
					kwargs[s[index+1].split("=")[0]] = s[index+1].split("=")[1]
					s.pop(index+1)
			args = s[1:]
			if s[0].lower() in ['error', 'debug', 'event', 'log', 'warning']:
				Console.log(thread="CONSOLE", message=f"The command {s[0]} has been disabled for console use.")
				continue
			try:
				getattr(self, s[0])(*args, **kwargs)
			except AttributeError as att:
				Console.error(thread="CONSOLE", message=f"Could not find command {att}, please check your spelling and try again.")

	def kill(self):
		self.running = False
