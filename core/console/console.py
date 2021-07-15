from sys import stdout

from settings import ANSI_COLORS, DEBUG


class Console:
	query = ""

	@staticmethod
	def printAutocomplete(message):
		stdout.write(f"\r{message}\n{Console.query}")
		stdout.flush()

	@staticmethod
	def log(message, **kwargs):
		if 'thread' in kwargs:
			stdout.write(f"\r[LOG]\t({kwargs['thread']})\t{message}\n{Console.query}")
		else:
			stdout.write(f"\r[LOG]\t(UnkownThread)\t{message}\n{Console.query}")
		stdout.flush()

	@staticmethod
	def error(message, **kwargs):
		if 'thread' in kwargs:
			stdout.write(f"\r{ANSI_COLORS['red']}[ERROR]\t({kwargs['thread']})\t{message}\033[0m\n"
						 f"{Console.query}")
		else:
			stdout.write(f"\r{ANSI_COLORS['red']}[ERROR]\t(UnkownThread)\t{message}\033[0m\n"
						 f"{Console.query}")
		stdout.flush()

	@staticmethod
	def warning(message, **kwargs):
		if 'thread' in kwargs:
			stdout.write(f"\r{ANSI_COLORS['red']}[WARNING]\t({kwargs['thread']})\t{message}\033[0m\n"
						 f"{Console.query}")
		else:
			stdout.write(f"\r{ANSI_COLORS['red']}[WARNING]\t(UnkownThread)\t{message}\033[0m\n"
						 f"{Console.query}")
		stdout.flush()

	@staticmethod
	def debug(message, **kwargs):
		if not DEBUG:
			return
		if 'thread' in kwargs:
			stdout.write(f"\r{ANSI_COLORS['green']}[DEBUG]\t({kwargs['thread']})\t{message}\033[0m\n"
						 f"{Console.query}")
		else:
			stdout.write(f"\r{ANSI_COLORS['green']}[DEBUG]\t(UnkownThread)\t{message}\033[0m\n"
						 f"{Console.query}")
		stdout.flush()

	@staticmethod
	def event(message, **kwargs):
		if 'thread' in kwargs:
			stdout.write(f"\r{ANSI_COLORS['yellow']}[EVENT]\t({kwargs['thread']})\t{message}\033[0m\n"
						 f"{Console.query}")
		else:
			stdout.write(f"\r{ANSI_COLORS['yellow']}[EVENT]\t(UnkownThread)\t{message}\033[0m\n"
						 f"{Console.query}")
		stdout.flush()
