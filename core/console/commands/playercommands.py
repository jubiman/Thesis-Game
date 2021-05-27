from core.items.items import Items
from core.console.console import Console
from core.console.consolehelper import ConsoleHelper
from core.utils.errors.exceptions import *


class CommandsPlayer:
	class Give:
		names = ["give", "item"]

		@staticmethod
		def execute(*args, **kwargs):
			try:
				it = Items.getItemFromName(kwargs['item'])
				if it is not None:
					ConsoleHelper.Globals.game.player.inventory.add_new_item(it,
															1 if 'quantity' not in kwargs else int(kwargs['quantity']))
					return
				Console.error(thread="CONSOLE",
								message=f"Could not add {kwargs['item']} to inventory, please check your spelling and try again.")
			except KeyError as key:
				try:
					if len(args) == 0:
						raise ArgumentException
					it = Items.getItemFromName(args[0])
					if it is not None:
						ConsoleHelper.Globals.game.player.inventory.add_new_item(it, 1 if len(args) < 2 else int(args[1]))
						return
					Console.error(thread="CONSOLE",
									message=f"Could not add {args[0]} to inventory, please check your spelling and try again.")
				except ValueError:
					Console.error(thread="CONSOLE",
									message="Could not convert int to string, please check if you put a valid number.")
				except ArgumentException as ae:
					Console.error(thread="CONSOLE", message=ae)
				else:
					Console.error(thread="CONSOLE",
									message=f"Could not get item '{key}', please check your spelling and try again.")

		@staticmethod
		def fetchAutocompleteOptions(command, *args):
			pass

	class XP:
		names = ["xp", "exp"]

		@staticmethod
		def execute(*args, **kwargs):
			try:
				if kwargs['operation'] == "give" or kwargs['operation'] == "add":
					try:
						if kwargs['object'].lower() == "p" or kwargs['object'].lower() == "player":
							ConsoleHelper.Globals.game.player.lvl.xp += int(kwargs['amount'])
					# TODO: Add all induvidual skills (possibly without if chain)
					except ValueError:
						Console.error(thread="CONSOLE", message="Could not convert {kwargs['amount']} to an integer, "
																"please check your values and try again.")
					except KeyError as key:
						Console.error(thread="CONSOLE",
										message=f"Could not get item '{key}', please check your spelling and try again.")
			except ValueError:
				print(f"Could not convert {kwargs['amount']} to an integer, please check your values and try again.")
			except KeyError:
				try:
					if args[0] == "give" or args[0] == "add":
						try:
							if args[1].lower() == "p" or args[1].lower() == "player":
								ConsoleHelper.Globals.game.player.lvl.xp += int(args[2])
						# TODO: Add all induvidual skills (possibly without if chain)
						except ValueError:
							Console.error(thread="CONSOLE",
											message=f"Could not convert {args[2]} to an integer, please check "
													f"your values and try again.")
						except IndexError:
							Console.error(thread="CONSOLE", message=f"Expected 4 arguments, got {len(args)} instead.")
						else:
							ConsoleHelper.Globals.game.player.check_levels()
				except IndexError:
					Console.error(thread="CONSOLE", message=f"Expected 4 arguments, got {len(args)} instead.")
			# print(f"Expected at least 2 arguments, got {len(kwargs) + len(args)} instead")
			else:
				ConsoleHelper.Globals.game.player.check_levels()

		@staticmethod
		def fetchAutocompleteOptions(command, *args):
			pass
