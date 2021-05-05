import json
import os.path
import random
import time

from world.block import Block
from world.cache import Cache
from world.chunk import Chunk
from world.entity.enemy import Enemy
from world.gen.dungeongenerator import DungeonGenerator
from world.gen.generator import Generator
from world.material.materials import Materials


class World:
	def __init__(self, path):
		self.filepath = path
		self.isloaded = False
		self.configfile = None
		self.config = None
		self.name = None
		self.generator = None
		self.seed = None
		self.worldtype = None
		self.cache = Cache(self)
		self.entities: list[Enemy] = []
		self.lastTick = time.time()

	def load(self):
		if not self.isloaded:
			# only run this code if the world isn't loaded yet.
			self.configfile = self.filepath + "/config.json"
			if not os.path.isdir(self.filepath):
				os.mkdir(self.filepath)
			if not os.path.isfile(self.configfile):
				# Create config if it smh doesn't exist
				self.config = {
					"name": self.filepath.split("/")[-1],
					"seed": random.randint(0, 2 ** 31 - 1),
					"worldtype": "default"
				}
				open(self.configfile, "w").write(json.dumps(self.config))
			else:
				self.config = json.loads(open(self.configfile, "r").read())
			self.name = self.config["name"]
			self.seed = self.config["seed"]
			self.worldtype = self.config["worldtype"]
			self.generator = Generator(self.seed) if self.worldtype == "default" else DungeonGenerator(
				self.filepath[0:self.filepath.rfind("\\")], self.seed)

	def loadChunk(self, x: int, y: int):
		if os.path.isfile(os.path.join(self.filepath, "chunks", f"{x},{y}.json")):
			data = json.loads(open(os.path.join(self.filepath, "chunks", f"{x},{y}.json"), "r").read())
			blocks_json_list = data["b"]
			blocks_list: list[list[Block]] = []
			for cx in range(16):
				blocks_list.append([])
				for cy in range(16):
					blocks_list[cx].append(Block(Materials.getMaterial(blocks_json_list[cx * 16 + cy])))
			chunk = Chunk(blocks_list)
			return chunk
		return self.generator.generateChunk(x, y)

	def unload(self, x: int, y: int):
		print(f"Unloading: {x}, {y}")
		self.save(x, y)
		del self.cache.chunks[x, y]

	def save(self, x: int, y: int):
		cfile = os.path.join(self.filepath, "chunks", f"{x},{y}.json")
		if not os.path.isdir(os.path.join(self.filepath, "chunks")):
			os.mkdir(os.path.join(self.filepath, "chunks"))
		c = self.cache.chunks[x, y]
		blockjsonobj = []
		for row in c.blocks:
			for block in row:
				blockjsonobj.append(block.material.id)
		open(cfile, "w").write(json.dumps({
			"b": blockjsonobj
		}))

	def tick(self):
		now = time.time()
		if now - self.lastTick > 1.0 / 20:
			self.cache.checkForLazyChunks()
			self.lastTick = now

	def specialLoadChunk(self, x, y):
		return self.generator.specialGen(x, y)

	def getBlockAt(self, x: int, y: int):
		return self.getChunkAt(x // 16, y // 16).getBlock(x % 16, y % 16)

	def getBlockAtTup(self, loc: tuple[int, int]):
		return self.getChunkAt(loc[0] // 16, loc[1] // 16).getBlock(loc[0] % 16, loc[1] % 16)

	def getChunkAt(self, x: int, y: int):
		return self.cache.getChunk(x, y)
