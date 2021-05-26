import pygame
from core.console.console import Console
from core.console.consolehelper import ConsoleHelper
from world.entity.entitytypes import EntityTypes


class CommandsWorld:
	class SetPos:
		names = ["setpos"]

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
