import pygame
from pygame.locals import *
from skillbase import *


# (name: str, ID: int, level: int, spn: int, spf: str)
playerskills = [
	("Strenth", 0, 0, 1, "self.xp_needed+10"),  # Melee damage
	("Dexterity", 1, 0, 1, "self.xp_needed+10"),  # Crit chance (mostly with ranged weapons)
	("Physical Resistance", 2, 0, 1, "self.xp_needed+10"),  # Resistance from physical attack forms
	("Magical Resistance", 3, 0, 1, "self.xp_needed+10"),  # Resistance from magical attack forms
	("Agility", 4, 0, 1, "self.xp_needed+10"),  # Movement speed
	("Dodge", 5, 0, 1, "self.xp_needed+10"),  # Chance to dogde an attack (negates all damage)
	("Vitality", 6, 0, 1, "self.xp_needed+10")  # Maximum hit points increase
]


class Playerskill(Skillbase):
	def __init__(self, name, iden, level, spn, spf):
		"""
		:param str name: The name of the skill
		:param int iden: The ID of the skill
		:param int level: The level of the skill
		:param int spn: The skillpoints needed for levelup
		:param str spf: The sp formula for level ups
		"""
		super().__init__(name, iden, level, 0, spn, spf)


# Returns a list of player skills
def init():
	"""
	:return: Returns a list with all player skills
	"""
	tmp = []
	for ps in playerskills:
		# Create new Baseskill(name, id) object
		tmp.append(Playerskill(ps[0], ps[1], ps[2], ps[3], ps[4]))
	return tmp
