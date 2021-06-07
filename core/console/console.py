from settings import ANSI_COLORS, DEBUG
from sys import stdout


class Console:
	query = ""

	@staticmethod
	def printAutocomplete(**kwargs):
		stdout.write(f"\r{kwargs['message']}\n{Console.query}")
		stdout.flush()

	@staticmethod
	def log(**kwargs):
		if 'thread' in kwargs:
			stdout.write(f"\r[LOG] ({kwargs['thread']}) {kwargs['message']}\n{Console.query}")
		else:
			stdout.write(f"\r[LOG] (UnkownThread) {kwargs['message']}\n{Console.query}")
		stdout.flush()

	@staticmethod
	def error(**kwargs):
		if 'thread' in kwargs:
			stdout.write(f"\r{ANSI_COLORS['red']}[ERROR] ({kwargs['thread']}) {kwargs['message']}\033[0m\n"
							f"{Console.query}")
		else:
			stdout.write(f"\r{ANSI_COLORS['red']}[ERROR] (UnkownThread) {kwargs['message']}\033[0m\n"
							f"{Console.query}")
		stdout.flush()

	@staticmethod
	def warning(**kwargs):
		if 'thread' in kwargs:
			stdout.write(f"\r{ANSI_COLORS['red']}[WARNING] ({kwargs['thread']}) {kwargs['message']}\033[0m\n"
							f"{Console.query}")
		else:
			stdout.write(f"\r{ANSI_COLORS['red']}[WARNING] (UnkownThread) {kwargs['message']}\033[0m\n"
							f"{Console.query}")
		stdout.flush()

	@staticmethod
	def debug(**kwargs):
		if not DEBUG:
			return
		if 'thread' in kwargs:
			stdout.write(f"\r{ANSI_COLORS['green']}[DEBUG] ({kwargs['thread']}) {kwargs['message']}\033[0m\n"
							f"{Console.query}")
		else:
			stdout.write(f"\r{ANSI_COLORS['green']}[DEBUG] (UnkownThread) {kwargs['message']}\033[0m\n"
							f"{Console.query}")
		stdout.flush()

	@staticmethod
	def event(**kwargs):
		if 'thread' in kwargs:
			stdout.write(f"\r{ANSI_COLORS['yellow']}[EVENT] ({kwargs['thread']}) {kwargs['message']}\033[0m\n"
							f"{Console.query}")
		else:
			stdout.write(f"\r{ANSI_COLORS['yellow']}[EVENT] (UnkownThread) {kwargs['message']}\033[0m\n"
							f"{Console.query}")
		stdout.flush()
