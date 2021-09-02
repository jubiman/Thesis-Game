import shutil
from os import path

from core.console.console import Console
from core.console.consolehelper import ConsoleHelper
from core.utils.settings import Settings
from world.world import World


class CommandsMap:
	class LoadMap:
		names = ["loadmap", "mapload"]
		parameters: list[list[str]] = [
			["dungeon1"]]  # TODO: load from saved paths (possibly config parser/saves parser)

		@staticmethod
		def execute(*args, **kwargs):
			"""
			:param args: Needs a mapname or path from savesfolder to map
			:param kwargs: Available kwargs: path
			:return: None
			"""
			try:
				p = path.join(Settings.GAMEDIR, f"saves/{kwargs['path']}")
				if not path.isdir(p):
					raise NotADirectoryError
				ConsoleHelper.Globals.game.world = World(p, ConsoleHelper.Globals.game)
				ConsoleHelper.Globals.game.world.load()
			except KeyError as key:
				try:
					p = path.join(Settings.GAMEDIR, f"saves/{args[0]}")
					if not path.isdir(p):
						raise NotADirectoryError
					ConsoleHelper.Globals.game.world = World(p, ConsoleHelper.Globals.game)
					ConsoleHelper.Globals.game.world.load()
				except IndexError:
					Console.error(thread="CONSOLE", message=f"Expected at least 1 argument, got {len(args)} instead.")
				except NotADirectoryError:
					try:
						p = path.join(Settings.GAMEDIR, f"world/dungeon/dungeons/{args[0].rsplit('/')[-1]}")
						if not path.isdir(p):
							raise NotADirectoryError
						try:
							pa = args[0]
							Console.debug(thread="CONSOLE",
										  message=f"Copying {p} to {path.join(Settings.GAMEDIR, f'saves/{ConsoleHelper.Globals.game.world.name}/{pa}')}.")
							p = shutil.copytree(p, path.join(Settings.GAMEDIR,
															 f"saves/{ConsoleHelper.Globals.game.world.name}/{pa}"))
						except FileExistsError:
							p = path.join(Settings.GAMEDIR, f"saves/{ConsoleHelper.Globals.game.world.name}/{args[0]}")
						ConsoleHelper.Globals.game.world = World(p, ConsoleHelper.Globals.game)
						ConsoleHelper.Globals.game.world.load()
					except NotADirectoryError:
						Console.error(thread="CONSOLE", message=f"Could not open map: {args[0]}.")
				else:
					Console.error(thread="CONSOLE",
								  message=f"Could not get item '{key}', please check your spelling and try again.")
			except NotADirectoryError:
				try:
					p = path.join(Settings.GAMEDIR, f"world/dungeon/dungeons/{kwargs['path'].rsplit('/')[-1]}")
					if not path.isdir(p):
						raise NotADirectoryError
					try:
						pa = kwargs['path']
						Console.log(thread="CONSOLE",
									message=f"Copying {p} to {path.join(Settings.GAMEDIR, f'saves/{ConsoleHelper.Globals.game.world.name}/{pa}')}.")
						p = shutil.copytree(p,
											path.join(Settings.GAMEDIR, f"saves/{ConsoleHelper.Globals.game.world.name}/{pa}"))
					except FileExistsError:
						p = path.join(Settings.GAMEDIR, f"saves/{ConsoleHelper.Globals.game.world.name}/{kwargs['path']}")
					ConsoleHelper.Globals.game.world = World(p, ConsoleHelper.Globals.game)
					ConsoleHelper.Globals.game.world.load()
				except NotADirectoryError:
					Console.error(thread="CONSOLE", message=f"Could not open map: {kwargs['path']}.")

		@staticmethod
		def fetchAutocompleteOptions(parameter, *args):
			"""
			:param parameter: The current parameter we are working with
			:param args:
			:return: Yields all possible option or None if not available
			"""
			if len(args) == 1:  # we have an argc value
				for key in CommandsMap.LoadMap.parameters[args[0] - 1]:
					if key.startswith(parameter):
						if key != "":
							yield key
