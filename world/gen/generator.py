import random

from opensimplex import OpenSimplex

from utils.timer import Timer
from world.block import Block
from world.chunk import Chunk
from world.material.materials import Materials


class Generator:
	def __init__(self, seed):
		self.seed = seed
		self.noise = OpenSimplex(seed=seed)
		self.settings = {
			"wallHeight": 0.75,
			"randomizers": [  # Fancy random numbers
				752247,
				248398,
				58437,
				21553,
				12846  # Don't make the last one too high (is exponent)
			]
		}

	def getHeight(self, x: int, y: int):
		return (self.noise.noise2d(x, y) + 1) / 2

	def generateChunk(self, x: int, y: int):
		Timer.start(f"Chunk: {x},{y}")
		chunkseed = self.seed + \
					int(x * x * self.settings["randomizers"][0]) + \
					int(x * self.settings["randomizers"][1]) + \
					int(y * y * self.settings["randomizers"][2]) + \
					pow(int(y * self.settings["randomizers"][3]), self.settings["randomizers"][4])
		random.seed(chunkseed)
		print(f"generating chunk ({x},{y})")
		chunk: Chunk = Chunk([[Block(Materials.GRASS.value) for x in range(16)] for y in range(16)])
		for dx in range(16):
			for dy in range(16):
				height = self.getHeight(x * 16 + dx, y * 16 + dy)
				if height < self.settings["wallHeight"]:
					chunk.setBlock(dx, dy, Block(Materials.GRASS.value))
				else:
					chunk.setBlock(dx, dy, Block(Materials.WALL.value))
				if random.randint(0, 64) == 0:
					chunk.setBlock(dx, dy, Block(Materials.TREE.value))
		print(f"Took: {Timer.stop(f'Chunk: {x},{y}')} seconds")
		return chunk
