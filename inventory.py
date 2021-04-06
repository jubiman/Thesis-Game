import pygame
from pygame.locals import *
import item


class InventoryItem:
	def __init__(self, it, quant=0):
		"""
		:param item.Item it: The item object to reference to
		:param int quant: The quantity of the item
		"""
		self.item = it
		self.quantity = quant


# TODO: Create working inventory with items
class Inventory:
	def __init__(self):
		self.inv = []  # Quit item to test out breaking of trees
		self.slots = []
		# for i in range(9):
		self.slots.append(InventorySlot(item.Item('Axe', 1), 1, 1))
		# self.slots.append(InventorySlot(item.Item('empty', 0), i+1))
		self.inv = self.slots

	# Method to add items to inventory
	def add_new_item(self, it, quant=0):
		"""
		:param item.Item it: The item to add
		:param int quant: The quantity to add
		"""
		# Search for item in inventory
		for it2 in self.inv:
			if it.name.lower() == it2.item.name.lower():
				it2.quantity += quant
				return
		# Make new item
		self.inv.append(InventoryItem(it, quant))


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
		:rtype: item.Item
		"""
		return self.item
