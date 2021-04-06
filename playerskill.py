import pygame
from pygame.locals import *
from skillbase import *


# (Name, ID, level, spn)
playerskills = [
	("Strenth", 0, 0, 1),
	("Dexterity", 1, 0, 1),
	("Physical Resistance", 2, 0,1 ),
	("Magic Resistance", 3, 0, 1),
	("Agility", 4, 0, 1),
	("Dodge", 5, 0, 1)
]


class Playerskill(Skillbase):
	def __init__(self, name, iden, level, spn=10):
		"""
		:param str name: The name of the skill
		:param int iden: The ID of the skill
		:param int level: The level of the skill
		:param int spn: The skillpoints needed for levelup
		"""
		Skillbase.__init__(self, name, iden, level, 0, spn)
		# Does nothing at the moment
		# TODO: do something with a good formula to change needed sp per level per skill
		self.sp_formula = "x = x + 10"


# Returns a list of player skills
def init():
	"""
	:return: Returns a list with all player skills
	"""
	tmp = []
	for i in range(len(playerskills)):
		# Create new Baseskill(name, id) object
		tmp.append(Playerskill(playerskills[i][0], playerskills[i][1], playerskills[i][2], playerskills[i][3]))
	return tmp
