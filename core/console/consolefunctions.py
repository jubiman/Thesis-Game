import shutil
import sys
import inspect
from os import path

import pygame.math

from settings import *
from world.world import World
from core.console.console import Console
from world.entity.entitytypes import EntityTypes
from core.utils.getch import getch
from core.console.consolehelper import ConsoleHelper
from core.console.commands.worldcommands import CommandsWorld
from core.console.commands.playercommands import CommandsPlayer
from core.console.commands.mapcommands import CommandsMap
from core.utils.timer import Timer


# TODO: Make every function compatible with kwargs
class ConsoleFunctions(Console):
	Commands = {}

	def __init__(self, game):
		Timer.start('ConsoleInit')
		# Parse game instance for functions to use
		ConsoleHelper.Globals.game = game

		# Make sure the console can run
		self.running = True

		# Initialize basic variables
		self.query = ""
		# The location where we are typing in the query (CHA = cursor + 4)
		self.cursor = 0
		# History
		self.history = []
		self.histIndex = -1
		self.tmp = ""  # Temp string for query saving before history switching

		# Create commands dictionary for autocompletion and make commands runnable
		self.populateCommandRegistry()

		# Log that the console finished initializing
		dura = Timer.stop('ConsoleInit')
		Console.event(thread="CONSOLE", message=f"Console finished initializing in {dura} seconds.")

	# @staticmethod
	def populateCommandRegistry(self):
		for name, obj in inspect.getmembers(CommandsWorld):
			if inspect.isclass(obj) and name != "__class__":
				for n in obj.names:
					self.Commands[n] = obj
					# Console.debug(message=f"Added {n} to console")
		for name, obj in inspect.getmembers(CommandsPlayer):
			if inspect.isclass(obj) and name != "__class__":
				for n in obj.names:
					self.Commands[n] = obj
					# Console.debug(message=f"Added {n} to console")
		for name, obj in inspect.getmembers(CommandsMap):
			if inspect.isclass(obj) and name != "__class__":
				for n in obj.names:
					self.Commands[n] = obj
					# Console.debug(message=f"Added {n} to console")

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

	@staticmethod
	def executeInternal(command, *args, **kwargs):
		# TODO: maybe output stuff
		try:
			cmd = ConsoleFunctions.Commands[command]
		except KeyError:
			Console.error(thread="CONSOLE", message=f"Could not find command {command}, please check your spelling and try again.")
		else:
			cmd.execute(*args, **kwargs)

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
			if bool(ConsoleHelper.Globals.game.cpc['CONSOLE']['duplicate_history']) and self.query not in self.history:
				self.history.insert(0, self.query)

			# Create a new line in the console
			sys.stdout.write("\n")

			# Split arguments into a list ('spawn x y' -> ['spawn', 'x', 'y'])
			s = self.query.split()

			# Remove the command so we can parse the arguments
			argStr = ""
			for ar in s[1:]:
				argStr += ar + " "

			# Algorithm to divide args and kwargs
			args, kwargs = ConsoleHelper.tokeniseString(argStr[:-1])

			# Reset the query
			self.query = ""

			# Tell console logger to move cursor up
			# CUU (https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences)
			# See also: (https://en.wikipedia.org/wiki/ANSI_escape_code)
			Console.query = "\033[A"

			# Skip commands error debug event log and warning
			# TODO: might remove as we no longer use getattr() in this class
			if s[0].lower() in ['error', 'debug', 'event', 'log', 'warning']:  # Skip logging commands
				Console.log(thread="CONSOLE", message=f"The command {s[0]} has been disabled for console use.")
				continue

			# Execute the command with arguments
			self.executeInternal(s[0], *args, **kwargs)


			sys.stdout.write("\n$> ")
			sys.stdout.flush()

	def kill(self):
		self.running = False
