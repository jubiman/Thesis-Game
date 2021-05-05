from enum import Enum

import pygame

import assets
from world.entity.material import Material


class Materials(Enum):
	AIR = Material("Air", "empty", 0)
	GRASS = Material("Grass", "grass_0", 1)
	TREE = Material("Tree", "tree_0", 2)
	WALL = Material("Wall", "wall_0", 3)

	@staticmethod
	def getMaterial(iden: int):
		for mat in Materials:
			if mat.value.id == iden:
				return mat.value
		return None

	@staticmethod
	def load(game):
		for mat in Materials:
			if mat.value.texturePath is not None:
				mat.value.image = pygame.transform.scale(
					assets.get_asset_from_name(game.graphics, mat.value.texturePath).image, (64, 64))
				mat.value.rect = mat.value.image.get_rect()
