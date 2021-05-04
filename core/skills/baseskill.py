from core.skills.skillbase import Skillbase


class Baseskill(Skillbase):
	def __init__(self, displayName, texturePath, iden, level, xp, xpn, xpf):
		"""
		:param str displayName: The name of the skill
		:param str texturePath: The assetname of the skill
		:param int iden: The ID of the skill
		:param int level: The level of the skill
		:param int xp: The experience points of the skill
		:param int xpn: The experience needed for levelup
		:param str xpf: The xp formula for level ups
		"""
		super().__init__(displayName, iden, level, xp, xpn, xpf)
		self.texturePath = texturePath
		self.image = None
		self.rect = None
