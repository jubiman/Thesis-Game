from core.console.console import Console
from core.console.consolehelper import ConsoleHelper
from core.items.items import Items
from core.skills.baseskills import Baseskills
from core.skills.playerskills import Playerskills
from core.utils.errors.exceptions import *


class CommandsPlayer:
	class Give:
		names = ["give", "item"]
		parameters: list[list[str]] = [[""]]  # TODO: Get all items in parameters or a pointer to them

		@staticmethod
		def execute(*args, **kwargs):
			try:
				it = Items[(kwargs['item']).upper()].value
				if it is not None:
					ConsoleHelper.Globals.game.player.inventory.add_new_item(it,
																			1 if 'quantity' not in kwargs else int(
																				kwargs['quantity']))
					return
				Console.error(thread="CONSOLE",
								message=f"Could not add {kwargs['item']} to inventory, please check your spelling and try again.")
			except KeyError as key:
				try:
					if len(args) == 0:
						raise ArgumentException
					# TODO: add error handling and more itemname support (id, idstring, itemname)
					it = Items[args[0].upper()].value
					if it is not None:
						ConsoleHelper.Globals.game.player.inventory.add_new_item(it,
																				1 if len(args) < 2 else int(args[1]))
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
		def fetchAutocompleteOptions(parameter, *args):
			"""
			:param parameter: The current parameter we are working with
			:param args:
			:return: Yields all possible option or None if not available
			"""
			if len(args) == 1:  # we have an argc value
				for key in CommandsPlayer.Give.parameters[args[0] - 1]:
					if key.startswith(parameter):
						if key != "":
							yield key

	class XP:
		names = ["xp", "exp"]
		parameters: list[list[str]] = [["give", "add"], [""]]

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
							else:
								try:
									Baseskills[args[1].upper()].value.lvl.xp += int(args[2])
								except KeyError:
									try:
										Playerskills[args[1].upper()].value.lvl.xp += int(args[2])
									except KeyError:
										Console.error(
											f"Could not find skill {args[1]}. Please check your spelling and try again",
											thread="CONSOLE")
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
		def fetchAutocompleteOptions(parameter,
									 *args):  # TODO: Might change *args for argc/completely remove it for eff
			"""
			:param parameter: The current parameter we are working with
			:param args:
			:return: Yields all possible option or None if not available
			"""
			if len(args) == 1:  # we have an argc value
				if args[0] == 1 and parameter == "":
					yield "give"
				for key in CommandsPlayer.XP.parameters[args[0] - 1]:
					if key.startswith(parameter):
						if key != "":
							yield key

	class ShowPos:
		names = ["showpos", "pos"]
		parameters: list[list[str]] = [[]]

		@staticmethod
		def execute(*args, **kwargs):
			Console.log(thread="CONSOLE", message=f"{ConsoleHelper.Globals.game.player.pos}")

		@staticmethod
		def fetchAutocompleteOptions(parameter,
									 *args):  # TODO: Might change *args for argc/completely remove it for eff
			"""
			:param parameter: The current parameter we are working with
			:param args:
			:return: Yields all possible option or None if not available
			"""
			if len(args) == 1:  # we have an argc value
				if args[0] == 1 and parameter == "":
					yield "give"
				for key in CommandsPlayer.ShowPos.parameters[args[0] - 1]:
					if key.startswith(parameter):
						if key != "":
							yield key

	# TODO: Placeholder to set an item on a slot
	class SetSlot:
		names = ["setslot", "slot"]
		parameters: list[int, list[str]] = []

		@staticmethod
		def execute(*args, **kwargs):
			try:
				if len(args) < 2:
					raise ArgumentException
			except ArgumentException as ae:
				Console.error(thread="CONSOLE", message=ae)
				return

			it = Items[args[1].upper()].value
			# ConsoleHelper.Globals.game.player.inventory.slots.get()[int(args[0])] = it
			ConsoleHelper.Globals.game.player.inventory.slots.get()[int(args[0]) - 1] = it

		@staticmethod
		def fetchAutocompleteOptions(parameter, *args):
			pass
