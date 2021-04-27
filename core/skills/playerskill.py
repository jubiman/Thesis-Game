from core.skills.skillbase import Skillbase


class Playerskill(Skillbase):
	def __init__(self, displayName, texturePath, iden, level, sp, spn, spf):
		"""
		:param str displayName: The name of the skill
		:param str texturePath: The assetname of the skill
		:param int iden: The ID of the skill
		:param int level: The level of the skill
		:param int sp: The amount of skillpoints in the skill
		:param int spn: The skillpoints needed for levelup
		:param str spf: The sp formula for level ups
		"""
		super().__init__(displayName, iden, level, sp, spn, spf)
		self.texturePath = texturePath
		self.image = None
		self.rect = None
