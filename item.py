import pygame


items = [
	("empty", 0),
	("axe", 1),
	("sword", 2)
]


# TODO: Create new items, possibly with list
class Item:
	# TODO: add plural name?
	def __init__(self, name, iden=-1):
		self.name = name
		self.id = iden


def populate_items():
	tmp = []
	for it in items:
		tmp.append(Item(it[0], it[1]))
	return tmp


def get_item_from_name(itlist, n):
	for it in itlist:
		if it.name.lower() == n.lower():
			return it
	return None
