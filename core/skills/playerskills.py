from enum import Enum
import pygame

import assets
from core.skills.playerskill import Playerskill


class Playerskills(Enum):
	WOODCUTTING = Playerskill("Woodcutting", "skill_woodcutting", 0, 0, 0, 10, "self.xp_needed*2")
	MINING = Playerskill("Mining", "skill_mining", 1, 0, 0, 10, "self.xp_needed+10")
	FISHING = Playerskill("Fishing", "skill_fishing", 2, 0, 0, 10, "self.xp_needed+10")
	FARMING = Playerskill("Farming", "skill_farming", 3, 0, 0, 10, "self.xp_needed+10")
	HEALTH = Playerskill("Health", "skill_health", 4, 0, 0, 10, "self.xp_needed+10")
	INTELLIGENCE = Playerskill("Intelligence", "skill_intelligence", 5, 0, 0, 10, "self.xp_needed+10")

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
					assets.get_asset_from_name(game.graphics, bs.value.texturePath).image, (64, 64))
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
