from opensimplex import OpenSimplex

from world.block import Block
from world.chunk import Chunk
from world.materials import Materials


class Generator:

	def __init__(self, seed):
		self.seed = seed
		self.noise = OpenSimplex(seed=seed)
		self.settings = {
			"wallHeight": 0.5
		}

	def getHeight(self, x: int, y: int):
		return (self.noise.noise2d(x, y) + 1) / 2

	def generateChunk(self, x: int, y: int):
		print(f"generating chunk {x},{y}")
		# chunk: Chunk = Chunk([[Block(Materials.GRASS.value if x % 2 == 0 and y % 2 == 1 else Materials.WALL.value) for x in range(16)] for y in range(16)])
		chunk: Chunk = Chunk([[Block(Materials.GRASS.value) for x in range(16)] for y in range(16)])
		ax = x * 16
		ay = y * 16
		for dx in range(16):
			for dy in range(16):
				height = self.getHeight(ax + dx, ay + dy)
				# print(f"height: {height}, x: {ax+dx},y: {ay+dy}")
				if height < self.settings["wallHeight"]:
					chunk.setBlock(dx, dy, Block(Materials.GRASS.value))
				else:
					chunk.setBlock(dx, dy, Block(Materials.WALL.value))
		return chunk
