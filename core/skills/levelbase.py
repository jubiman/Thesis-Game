class Levelbase:
	def __init__(self, level, xp, xpn, xpf="self.xp_needed+10", game=None):
		"""
		:param int level: The level value
		:param int xp: Current experience/skill points
		:param int xpn: XP/SP needed for levelup
		:param str xpf: The xp formula for level ups
		"""
		self.level = level
		self.xp = xp  # XP could be used for Skill Points!
		self.xp_needed = xpn
		self.xp_formula = xpf
		self.game = game

	def levelup(self, t=""):
		"""
		:param str t: Type of object levelup was called from (player/bs/ps)
		"""
		self.level += 1
		self.xp -= self.xp_needed
		self.xp_needed = eval(self.xp_formula)  # TODO: Make dynamic XP/SP system to have working lvlbase
		if t == "player":
			self.game.player.hp += 10  # TODO: Add more player levelup bonus
