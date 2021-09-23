from os import getcwd


class Settings:
	DEBUG = True

	# Game settings
	class Game:
		WIDTH = 1536  # 1920  # 1536  # 1024   # 16 * 64 or 32 * 32 or 64 * 16
		HEIGHT = 768  # 1080  # 768  # 16 * 48 or 32 * 24 or 64 * 12
		FPS = 144
		TITLE = "Thesis Game"
		TILESIZE = 64

	GAMEDIR = getcwd()

	class Player:
		# Player settings
		PLAYERSPEED = 350

	class World:
		CHUNK_UNLOAD_DELAY = 10000
