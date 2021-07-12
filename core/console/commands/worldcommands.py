import pygame
from core.console.console import Console
from core.console.consolehelper import ConsoleHelper
from world.entity.entitytypes import EntityTypes
from world.material.materials import Materials
from world.block import Block


class CommandsWorld:
	class SetPos:
		names = ["setpos"]
		parameters: list[list[str]] = [[""]]

		@staticmethod
		def execute(*args, **kwargs):
			try:
				ConsoleHelper.Globals.game.player.pos = pygame.math.Vector2(float(kwargs['x']), float(kwargs['y']))
			except ValueError:
				Console.error(thread="CONSOLE",
								message=f"Could not convert ({kwargs['x']}. {kwargs['y']}) to a valid position, please check your "
										f"values and try again.")
			except KeyError:
				try:
					ConsoleHelper.Globals.game.player.pos = pygame.math.Vector2(float(args[0]), float(args[1]))
				except ValueError:
					Console.error(thread="CONSOLE", message=f"Could not convert ({args[0]}, {args[1]}) to a valid "
															f"position, please check your values and try again.")
					return
				except IndexError:
					Console.error(thread="CONSOLE",
									message=f"Expected 2 arguments, got {len(args) + len(kwargs)} instead.")

		@staticmethod
		def fetchAutocompleteOptions(command, *args):
			pass

	class Spawn:
		names = ["spawn", "enemy"]
		parameters: list[list[str]] = [[""], [""], [""]]  # TODO: add all enemies to last parameter

		@staticmethod
		def execute(*args, **kwargs):
			try:
				# TODO: add all enemies with arguments
				en = None if len(args) < 3 and 'enemy' not in kwargs else args[2] if 'enemy' not in kwargs else kwargs[
					'enemy']
				if en:
					try:
						enemy = EntityTypes[en.upper()]
					except KeyError:
						Console.error(thread="CONSOLE", message=f"Could not find enemy {en}.")
						return
				else:
					enemy = None

				if ConsoleHelper.Globals.game.spawner.spawnEventLoc(float(args[0]), float(args[1]), enemy):
					Console.error(thread="CONSOLE",
									message=f"Could not spawn an enemy at ({kwargs['x']}, {kwargs['y']}).")
			except KeyError as err:
				# TODO: Placeholder
				print(err)
				print("keyerror")
				ConsoleHelper.Globals.game.spawner.spawnEvent()
			except ValueError:
				Console.error(thread="CONSOLE",
								message=f"Could not convert ({args[0]}, {args[1]}) to a position, please try again.")
			except TypeError:
				en = None if len(args) < 3 else args[2] if 'enemy' not in kwargs else kwargs['enemy']
				Console.error(thread="CONSOLE", message=f"Could not find enemy {en}.")

		@staticmethod
		def fetchAutocompleteOptions(command, *args):
			pass

	class SetBlock:
		names = ["setblock", "set"]
		parameters: list[int, int, list[str]] = [int, int, []]  # TODO: add all blocks to last parameter
		# setblock x y block

		@staticmethod
		def execute(*args, **kwargs):
			try:
				blockstr = kwargs['block'][kwargs['block'].rfind(':')+1].upper()
				try:
					ConsoleHelper.Globals.game.world.setBlock(int(kwargs['x']), int(kwargs['y']), Block(Materials[blockstr].value))
				except KeyError:
					Console.error(thread="CONSOLE",
									message=f"Couldn't find block {args[2]}. Please check your spelling and try again.")
			except KeyError:
				if len(args) < 3:
					return Console.error(thread="CONSOLE", message=f"Expected 3 arguments, got {len(args)} instead.")
				loc = args[2].rfind(':')+1
				if loc > 0:
					blockstr = args[2][loc:].upper()
				else:
					blockstr = args[2].upper()
				try:
					ConsoleHelper.Globals.game.world.setBlock(int(args[0]), int(args[1]), Block(Materials[blockstr].value))
				except KeyError:
					Console.error(thread="CONSOLE",
									message=f"Couldn't find block {args[2]}. Please check your spelling and try again.")

		@staticmethod
		def fetchAutocompleteOptions(parameter, *args):  # TODO: Might change *args for argc/completely remove it for eff
			"""
			:param parameter: The current parameter we are working with
			:param args:
			:return: Yields all possible option or None if not available
			"""
			if len(args) > 0:  # we have an argc value
				if args[0] == 3 and parameter == "" or parameter in "game:":
					for param in CommandsWorld.SetBlock.parameters[2]:
						yield param
					return
				for key in CommandsWorld.SetBlock.parameters[args[0] - 1]:
					if key.startswith(parameter):
						if key != "":
							yield key
