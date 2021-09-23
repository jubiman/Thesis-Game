from world.block import Block
from world.entity.entities.enemy import Enemy


class Chunk:
	def __init__(self, blocks: list[list[Block]]):
		self.blocks = blocks
		self.entities = []  # TODO: Maybe delete entities from chunk

	def is_empty(self) -> bool:
		return any(self.blocks) and sum(sum(y.material.id for y in x) for x in self.blocks) == 0

	def getBlock(self, x: int, y: int):
		return self.blocks[y][x]

	def setBlock(self, x: int, y: int, block: Block):
		self.blocks[y][x] = block

	def getEntity(self, x: int, y: int):
		return self.entities[y][x]

	def setEntity(self, x: int, y: int, enemy: Enemy):
		self.entities[y][x] = enemy
