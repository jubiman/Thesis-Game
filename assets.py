import pygame
from os import path


# Static methods

# Get assets from coordinates, returns the asset object or None if the asset was not found
def get_asset_from_loc(assets, loc):
	"""
	:param list[Asset] assets: The list of assets to search through
	:param tuple[int, int] loc: The location of the asset to find
	:return: Returns Asset on success or None on failure
	"""
	for asset in assets:
		if asset.loc == loc:
			return asset
	return None


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
			loc = (16*x, 16*y)
			# assets.append(sheet.subsurface(pygame.Rect(loc, 16)))
			# TODO: fix this fucking code lol
			assets.append(Asset(get_name(x*22+y), sheet.subsurface(pygame.Rect(loc, (16, 16))), x*22+y, loc))
			# index += 1
	# Debugging:
	for asset in assets:
		print(f"Loaded asset: {asset.name}, {asset.id}, {asset.loc}")
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
		0: "empty",
		1: "tree1",
		23: "stone1",
		45: "stone2",
		67: "stone3",
		89: "stone4",
		111: "grass1",
		133: "grass2",
		155: "grass3",
		394: "wall1",
		550: "player1"
	}
	return switch.get(index, "unkown")


class Asset:
	def __init__(self, name, img, ident=-1, loc=(-1, -1)):
		"""
		:param str name: The name identifier of the asset
		:param pygame.surface.Surface img: The image of the asset
		:param int ident: The ID of the asset
		:param tuple[int, int] loc: The location on the tilesheet
		"""
		self.name = name
		self.id = ident
		self.loc = loc
		self.image = img


# TODO: Might remove this class as it seems useless
class Assets:
	def __init__(self):
		# self.assets = populate_asset('assets/visual/Tilesheet/colored_transparent_packed.png')
		self.assets = populate_assets()

	def get_from_loc(self, loc):
		"""
		:param tuple[int, int] loc: the location to get the asset from
		:return: Returns Asset on success or none on failure
		"""
		for asset in self.assets:
			if asset.loc == loc:
				return asset
		return None
