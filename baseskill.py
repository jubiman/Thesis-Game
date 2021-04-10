import pygame
from pygame.locals import *
from skillbase import *


# (name: str, ID: int, level: int, xpn: int, xp_formula: str)
baseskills = [
	("Woodcutting", 0, 0, 10, "self.xp_needed*2"),
	("Mining", 1, 0, 10, "self.xp_needed+10"),
	("Fishing", 2, 0, 10, "self.xp_needed+10"),
	("Farming", 3, 0, 10, "self.xp_needed+10"),
	("Health", 4, 0, 10, "self.xp_needed+10"),
	("Intelligence", 5, 0, 10, "self.xp_needed+10")
]


class Baseskill(Skillbase):
	def __init__(self, name, iden, level, xp, xpn, xpf):
		"""
		:param str name: The name of the skill
		:param int iden: The ID of the skill
		:param int level: The level of the skill
		:param int xp: The experience points of the skill
		:param int xpn: The experience needed for levelup
		:param str xpf: The xp formula for level ups
		"""
		super().__init__(name, iden, level, xp, xpn, xpf)


# Returns a list of base skills
def init():
	"""
	:return: Returns a list with all player skills
	"""
	tmp = []
	for bs in baseskills:
		# Create new Baseskill(name, id) object
		tmp.append(Baseskill(bs[0], bs[1], bs[2], 0, bs[3], bs[4]))
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
	for bs in blist:
		if bs.id == iden:
			return bs.name
	return None
