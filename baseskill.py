import pygame
from pygame.locals import *

baseskills = [
	("Woodcutting", 0),
	("Mining", 1),
	("Fishing", 2),
	("Farming", 3),
	("Health", 4),
	("Intelligence", 5)
]


class Baseskill:
	def __init__(self, name, iden=-1, level=0, xp=0, xpn=10):
		self.name = name
		self.id = iden
		self.level = level
		self.xp = xp
		self.xp_needed = xpn
		# Does nothing at the moment
		# TODO: do something with a good formula to change needed xp per level per skill
		self.xp_formula = "x = x + 10"


# Returns a list of base skills
def init():
	tmp = []
	for i in range(len(baseskills)):
		# Create new Baseskill(name, id) object
		tmp.append(Baseskill(baseskills[i][0], baseskills[i][1]))
	return tmp


def get_from_name(plist, n):
	for bs in plist:
		if bs.name.lower() == n.lower():
			return bs
	return None


def get_from_id(iden):
	for bs in baseskills:
		if bs[1] == iden:
			return bs
	return None


def get_name_from_id(iden):
	for bs in baseskills:
		if bs[1] == iden:
			return bs[0]
