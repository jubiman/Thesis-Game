# TODO: add more items/materials
items = [
	("Empty", 0, 1),

	# Tools
	("Axe", 1, 1),
	("Pickaxe", 2, 1),
	("Hammer", 3, 1),

	# Weapons
	("Sword", 25, 1),
	("Bow", 26, 1),
	("Gun", 27, 1),

	# Materials
	("Wood", 50, 999),
	("Stone", 51, 999),
	("Iron", 52, 999),
	("Sulfur", 53, 999),
	("Copper", 54, 999),
	("Tin", 55, 999),
	("Silver", 56, 999),
	("Coal", 57, 999),
	("Gold", 58, 999),

	# Ores
	("Log", 100, 999),
	("Iron", 101, 999),
	("Sulfur_Ore", 102, 999),
	("Copper_Ore", 102, 999),
	("Tin_Ore", 103, 999),
	("Silver_Ore", 104, 999),
	("Gold_Ore", 105, 999)
]


# TODO: Create new items, possibly with list
class Item:
	# TODO: add plural name?
	def __init__(self, name, iden=-1, max_stack=1):
		"""
		:param str name: The name of the item
		:param int iden: The ID of the item
		:param int max_stack: The maximum amount the player can hold of the item in one slot
		"""
		self.name = name
		self.id = iden
		self.max_stack = max_stack


def populate_items():
	"""
	:return: Returns a list with all items
	"""
	tmp = []
	for it in items:
		tmp.append(Item(it[0], it[1], it[2]))
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
