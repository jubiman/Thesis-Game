from random import randint
from typing import Generator

from core.items.item import Item
from core.items.items import Items
from core.skills.baseskills import Baseskills

from core.console.console import Console


class Material:
	def __init__(self, displayName, texturePath, iden, idstring, tools: list[str] = None, xptypes: list[str] = None,
					it_dr: list[tuple[str, float, tuple[int, int]]] = None, sk_mp: list[str] = None):
		"""
		:param displayName: The display name of the material
		:param texturePath: The idstring of the image
		:param iden: The identifier of the material
		:param idstring: The idstring of the material
		:param tools: What tools can break this material (None means unbreakable, otherwise list)
		:param xptypes: What type of xp the block gives
		:param it_dr: The item(s) the material drops, it's chances and the (min, max) base amount it can drop
		:param sk_mp: The skill multipliers (i.e. woodcutting on trees)
		"""
		# TODO: Might change tools to seperate class (item/tool class)
		self.displayName = displayName
		self.texturePath = texturePath
		self.id = iden
		self.idstring = idstring
		self.xptypes = xptypes
		self.tools = tools
		self.image = None
		self.rect = None

		self.item_drops = it_dr
		self.skill_multipliers = sk_mp

	# TODO: Get correct items and use skill multipliers
	def calculateItemDrops(self):
		"""
		:return: Returns a list[tuple[Item, int]] with the Item it drops and the quantity of it
		:rtype: Generator[tuple[Item, int]]
		"""
		for item, chance, amounts in self.item_drops:
			if randint(0, 100) / 100 < chance:  # The item drops
				bs = 1
				ps = 1
				for baseskill in self.skill_multipliers:
					bs += Baseskills[baseskill.upper()].value.improve

				Console.debug(bs)
				amount = int(randint(*amounts) * bs * ps)
				yield Items[item.upper()].value, amount
