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
	sheet = pygame.image.load(
		path.join(path.dirname(__file__), 'assets/visual/Tilesheet/colored_transparent_packed.png'))
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
		1: "tree_0",
		2: "fern",
		3: "fence_low",
		5: "rails_1010",
		7: "directions_sign",
		9: "door_blue_locked",
		10: "lock_blue_locked",
		11: "button_blue_locked",
		12: "chimney",
		13: "brick_white",
		14: "gravestone_0",
		15: "skull_human",
		19: "house_red_0",
		20: "house_red_2",
		21: "house_white_0",
		# Column 1
		22: "path_stone_0",
		23: "tree_1",
		24: "plant_0",
		25: "fence",
		# Column 2
		44: "path_stone_1",
		45: "tree_2",
		46: "plant_1",
		47: "fence_high",
		48: "fence_white_broken",
		# Column 3
		66: "path_stone_2",
		67: "forest_0",
		68: "forest_1",
		69: "fence_red_gate",
		70: "fence_white_gate",
		71: "rails_1111",
		72: "stairs_red_1",
		73: "bookshelf",
		74: "cart_half",
		75: "door_red",
		81: "candle_red",
		85: "castle_white_1",
		86: "school",
		87: "apartment",

		# Column 4
		88: "path_stone_3",
		89: "tree_3",
		# Column 5
		110: "grass_0",
		111: "cactus",
		# Column 6
		132: "grass_1",
		# Column 7
		154: "grass_2",
		155: "cacti",
		# Column 8
		# water_{upleft}{up}{upright}{right}{bottomright}{bottom}{bottomleft}{left}
		180: "water_01000100",
		181: "water_11111111",
		# Column 9
		202: "water_00010100",
		203: "water_01111100",
		# Column 10
		224: "water_01010100",
		225: "water_00011100",
		# Column 11
		246: "water_01010101",
		247: "water_01111111",
		# Column 12
		268: "water_00000100",
		267: "water_01000100",
		# Column 18
		394: "wall_0",
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
