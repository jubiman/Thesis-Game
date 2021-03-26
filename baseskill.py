import pygame
from pygame.locals import *
from skillbase import *


baseskills = [
	("Woodcutting", 0),
	("Mining", 1),
	("Fishing", 2),
	("Farming", 3),
	("Health", 4),
	("Intelligence", 5)
]


class Baseskill(Skillbase):
	def __init__(self, name, iden=-1, level=0, xp=0, xpn=10):
		"""
		:param str name: The name of the skill
		:param int iden: The ID of the skill
		:param int level: The level of the skill
		:param int xp: The experience points of the skill
		:param int xpn: The experience needed for levelup
		"""
		Skillbase.__init__(self, name, iden, level, xp, xpn)
		# Does nothing at the moment
		# TODO: do something with a good formula to change needed xp per level per skill
		self.xp_formula = "x = x + 10"


# Returns a list of base skills
def init():
	"""
	:return: Returns a list with all player skills
	"""
	tmp = []
	for i in range(len(baseskills)):
		# Create new Baseskill(name, id) object
		tmp.append(Baseskill(baseskills[i][0], baseskills[i][1]))
	return tmp


def get_from_name(blist, n):
	"""
	:param list[Baseskill] blist: The list of baseskills to search through
	:param str n: The name of the Baseskill to find
	:return: Returns Baseskill on success or None on failure
	"""
	for bs in blist:
		if bs.name.lower() == n.lower():
			return bs
	return None


def get_from_id(blist, iden):
	"""
	:param list[Baseskill] blist: The list of baseskills to search through
	:param int iden: The ID of the baseskill to find
	:return: Returns Baseskill on success or None on failure
	"""
	for bs in blist:
		if bs.id == iden:
			return bs
	return None


def get_name_from_id(blist, iden):
	"""
	:param list[Baseskill] blist: The list of baseskills to search through
	:param int iden: The ID of the baseskill to find
	:return: Returns Baseskill on success or None on failure
	:rtype: str | None
	"""
	for bs in baseskills:
		if bs.id == iden:
			return bs.name
	return None
