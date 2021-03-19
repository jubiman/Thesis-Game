import pygame
from os import path


# Static methods

# Get assets from coordinates, returns the asset object or None if the asset was not found
def get_asset_from_loc(assets, loc):
	for asset in assets:
		if asset.loc == loc:
			return asset
	return None


def get_asset_from_name(assets, name):
	for asset in assets:
		if asset.name == name:
			return asset
	return None


# Populate induvidual assets in a tilesheet (currently hardcoded). Returns a list with Asset objects
def populate_assets():
	# Define list with image chunks
	assets = []
	# Open the tilesheet
	# colored_packed.png is 16x16, currently is hardcoded to this file
	sheet = pygame.image.load(path.join(path.dirname(__file__), 'assets/visual/Tilesheet/colored_transparent_packed.png'))
	# index = 0  # is used to know how many iterations we have done (i*22+j = index)
	for i in range(48):
		for j in range(22):
			loc = (16*i, 16*j)
			# assets.append(sheet.subsurface(pygame.Rect(loc, 16)))
			# TODO: fix this fucking code lol
			assets.append(Asset(get_name(i*22+j), sheet.subsurface(pygame.Rect(loc, (16, 16))), i*22+j, loc))
			# index += 1
	# Debugging:
	for asset in assets:
		print(f"Loaded asset: {asset.name}, {asset.id}, {asset.loc}")
	return assets


# Returns name of asset
def get_name(index):
	# A python switch case
	# TODO: fully populate names (only 1056 lol)
	switch = {
		0: "empty",
		1: "stone1",
		2: "stone2",
		3: "stone3",
		4: "stone4",
		5: "grass1",
		6: "grass2",
		7: "grass3",
		394: "wall1",
		550: "player1"
	}
	return switch.get(index, "unkown")


class Asset:
	def __init__(self, name, img, ident=-1, loc=(-1, -1)):
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
		for asset in self.assets:
			if asset.loc == loc:
				return asset
		return None
