import logging
import os
from sys import platform

DEBUG = True

logging.basicConfig(level=logging.DEBUG,
					format='[%(levelname)s] (%(threadName)-10s) %(message)s')

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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1536  # 1920  # 1536  # 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 1080  # 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 144
TITLE = "Thesis Game"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

GAMEDIR = os.getcwd()

# Player settings
PLAYERSPEED = 350

CHUNK_UNLOAD_DELAY = 10000
