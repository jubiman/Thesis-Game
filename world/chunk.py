from world.block import Block
from world.entity.enemy import Enemy


class Chunk:
	def __init__(self, blocks: list[list[Block]]):
		self.blocks = blocks
		self.entities = []  # TODO: Maybe delete entities from chunk

	def getBlock(self, x: int, y: int):
		return self.blocks[y][x]

	def setBlock(self, x: int, y: int, block: Block):
		self.blocks[y][x] = block

	def getEntity(self, x: int, y: int):
		return self.entities[y][x]

	def setEntity(self, x: int, y: int, enemy: Enemy):
		self.entities[y][x] = enemy
