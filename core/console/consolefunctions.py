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
from core.utils.getch import getch


# TODO: Make new console window for console
# TODO: Make every function compatible with kwargs
# TODO: Change input to query with getch()
class ConsoleFunctions(Console):
	def __init__(self, game):
		self.game = game
		self.running = True
		self.query = ""
		# The location where we are typing in the query (CHA = cursor + 4)
		self.cursor = 0
		# TODO: Add dictionary for console commands and auto completion
		self.dict = {}
		# TODO: Add working history
		# History
		self.history = []
		self.histIndex = -1
		self.tmp = ""  # Temp string for query saving before history switching
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

	# Deprecated
	def runOld(self):
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

		raise DeprecationWarning

	def run(self):
		while self.running:
			# TODO: Test on on other operating systems than Windows
			Console.query = "$> " + self.query
			inp = getch()  # Get a single character at a time
			# Console.debug(message=f"inp = {inp}")
			if inp != b"\r":  # If we don't return we don't want to execute the code yet, but add the letter to the query instead
				if inp == b"\x08":  # Backspace
					if len(self.query) > 0:  # If the query is empty we don't want to remove anything
						self.query = self.query[:self.cursor-1] + self.query[self.cursor:]
						self.cursor -= 1
						sys.stdout.write(f"\r\033[K$> {self.query}\033[{self.cursor + 4}G")

				elif inp == b"\xe0":  # First of 2 characters for control keys
					key = getch()
					# Console.debug(message=f"key = {key}")
					if key == b"\x4b":  # Left arrow
						if self.cursor == 0:
							continue
						self.cursor -= 1
						sys.stdout.write("\033[D")

					elif key == b"\x4d":  # Right arrow
						if self.cursor == len(self.query):
							continue
						self.cursor += 1
						sys.stdout.write("\033[C")

					elif key == b"\x48":  # Up arrow
						if self.histIndex == -1:
							self.tmp = self.query
						self.histIndex += 1
						try:
							self.query = self.history[self.histIndex]
						except IndexError:  # Can't go up
							self.histIndex -= 1
							try:
								self.query = self.history[self.histIndex]
							except IndexError:
								self.query = self.tmp
						sys.stdout.write(f"\r\033[K$> {self.query}")
						sys.stdout.flush()
						self.cursor = len(self.query) + 1

					elif key == b"\x50":  # Down arrow
						if self.histIndex == -1:  # We can't go down in history
							continue
						if self.histIndex == 0:  # We have reached the beginning of the history
							self.query = self.tmp  # Reset our query to what we had before the history change
							self.tmp = ""  # Reset the tempory variable
							self.histIndex = -1
							sys.stdout.write(f"\r\033[K$> {self.query}")
							self.cursor = len(self.query) + 1
							continue
						self.histIndex -= 1
						try:
							self.query = self.history[self.histIndex]
						except IndexError:  # Can't go down
							self.histIndex = -1
							self.query = self.tmp
						sys.stdout.write(f"\r\033[K$> {self.query}")
						sys.stdout.flush()
						self.cursor = len(self.query) + 1
					elif key == b"S":  # Delete key
						if len(self.query) > 0:  # If the query is empty we don't want to remove anything
							self.query = self.query[:self.cursor] + self.query[self.cursor + 1:]
							sys.stdout.write(f"\r\033[K$> {self.query}\033[{self.cursor + 4}G")

					continue

				elif inp == b"\t":
					# TODO: Add completion
					pass
				else:
					try:
						self.query = self.query[:self.cursor] + inp.decode("utf-8") + self.query[self.cursor:]
						self.cursor += 1
					except UnicodeDecodeError:
						pass
				sys.stdout.write(f"\r\033[K$> {self.query}\033[{self.cursor + 4}G")
				sys.stdout.flush()
				continue

			# Reset history and CHA
			self.histIndex = -1
			self.cursor = 0

			# If the query is empty, don't execute any code
			if self.query == "":
				continue

			# Add command to history and check for duplicates if setting is disabled
			if self.query not in self.history and bool(self.game.cpc['CONSOLE']['duplicate_history']):
				self.history.insert(0, self.query)

			# Create a new line in the console
			sys.stdout.write("\n")

			# Split arguments into a list ('spawn x y' -> ['spawn', 'x', 'y'])
			s = self.query.split()

			# Reset the query
			self.query = ""

			# Tell console logger to move cursor up
			# CUU (https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences)
			# See also: (https://en.wikipedia.org/wiki/ANSI_escape_code)
			Console.query = "\033[A"

			# Algorithm to divide args and kwargs
			kwargs = {}
			for index, arg in enumerate(s[1:]):
				if '=' in s[index+1].replace(' ', ''):
					kwargs[s[index+1].split("=")[0]] = s[index+1].split("=")[1]
					s.pop(index+1)
			args = s[1:]
			if s[0].lower() in ['error', 'debug', 'event', 'log', 'warning']:  # Skip logging commands
				Console.log(thread="CONSOLE", message=f"The command {s[0]} has been disabled for console use.")
				continue
			try:
				getattr(self, s[0])(*args, **kwargs)  # Run a method from string (name) and give it args and kwargs
			except AttributeError as att:  # Couldn't find the command (method)
				Console.error(thread="CONSOLE", message=f"Could not find command {att}, please check your spelling and try again.")

			sys.stdout.write("\n$> ")
			sys.stdout.flush()

	def kill(self):
		self.running = False
