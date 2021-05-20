from settings import ANSI_COLORS, DEBUG


class Console:
	@staticmethod
	def log(**kwargs):
		if 'thread' in kwargs:
			print(f"[LOG] ({kwargs['thread']}) {kwargs['message']}\033[0m")
		else:
			print(f"[LOG] (UnkownThread) {kwargs['message']}\033[0m")

	@staticmethod
	def error(**kwargs):
		if 'thread' in kwargs:
			print(f"{ANSI_COLORS['red']}[ERROR] ({kwargs['thread']}) {kwargs['message']}\033[0m")
		else:
			print(f"{ANSI_COLORS['red']}[ERROR] (UnkownThread) {kwargs['message']}\033[0m")

	@staticmethod
	def warning(**kwargs):
		if 'thread' in kwargs:
			print(f"{ANSI_COLORS['red']}[WARNING] ({kwargs['thread']}) {kwargs['message']}\033[0m")
		else:
			print(f"{ANSI_COLORS['red']}[WARNING] (UnkownThread) {kwargs['message']}\033[0m")

	@staticmethod
	def debug(**kwargs):
		if not DEBUG:
			return
		if 'thread' in kwargs:
			print(f"{ANSI_COLORS['green']}[DEBUG] ({kwargs['thread']}) {kwargs['message']}\033[0m")
		else:
			print(f"{ANSI_COLORS['green']}[DEBUG] (UnkownThread) {kwargs['message']}\033[0m")

	@staticmethod
	def event(**kwargs):
		if 'thread' in kwargs:
			print(f"{ANSI_COLORS['yellow']}[EVENT] ({kwargs['thread']}) {kwargs['message']}\033[0m")
		else:
			print(f"{ANSI_COLORS['yellow']}[EVENT] (UnkownThread) {kwargs['message']}\033[0m")