from enum import Enum

import pygame

import assets
from core.skills.baseskill import Baseskill


class Baseskills(Enum):
	WOODCUTTING = Baseskill("Woodcutting", "skill_woodcutting", 0, 0, 0, 10, "self.xp_needed*2")
	MINING = Baseskill("Mining", "skill_mining", 1, 0, 0, 10, "self.xp_needed+10")
	FISHING = Baseskill("Fishing", "skill_fishing", 2, 0, 0, 10, "self.xp_needed+10")
	FARMING = Baseskill("Farming", "skill_farming", 3, 0, 0, 10, "self.xp_needed+10")
	HEALTH = Baseskill("Health", "skill_health", 4, 0, 0, 10, "self.xp_needed+10")
	INTELLIGENCE = Baseskill("Intelligence", "skill_intelligence", 5, 0, 0, 10, "self.xp_needed+10")

	@staticmethod
	def getBaseskill(iden):
		"""
		:param int iden: the identifier of the entbsy type
		:return: Returns Baseskill or None
		:rtype: Baseskill
		"""
		if iden > len(list(Baseskills)) - 1:
			return None
		return list(Baseskills)[iden]

	@staticmethod
	def load(game):
		for bs in Baseskills:
			if bs.value.texturePath is not None:
				bs.value.image = pygame.transform.scale(
					assets.get_asset_from_name(game.graphics, bs.value.texturePath).image, (64, 64))
				bs.value.rect = bs.value.image.get_rect()

	@staticmethod
	def getBaseskillFromName(n):
		"""
		:param str n: The name string
		:return: Returns the bsem object on success or None on failure
		"""
		try:
			return Baseskills[n.upper()].value
		except KeyError:
			return None
