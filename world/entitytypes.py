from enum import Enum

import pygame

import assets
from world.entitytype import EntityType
from sprites import EnemyStandard


class EntityTypes(Enum):
	ENEMYTEST = EntityType("EnemyTest", "mage3", 0)

	@staticmethod
	def getEntity(iden):
		"""
		:param int iden: the identifier of the entity type
		:return: Returns entity or None
		:rtype: Entity
		"""
		for ent in EntityTypes:
			if ent.value.id == iden:
				return ent.value
		return None

	@staticmethod
	def load(game):
		for ent in EntityTypes:
			if ent.value.texturePath is not None:
				ent.value.image = pygame.transform.scale(
					assets.get_asset_from_name(game.graphics, ent.value.texturePath).image, (64, 64))
				ent.value.rect = ent.value.image.get_rect()
