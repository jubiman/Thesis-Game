from opensimplex import OpenSimplex

from world.block import Block
from world.chunk import Chunk
from world.materials import Materials
from world.enemy import Enemy
from world.entitytypes import EntityTypes

class Generator:

	def __init__(self, seed):
		self.seed = seed
		self.noise = OpenSimplex(seed=seed)
		self.settings = {
			"wallHeight": 0.5
		}

	def getHeight(self, x: int, y: int):
		return self.noise.noise2d(x, y)

	def generateChunk(self, x: int, y: int):
		print(f"generating chunk {x},{y}")
		chunk: Chunk = Chunk([[Block(Materials.GRASS.value) for x in range(16)] for y in range(16)])
		for dx in range(16):
			for dy in range(16):
				height = self.getHeight(x * 16 + dx, y * 16 + dy)
				if height < self.settings["wallHeight"]:
					chunk.setBlock(dx, dy, Block(Materials.GRASS.value))
				else:
					chunk.setBlock(dx, dy, Block(Materials.WALL.value))
		return chunk
