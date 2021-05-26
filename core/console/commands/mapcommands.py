from os import path

import shutil
from settings import GAMEDIR
from world.world import World
from core.console.console import Console
from core.console.consolehelper import ConsoleHelper


class CommandsMap:
	class LoadMap:
		names = ["loadmap", "mapload"]

		@staticmethod
		def loadmap(*args, **kwargs):
			try:
				p = path.join(GAMEDIR, f"saves/{kwargs['path']}")
				if not path.isdir(p):
					raise NotADirectoryError
				ConsoleHelper.Globals.game.world = World(p, ConsoleHelper.Globals.game)
				ConsoleHelper.Globals.game.world.load()
			except KeyError as key:
				try:
					p = path.join(GAMEDIR, f"saves/{args[0]}")
					if not path.isdir(p):
						raise NotADirectoryError
					ConsoleHelper.Globals.game.world = World(p, ConsoleHelper.Globals.game)
					ConsoleHelper.Globals.game.world.load()
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
											message=f"Copying {p} to {path.join(GAMEDIR, f'saves/{ConsoleHelper.Globals.game.world.name}/{pa}')}.")
							p = shutil.copytree(p, path.join(GAMEDIR, f"saves/{ConsoleHelper.Globals.game.world.name}/{pa}"))
						except FileExistsError:
							p = path.join(GAMEDIR, f"saves/{ConsoleHelper.Globals.game.world.name}/{args[0]}")
						ConsoleHelper.Globals.game.world = World(p, ConsoleHelper.Globals.game)
						ConsoleHelper.Globals.game.world.load()
					except NotADirectoryError:
						Console.error(thread="CONSOLE", message=f"Could not open map: {args[0]}.")
				else:
					Console.error(thread="CONSOLE",
									message=f"Could not get item '{key}', please check your spelling and try again.")
			except NotADirectoryError:
				try:
					p = path.join(GAMEDIR, f"world/dungeon/dungeons/{kwargs['path'].rsplit('/')[-1]}")
					if not path.isdir(p):
						raise NotADirectoryError
					try:
						pa = kwargs['path']
						Console.log(thread="CONSOLE",
									message=f"Copying {p} to {path.join(GAMEDIR, f'saves/{ConsoleHelper.Globals.game.world.name}/{pa}')}.")
						p = shutil.copytree(p, path.join(GAMEDIR, f"saves/{ConsoleHelper.Globals.game.world.name}/{pa}"))
					except FileExistsError:
						p = path.join(GAMEDIR, f"saves/{ConsoleHelper.Globals.game.world.name}/{kwargs['path']}")
					ConsoleHelper.Globals.game.world = World(p, ConsoleHelper.Globals.game)
					ConsoleHelper.Globals.game.world.load()
				except NotADirectoryError:
					Console.error(thread="CONSOLE", message=f"Could not open map: {kwargs['path']}.")

		@staticmethod
		def fetchAutocompleteOptions(command, *args):
			pass
