import json
import os.path
import random
import shutil
import threading
import time

from pygame.math import Vector2

from core.console.console import Console
from core.inventory.inventory import Inventory
from core.utils.settings import Settings
from world.block import Block
from world.cache import Cache
from world.chunk import Chunk
from world.entity.entities.enemy import Enemy
from world.gen.dungeongenerator import DungeonGenerator
from world.gen.generator import Generator
from world.material.materials import Materials


class World:
	def __init__(self, path, game):
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
		self.game = game
		self.ticks = 0

	def auto_save(self):
		chunkcopy = self.cache.chunks.copy()
		self.update_config()
		self.save_config()

		def tempfunc():
			for coords in chunkcopy:
				x, y = coords
				savestr = self.get_raw_save_string(chunkcopy[coords], x, y)
				cfile = os.path.join(self.filepath, "region", f"{int(x // 16)},{int(y // 16)}.region")
				if savestr is not None:
					if not os.path.isfile(cfile):
						open(cfile, "w").close()
					with open(cfile, "r") as file:
						lines = file.readlines()
					with open(cfile, "w") as file:
						if len(lines) < 256:
							for i in range(256 - len(lines)):
								lines.append("\n")
						lines[int((x % 16) * 16 + y % 16)] = savestr + "\n"
						file.writelines(lines)

		threading.Thread(target=tempfunc, name="Auto Save").start()

	def update_config(self):
		self.config["playerpos"] = [self.game.player.pos.x, self.game.player.pos.y]
		self.config["inventory"] = self.game.player.inventory.to_json()

	def save_config(self):
		open(self.configfile, "w").write(json.dumps(self.config))

	def save_all(self):
		"""
		Updates the config and saves all loaded chunks.
		Useful for auto-saves.
		"""
		self.update_config()
		self.save_config()
		for coords in self.cache.chunks.copy():
			x, y = coords
			self.save(x, y)

	def unload_all(self):
		"""
		Updates the config and unloads all loaded chunks.
		Useful for unloading a world.
		"""
		self.update_config()
		self.save_config()
		for coords in self.cache.chunks.copy():
			x, y = coords
			self.unload(x, y)

	def load(self):
		if not self.isloaded:
			# Only run this code if the world isn't loaded yet.
			self.configfile = self.filepath + "/config.json"

			# Create new world if it doesn't exist already
			if not os.path.isdir(self.filepath):
				os.mkdir(self.filepath)
			# The default world configuration
			defaultconfig = {
				"name": self.filepath.split("/")[-1],
				"seed": random.randint(0, 2 ** 31 - 1),
				"worldtype": "default",
				"playerpos": [
					0.5,
					0.5
				]
			}
			# Create config file if existing
			if not os.path.isfile(self.configfile):
				# Create config if it smh doesn't exist
				self.config = defaultconfig
				open(self.configfile, "w").write(json.dumps(self.config))
			else:
				self.config = json.loads(open(self.configfile, "r").read())
				# Add key with default value if the option is not already defined in the config
				# Useful for changing the default config. When you add a new option it will be added
				# to the world config the next time it is loaded.
				for key in defaultconfig:
					if self.config.get(key) is None:
						self.config[key] = defaultconfig[key]
				self.game.player.pos.x, self.game.player.pos.y = self.config["playerpos"]
				if (invjson := self.config.get("inventory")) is not None:
					self.game.player.inventory = Inventory.from_json(invjson)

			# Make the Chunks folder where the chunks will be saved if it doesn't already exist
			try:
				os.mkdir(os.path.join(self.filepath, "region"))
			except FileExistsError:
				pass

			# Set some variables via config
			self.name = self.config["name"]
			self.seed = self.config["seed"]
			self.worldtype = self.config["worldtype"]

			# Select generator type
			self.generator = Generator(self.seed) if self.worldtype == "default" else DungeonGenerator(self.seed,
																									   self.game)

			# Do dungeon stuff if world is a dungeon
			if self.worldtype == "dungeon":
				Console.debug(thread="WORLD",
							  message=f"{self.name} {self.filepath}")
				# Set the player to the middle of the spawn or different posision if needed
				self.game.player.pos = Vector2(*map(int, self.config["startpos"].split(' ')))

				# Set the first chunk to be the spawn chunk
				# TODO: This shizzle doesn't work anymore, good luck fixing it future me.

				shutil.copy(os.path.join(Settings.GAMEDIR, "assets/dungeon/prefabs/spawn.json"),
							os.path.join(self.filepath, "chunks", "0,0.json"))

			# Set isloaded True so we don't reload the world
			self.isloaded = True
		else:
			Console.log(thread="WORLD", message=f"{self.name} is already loaded.")

	def loadChunk(self, x: int, y: int):
		Console.debug(thread="WORLD", message=f"Loading {x}, {y}")
		tworld = self

		def tempfunc(self):
			if os.path.isfile(os.path.join(self.filepath, "region", f"{int(x // 16)},{int(y // 16)}.region")) and (
					a := open(os.path.join(self.filepath, "region", f"{int(x // 16)},{int(y // 16)}.region"), "r").readlines()[int((x % 16) * 16 + y % 16)][:-1]) != "":
				data = json.loads(a)
				blocks_json_list = data["b"]
				blocks_list: list[list[Block]] = []
				for cx in range(16):
					blocks_list.append([])
					for cy in range(16):
						block = blocks_json_list[cx * 16 + cy]
						if isinstance(block, list):
							blocks_list[cx].append(Block(Materials.getMaterial(block[0]), data=block[1]))
						else:
							blocks_list[cx].append(Block(Materials.getMaterial(block)))
				chunk = Chunk(blocks_list)
				if data.get("e") is not None:
					ents = data.get("e")
					for ent in ents:
						tworld.entities.append(Enemy.deserialize(ent, chunk))
			else:
				chunk = self.generator.generateChunk(x, y)

			self.cache.chunks[x, y] = chunk

		# Load or generate the chunk in a separate thread.
		thread = threading.Thread(target=tempfunc, name=f"Generate Chunk {x},{y}", args=[self])
		thread.start()
		return Chunk([[Block(Materials.AIR.value) for x in range(16)] for y in range(16)])

	def unload(self, x: int, y: int):
		Console.log(thread="WORLD",
					message=f"Unloading: {x}, {y}")
		self.save(x, y)
		del self.cache.chunks[x, y]

	def save(self, x: int, y: int):
		cfile = os.path.join(self.filepath, "region", f"{int(x // 16)},{int(y // 16)}.region")
		c = self.cache.chunks[x, y]
		savestr = self.get_raw_save_string(c, x, y)
		if savestr is not None:
			if not os.path.isfile(cfile):
				open(cfile, "w").close()
			with open(cfile, "r") as file:
				lines = file.readlines()
			with open(cfile, "w") as file:
				if len(lines) < 256:
					for i in range(256 - len(lines)):
						lines.append("\n")
				lines[int((x % 16) * 16 + y % 16)] = savestr + "\n"
				file.writelines(lines)

	def get_raw_save_string(self, chunk: Chunk, x: int, y: int):
		if chunk.is_empty():
			return None
		blockjsonobj = []
		for row in chunk.blocks:
			for block in row:
				if block.data != {}:
					blockjsonobj.append([block.material.id, block.data])
				else:
					blockjsonobj.append(block.material.id)
		filteredents = [ent for ent in self.entities if x == ent.pos.x // 16 and y == ent.pos.y // 16]
		self.entities = [e for e in self.entities if e not in filteredents]
		data = {
			"b": blockjsonobj
		}
		if any(filteredents):
			data["e"] = [ent.serialize() for ent in filteredents]
		return json.dumps(data, separators=(',', ':'))

	def tick(self):
		now = time.time()
		if now - self.lastTick > 1.0 / 20:
			self.cache.checkForLazyChunks()
			self.lastTick = now
			self.ticks += 1
			if self.ticks % 6000 == 0:
				# Auto Save every 5 minutes
				self.auto_save()

		# Update entities every tick
		for ent in self.entities:
			ent.update()

	def getBlockAt(self, x: int, y: int):
		return self.getChunkAt(int(x // 16), int(y // 16)).getBlock(int(x % 16), int(y % 16))

	def getBlockAtTup(self, loc: tuple[int, int]):
		return self.getChunkAt(int(loc[0] // 16), int(loc[1] // 16)).getBlock(loc[0] % 16, loc[1] % 16)

	def getChunkAt(self, x: int, y: int):
		return self.cache.getChunk(x, y)

	def setBlock(self, x: int, y: int, block: Block):
		self.getChunkAt(int(x // 16), int(y // 16)).setBlock(int(x % 16), int(y % 16), block)
