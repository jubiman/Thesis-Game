import json
import os.path
import random

from world.cache import Cache
from world.gen.generator import Generator
from world.enemy import Enemy


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

	def load(self):
		if not self.isloaded:
			# only run this code if the world isn't loaded yet.
			self.configfile = self.filepath + "/config.json"
			if not os.path.isfile(self.configfile):
				# Create config if it smh doesn't exist
				self.config = {
					"name": self.filepath.split("/")[len(self.filepath.split("/")) - 1],
					"seed": random.randint(0, 2 ** 31 - 1),
					"worldtype": "default"
				}
			else:
				self.config = json.loads(open("config.json", "r").read())
			self.name = self.config["name"]
			self.seed = self.config["seed"]
			self.worldtype = self.config["worldtype"]
			self.generator = Generator(self.seed)

	def loadChunk(self, x: int, y: int):
		if os.path.isfile(self.filepath + "/regions/" + f"{x},{y}.reg"):
			# TODO: load chunk from file
			return None
		return self.generator.generateChunk(x, y)

	def getBlockAt(self, x: int, y: int):
		return self.getChunkAt(x // 16, y // 16).getBlock(x % 16, y % 16)

	def getBlockAtTup(self, loc: tuple[int, int]):
		return self.getChunkAt(loc[0] // 16, loc[1] // 16).getBlock(loc[0] % 16, loc[1] % 16)

	def getChunkAt(self, x: int, y: int):
		return self.cache.getChunk(x, y)
