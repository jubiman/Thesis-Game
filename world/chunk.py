from world.block import Block


class Chunk:

	def __init__(self, blocks: list[list[Block]]):
		self.blocks = blocks

	def getBlock(self, x: int, y: int):
		return self.blocks[y][x]

	def setBlock(self, x: int, y: int, block: Block):
		self.blocks[y][x] = block
