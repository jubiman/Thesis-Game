from core.skills.skillbase import Skillbase


class Baseskill(Skillbase):
	def __init__(self, displayName, texturePath, iden, level, xp, xpn, xpf, __improve=0):
		"""
		:param str displayName: The name of the skill
		:param str texturePath: The asset name of the skill
		:param int iden: The ID of the skill
		:param int level: The level of the skill
		:param int xp: The experience points of the skill
		:param int xpn: The experience needed for levelup
		:param str xpf: The xp formula for level ups
		:param float __improve: The amount of times it adds (i.e. 2.5x). By default 0
		"""
		super().__init__(displayName, iden, level, xp, xpn, xpf)
		self.texturePath = texturePath

		self.__improve: float = __improve

		self.image = None
		self.rect = None

	@property
	def improve(self):
		return self.__improve

	@improve.setter
	def improve(self, value):
		self.__improve = value

	def levelup(self):
		# TODO: add max lvl?
		while self.lvl.xp > self.lvl.xp_needed:
			self.lvl.levelup()
			self.improve += .5
