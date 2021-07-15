from enum import Enum

import pygame

import assets
from world.material.material import Material


class Materials(Enum):
	# TODO: add tools to materials and add all materials
	AIR = Material("Air", "empty", 0, "game:air")
	GRASS = Material("Grass", "grass_0", 1, "game:grass")
	TREE = Material("Tree", "tree_0", 2, "game:tree", tools=['wood_axe', 'iron_axe', 'copper_axe', 'bronze_axe'],
					it_dr=[("wood", 1, (2, 10)), ("thatch", .05, (10, 50))], sk_mp=["woodcutting"])
	WALL = Material("Wall", "wall_part_0_11111111", 3, "game:wall_part_0_11111111")

	@staticmethod
	def getMaterial(iden: int):  # TODO: Order materials by id for faster id searching
		for mat in Materials:
			if mat.value.id == iden:
				return mat.value
		return None

	@staticmethod
	def getMaterialID(iden: int):  # TODO: New way with ID sorted Materials
		return list(Materials)[iden]

	@staticmethod
	def load(game):
		for mat in Materials:
			if mat.value.texturePath is not None:
				mat.value.image = pygame.transform.scale(
					assets.get_asset_from_name(game.graphics, mat.value.texturePath).image, (64, 64))
				mat.value.rect = mat.value.image.get_rect()
