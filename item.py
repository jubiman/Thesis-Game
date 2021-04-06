import pygame


items = [
	("Empty", 0),
	("Axe", 1),
	("Sword", 2),
	("Wood", 3)
]


# TODO: Create new items, possibly with list
class Item:
	# TODO: add plural name?
	def __init__(self, name, iden=-1):
		self.name = name
		self.id = iden


def populate_items():
	"""
	:return: Returns a list with all items
	"""
	tmp = []
	for it in items:
		tmp.append(Item(it[0], it[1]))
	return tmp


def get_item_from_name(itlist, n):
	"""
	:param list[Item] itlist: list of items to iterate over
	:param str n: The name string
	:return: Returns the Item object on success or None on failure
	"""
	for it in itlist:
		if it.name.lower() == n.lower():
			return it
	return None
