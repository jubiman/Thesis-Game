from enum import Enum

import pygame

from core.assets import asset
from core.skills.playerskill import Playerskill


class Playerskills(Enum):
	# TODO: make these not a copy of baseskills lol
	WOODCUTTING2 = Playerskill("Woodcutting2", "skill_woodcutting2", 0, 0, 0, 10, "self.xp_needed*2")
	MINING2 = Playerskill("Mining2", "skill_mining2", 1, 0, 0, 10, "self.xp_needed+10")
	FISHING2 = Playerskill("Fishing2", "skill_fishing2", 2, 0, 0, 10, "self.xp_needed+10")
	FARMING2 = Playerskill("Farming2", "skill_farming2", 3, 0, 0, 10, "self.xp_needed+10")
	HEALTH2 = Playerskill("Health2", "skill_health2", 4, 0, 0, 10, "self.xp_needed+10")
	INTELLIGENCE2 = Playerskill("Intelligence2", "skill_intelligence2", 5, 0, 0, 10, "self.xp_needed+10")

	@staticmethod
	def getPlayerskill(iden):
		"""
		:param int iden: the identifier of the entbsy type
		:return: Returns entbsy or None
		:rtype: Entbsy
		"""
		for bs in Playerskills:
			if bs.value.id == iden:
				return bs.value
		return None

	@staticmethod
	def load(game):
		for bs in Playerskills:
			if bs.value.texturePath is not None:
				bs.value.image = pygame.transform.scale(
					asset.get_asset_from_name(game.graphics, bs.value.texturePath).image, (64, 64))
				bs.value.rect = bs.value.image.get_rect()

	@staticmethod
	def getPlayerskillFromName(n):
		"""
		:param str n: The name string
		:return: Returns the bsem object on success or None on failure
		"""
		try:
			return Playerskills[n.upper()].value
		except KeyError:
			return None
