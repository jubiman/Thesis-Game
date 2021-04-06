class Levelbase:
	def __init__(self, level, xp, xpn):
		"""
		:param int level: The level value
		:param int xp: Current experience/skill points
		:param int xpn: XP/SP needed for levelup
		"""
		self.level = level
		self.xp = xp  # XP could be used for Skill Points!
		self.xp_needed = xpn
		self.xp_formula = "x = x + 10"

	def levelup(self, t=""):
		"""
		:param str t: Type of object levelup was called from (player/bs/ps)
		"""
		self.level += 1
		self.xp = 0
		self.xp_needed += 10  # TODO: Make dynamic XP/SP system to have working lvlbase
		if t == "player":
			pass