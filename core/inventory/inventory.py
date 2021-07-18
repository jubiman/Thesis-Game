from core.items.items import Items
from core.console.console import Console


class InventoryItem:
	def __init__(self, it, quant=0):
		"""
		:param Item it: The item object to reference to
		:param int quant: The quantity of the item
		"""
		self.item = it
		self.quantity = quant


# TODO: Might change this class for some checks inside code
class InventoryList:
	def __init__(self, size, __ls=None):
		"""
		:param int size: Maximum size of the list
		:param list[InventoryItem] ls: The inventory list
		"""
		if __ls is None:
			__ls = []

		self.max_size = size
		self.__ls = __ls

	def push(self, it):
		"""
		:param InventoryItem it: the item to add to the inventory
		:return: None
		"""
		if len(self.__ls) == self.max_size:
			Console.log("No space in inventory")
			# TODO: Do stuff with no inventory space
			return
		self.__ls.append(it)

	def set(self, value):
		"""
		:param value: New list to set
		:return: None
		"""
		if len(value) > self.max_size:
			self.__ls = value[0:self.max_size]
		else:
			self.__ls = value

	def get(self):
		return self.__ls

	def getSlot(self, slot):
		if slot > len(self.__ls):
			return Items.EMPTY.value
		return self.__ls[slot]

	def swap_item(self):
		pass


# TODO: Create working inventory with items
class Inventory:
	def __init__(self):
		self.inv = InventoryList(27)  # Inventory only has 27 slots
		# slot 0 is bound to 1, so slot 8 is max(9)
		self.slots = InventoryList(7)
		self.slots.set(self.inv.get()[0:6])

		self.selectedslot = 1

		# TODO: Old inventory system we discussed... *sigh*
		# TODO: How one lazy guy can fuck up the entire projects... annoys me
		# self.hands[0] is main hand, hands[1] is offhand
		# self.hands = [InventorySlot(Items.IRON_AXE.value, 1, 1), InventorySlot(Items.EMPTY.value, 2, 1)]

	# for i in range(9):
	# self.slots.append(InventorySlot(item.Item('Axe', 1), 1, 1))
	# self.slots.append(InventorySlot(item.Item('empty', 0), i+1))

	# Method to add items to inventory
	def add_new_item(self, it, quant=0):
		"""
		:param Item it: The item to add
		:param int quant: The quantity to add
		"""
		# Search for item in inventory
		for it2 in self.inv.get():
			if it.displayName.lower() == it2.item.displayName.lower():
				if it2.quantity + quant < it2.item.max_stack:
					it2.quantity += quant
				else:
					# Not enought space in inventory
					# TODO: Drop the rest of the item
					it2.quantity = it2.item.max_stack
				return
		# Make new item
		self.inv.push(InventoryItem(it, quant))


class InventorySlot(InventoryItem):
	def __init__(self, it, slot, quant=0):
		"""
		:param Item it: The item object to reference to
		:param int slot: Item slot in inventory (1-9)
		:param int quant: The quantity of the item to pass through to InventoryItem
		"""
		InventoryItem.__init__(self, it, quant)
		self.slot = slot

	def get_item(self):
		"""
		:return: Returns it's item object
		:rtype: Item
		"""
		return self.item
