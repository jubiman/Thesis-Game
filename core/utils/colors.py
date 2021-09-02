from sys import platform


class Colors:
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	DARKGREY = (40, 40, 40)
	LIGHTGREY = (100, 100, 100)
	GREEN = (0, 255, 0)
	RED = (255, 0, 0)
	YELLOW = (255, 255, 0)
	BGCOLOR = DARKGREY

	if platform == "win32":
		ANSI_COLORS = {
			'red': "\033[38;5;124m",
			'green': "\033[38;5;148m",
			'yellow': "\033[38;5;226m"
		}
	else:
		ANSI_COLORS = {
			'red': "\033[38;5;$124m",
			'green': "\033[38;5;$148m",
			'yellow': "\033[38;5;$226m"
		}
