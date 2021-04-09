from os import path

import pygame


# Static methods
def get_asset_from_name(assets, name):
	"""
	:param list[Asset] assets: The list of assets to search through
	:param str name: The name of the asset to find
	:return: Returns Asset on success or None on failure
	"""
	for asset in assets:
		if asset.name == name:
			return asset
	return None


# Populate induvidual assets in a tilesheet (currently hardcoded). Returns a list with Asset objects
# Assets loads collumn per collumn (x -> y)
def populate_assets():
	"""
	Populate induvidual assets in a tilesheet (currently hardcoded). Returns a list with Asset objects.\n
	Assets loads collumn per collumn (x -> y).

	:return: Returns a list of assets
	"""
	# Define list with image chunks
	assets = []
	# Open the tilesheet
	# colored_packed.png is 16x16, currently is hardcoded to this file
	sheet = pygame.image.load(path.join(path.dirname(__file__), 'assets/visual/Tilesheet/colored_transparent_packed.png'))
	# index = 0  # is used to know how many iterations we have done (x*22+y = index)
	for x in range(48):
		for y in range(22):
			# assets.append(Asset(get_name(x*22+y), sheet.subsurface(pygame.Rect((16*x, 16*y), (16, 16))), x*22+y, (16*x, 16*y)))
			assets.append(Asset(get_name(x * 22 + y), sheet.subsurface(pygame.Rect((16 * x, 16 * y), (16, 16)))))
	# Debugging:
	for asset in assets:
		print(f"Loaded asset: {asset.name}")
	return assets


# Returns name of asset
def get_name(index):
	"""
	:param int index: The index (ID) where to look for the name
	:return: Returns name string at the index location on success or "unknown" on failure
	"""
	# A python switch case
	# TODO: fully populate names (only 1056 lol)
	switch = {
		# Column 0
		0: "empty",
		1: "tree1",
		# Column 1
		22: "stone1",
		# Column 2
		44: "stone2",
		# Column 3
		66: "stone3",
		67: "forest",
		# Column 4
		88: "stone4",
		# Column 5
		110: "grass1",
		111: "cactus",
		# Column 6
		132: "grass2",
		# Column 7
		154: "grass3",
		155: "cacti",
		# Column 8
		180: "river",
		181: "water_full_tile",
		# Column 9
		202: "river_bend",
		203: "river_bank",
		# Column 18
		394: "wall1",
		550: "player1",
		# Column 24
		528: "mage1",
		529: "mage2",
		530: "mage3",
		# Column 25
		550: "player1",
		551: "player2",
		552: "player3",
    787: "number0",
		931: "axe"
	}
	return switch.get(index, "unkown")


class Asset:
	def __init__(self, name, img):
		"""
		:param str name: The name identifier of the asset
		:param pygame.surface.Surface img: The image of the asset

		"""
		self.name = name
		self.image = img
