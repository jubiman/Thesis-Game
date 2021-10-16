from core.console.console import Console
from core.items.item import Item
from core.items.items import Items


class _InventoryItem:
	def __init__(self, it: Item, quant=0):
		"""
		:param Item it: The item object to reference to
		:param int quant: The quantity of the item
		"""
		self.item = it
		self.quantity = quant

	def to_json(self):
		return [self.item.id, self.quantity]

	@staticmethod
	def from_json(obj):
		return _InventoryItem(Items.getItem(obj[0]), obj[1])


# TODO: Might change this class for some checks inside code
class _InventoryList:
	def __init__(self, size, __ls=None):
		"""
		:param int size: Maximum size of the list
		:param list[_InventoryItem] ls: The inventory list
		"""
		if __ls is None:
			__ls = []

		self.max_size = size
		self.__ls = __ls

	def push(self, it):
		"""
		:param _InventoryItem it: the item to add to the inventory
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
			return None
		return self.__ls[slot]

	def swap_item(self):
		pass

	def to_json(self):
		return [x.to_json() for x in self.__ls]

	@staticmethod
	def from_json(obj):
		return _InventoryList(len(obj), [_InventoryItem.from_json(x) for x in obj])


# TODO: Create working inventory with items
class Inventory:
	def __init__(self):
		self.__inv = _InventoryList(27)  # Inventory only has 27 slots
		# __slots[0] is bound to 1, so __slots[6] is max (7)
		self.__slots = _InventoryList(7, [_InventoryItem(Items.EMPTY.value, 1), _InventoryItem(Items.EMPTY.value, 1),
										  _InventoryItem(Items.EMPTY.value, 1), _InventoryItem(Items.EMPTY.value, 1),
										  _InventoryItem(Items.EMPTY.value, 1), _InventoryItem(Items.EMPTY.value, 1),
										  _InventoryItem(Items.EMPTY.value, 1)])

		# The currently selected slot saved as 0-based index for __slots array
		self.selectedslot = 0

	# TODO: No Old Inv. System
	# self.hands[0] is main hand, hands[1] is offhand
	# self.hands = [InventorySlot(Items.IRON_AXE.value, 1, 1), InventorySlot(_InventoryItem(Items.EMPTY.value, 1), 2, 1)]

	# for i in range(9):
	# self.slots.append(InventorySlot(item.Item('Axe', 1), 1, 1))
	# self.slots.append(InventorySlot(item.Item('empty', 0), i+1))

	def to_json(self):
		return [self.__inv.to_json(), self.__slots.to_json(), self.selectedslot]

	@staticmethod
	def from_json(obj):
		inv = Inventory()
		inv.__inv = _InventoryList.from_json(obj[0])
		inv.__slots = _InventoryList.from_json(obj[1])
		inv.selectedslot = obj[2]
		return inv

	# Returns private inventory object
	def get(self):
		return self.__inv.get()

	def getslots(self):
		return self.__slots.get()

	def getSlotsObject(self):
		return self.__slots

	def getSlot(self, slot):
		return self.__slots.getSlot(slot)

	# Method to add items to inventory
	def add_new_item(self, it, quant=1):
		"""
		:param Item it: The item to add
		:param int quant: The quantity to add
		"""
		# Search for item in slots
		for it2 in self.getslots():
			if it.displayName.lower() == it2.item.displayName.lower():
				if it2.quantity + quant < it2.item.max_stack:
					it2.quantity += quant
				else:
					# Not enough space in inventory
					# TODO: Drop the rest of the item
					it2.quantity = it2.item.max_stack
				return

		# Search for item in inventory
		for it2 in self.get():
			if it.displayName.lower() == it2.item.displayName.lower():
				if it2.quantity + quant < it2.item.max_stack:
					it2.quantity += quant
				else:
					# Not enough space in inventory
					# TODO: Drop the rest of the item
					it2.quantity = it2.item.max_stack
				return

		# Make new item
		for i, it2 in enumerate(self.getslots()):
			if it2.item.displayName == Items.EMPTY.value.displayName:
				self.getslots()[i] = _InventoryItem(it, quant)
				return

		self.__inv.push(_InventoryItem(it, quant))
