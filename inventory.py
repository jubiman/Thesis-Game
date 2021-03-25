import pygame
from pygame.locals import *
import item


# TODO: Create working inventory with items
class Inventory:
	def __init__(self):
		self.inv = []  # Quit item to test out breaking of trees
		self.slots = []
		for i in range(9):
			self.slots.append(InventorySlot(item.Item('axe', 1), i+1))
			# self.slots.append(InventorySlot(item.Item('empty', 0), i+1))


class InventorySlot:
	def __init__(self, it, slot):
		self.item = it
		self.slot = slot

	def get_item(self):
		return self.item
