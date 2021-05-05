import json

from random import randint
from os import path

from world.block import Block
from world.chunk import Chunk
from world.material.materials import Materials


# TODO: load random dungeon from room files
class DungeonGenerator:
	def __init__(self, p: str, seed: str):
		self.seed = seed
		self.rooms = {
			"room0": path.join(p, "world/dungeon/prefabs/room0.json"),
			"room1": path.join(p, "world/dungeon/prefabs/room1.json"),
			"room2": path.join(p, "world/dungeon/prefabs/room2.json"),
			"room3": path.join(p, "world/dungeon/prefabs/room3.json")
		}

	def generateChunk(self, x: int, y: int):
		print(f"generating dungeon chunk ({x}, {y})")
		chunk: Chunk = Chunk([[Block(Materials.GRASS.value) for x in range(16)] for y in range(16)])
		rnd = randint(0, 3)
		cfg = json.loads(open(self.rooms[f"room{rnd}"], "r").read())
		for dx in range(16):
			for dy in range(16):
				chunk.setBlock(dx, dy, Block(Materials[cfg[str(dx)][dy].upper()].value))
		return chunk

