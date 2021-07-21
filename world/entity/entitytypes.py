from enum import Enum

import pygame

from core.assets.assets import Assets
from world.entity.entitytype import EntityType


class EntityTypes(Enum):
	PLAYER = EntityType("Player", "player1", 0)
	ENEMYTEST = EntityType("EnemyTest", "mage3", 1)

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
	def load():
		for ent in EntityTypes:
			if ent.value.texturePath is not None:
				ent.value.image = pygame.transform.scale(
					Assets[ent.value.texturePath.upper()].value.image, (64, 64))
				ent.value.rect = ent.value.image.get_rect()
