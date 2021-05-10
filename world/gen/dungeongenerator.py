import json

from random import randint
from os import path

from world.block import Block
from world.chunk import Chunk
from world.material.materials import Materials
from world.spawner import Spawner
from settings import GAMEDIR


# TODO: load random dungeon from room files
class DungeonGenerator:
	def __init__(self, seed: int, game):
		self.game = game
		self.seed = seed
		self.rooms = {
			"room0": path.join(GAMEDIR, "assets/dungeon/prefabs/room0.json"),
			"room1": path.join(GAMEDIR, "assets/dungeon/prefabs/room1.json"),
			"room2": path.join(GAMEDIR, "assets/dungeon/prefabs/room2.json"),
			"room3": path.join(GAMEDIR, "assets/dungeon/prefabs/room3.json")
		}

	def generateChunk(self, x: int, y: int):
		print(f"generating dungeon chunk ({x}, {y})")
		# chunk: Chunk = Chunk([[Block(Materials.GRASS.value) for x in range(16)] for y in range(16)])
		rnd = randint(0, 3)
		cfg = json.loads(open(self.rooms[f"room{rnd}"], "r").read())
		blocks_json_list = cfg["b"]
		blocks_list: list[list[Block]] = []
		for cx in range(16):
			blocks_list.append([])
			for cy in range(16):
				blocks_list[cx].append(Block(Materials.getMaterial(blocks_json_list[cx * 16 + cy])))
		chunk = Chunk(blocks_list)
		self.game.spawner.dungeonSpawn(*map(int, cfg["enemies"].split(' ')), chunk, x, y)
		return chunk
