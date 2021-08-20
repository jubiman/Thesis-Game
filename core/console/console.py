from sys import stdout
from traceback import print_exc

from settings import ANSI_COLORS, DEBUG


class Console:
	query = "$> "

	@staticmethod
	def printAutocomplete(message):
		stdout.write(f"\033[2K\r{message}\n{Console.query}")
		stdout.flush()

	@staticmethod
	def log(message, thread="UNKOWN"):
		stdout.write(f"\033[2K\r[LOG]\t({thread})\t{message}\n{Console.query}")
		stdout.flush()

	@staticmethod
	def error(message, thread="UNKOWN"):
		stdout.write(f"\033[2K\r{ANSI_COLORS['red']}[ERROR]\t({thread})\t{message}\033[0m\n{Console.query}")
		stdout.flush()

	@staticmethod
	def traceback(thread="CONSOLE"):
		stdout.write(f"\033[2K\r{ANSI_COLORS['red']}[ERROR]\t({thread})\t")
		print_exc(chain=False)
		stdout.write(f"\033[0m$> ")
		stdout.flush()

	@staticmethod
	def warning(message, thread="UNKOWN"):
		stdout.write(f"\033[2K\r{ANSI_COLORS['red']}[WARNING]\t({thread})\t{message}\033[0m\n{Console.query}")
		stdout.flush()

	@staticmethod
	def debug(message, thread="UNKOWN"):
		if not DEBUG:
			return
		stdout.write(f"\033[2K\r{ANSI_COLORS['green']}[DEBUG]\t({thread})\t{message}\033[0m\n{Console.query}")
		stdout.flush()

	@staticmethod
	def event(message, thread="UNKOWN"):
		stdout.write(f"\033[2K\r{ANSI_COLORS['yellow']}[EVENT]\t({thread})\t{message}\033[0m\n{Console.query}")
		stdout.flush()
