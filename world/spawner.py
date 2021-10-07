import math
from random import randint

from pygame.math import Vector2

from core.console.consolefunctions import Console
from world.entity.entities.enemy import Enemy
from world.entity.entitytypes import EntityTypes


class Spawner:
	def __init__(self, game, r=2, mr=1):
		"""
		:param Game game: The game engine object
		:param int r: maximum range from the player
		:param int mr:
		"""
		self.game = game
		self.radius = r
		self.min_r = mr

	def spawnEvent(self):
		# TODO: Check for possible bugs and improve code
		# TODO: Add event call.
		loc = Vector2(math.floor(
			self.game.player.pos.x + randint(-self.radius + self.min_r, self.radius + self.min_r) - self.min_r),
			math.floor(self.game.player.pos.y + randint(-self.radius + self.min_r,
														self.radius + self.min_r) - self.min_r))

		chunk: tuple[int, int] = (int(loc.x // 16), int(loc.y // 16))

		for ent in self.game.world.entities:
			while ent.entitytype.rect.collidepoint(loc):
				Console.log(thread="SPAWNER",
							message=f"There is already a sprite at {loc}.")
				loc = Vector2(math.floor(
					self.game.player.pos.x + randint(-self.radius + self.min_r, self.radius + self.min_r) - self.min_r),
					math.floor(self.game.player.pos.y + randint(-self.radius + self.min_r,
																self.radius + self.min_r) - self.min_r))

		while self.game.world.getChunkAt(chunk[0], chunk[1]).getBlock(int(loc.x % 16),
																	  int(loc.y % 16)).material.id not in [0, 1]:
			Console.log(thread="SPAWNER",
						message=f"There is already a sprite at {loc}.")
			loc = Vector2(math.floor(
				self.game.player.pos.x + randint(-self.radius + self.min_r, self.radius + self.min_r) - self.min_r),
				math.floor(self.game.player.pos.y + randint(-self.radius + self.min_r,
															self.radius + self.min_r) - self.min_r))

		self.game.world.entities.append(
			Enemy(EntityTypes.ENEMYTEST.value, chunk, loc, 300, self.game, 10, 2))
		Console.event(thread="SPAWNER",
					  message=f"Enemy spawned at {loc} in chunk {chunk}")

	def spawnEventLoc(self, x, y, enemy):
		"""
		:param Any x: X coordinate for the spawn location of the enemy
		:param Any y: Y coordinate for the spawn location of the enemy
		:param EntityTypes enemy: The type of enemy to spawn
		:return: Returns 1 on failure and 0 on success
		:rtype: int
		"""
		# TODO: Placeholder
		if not enemy:
			enemy = EntityTypes.ENEMYTEST.value
		# TODO: Check for possible bugs and improve code
		loc = Vector2(x, y)

		chunk: tuple[int, int] = (int(loc.x // 16), int(loc.y // 16))

		for ent in self.game.world.entities:
			while ent.entitytype.rect.collidepoint(loc):
				Console.log(thread="SPAWNER",
							message=f"There is already a sprite at {loc}.")
				return 1

		if self.game.world.getBlockAt(int(loc.x % 16), int(loc.y % 16)).material.id not in [0, 1]:
			Console.log(f"There is already a sprite at {loc}.", thread="SPAWNER")
			return 1

		self.game.world.entities.append(
			Enemy(enemy, chunk, loc, 1, self.game, 10, 2))
		Console.event(f"Enemy spawned at {loc} in chunk {chunk}", thread="SPAWNERLOC")
		return 0

	def dungeonSpawn(self, nmin, nmax, chunk, x, y):
		"""
		:param nmin: minimum number of enemies
		:param nmax: maximum number of enemies
		:param chunk: the chunk data of the chunk we're spawning the enemy in
		:param x: the x location of the chunk
		:param y: the y location of the chunk
		:return: function of void type
		"""
		# tmp = []
		ents = []
		for i in range(randint(nmin, nmax)):
			loc = Vector2(randint(0, 15), randint(0, 15))
			for ent in ents:
				# logging.debug(f"Ent: {ent.entitytype.displayName}, {ent.entitytype.rect}")
				if ent.entitytype.rect.collidepoint(loc):
					Console.log(thread="SPAWNER",
								message=f"There is already a sprite at {loc}.")
					# Console.debug(((x * 16 + loc.x) * TILESIZE, (y * 16 + loc.y) * TILESIZE))
					loc = Vector2(randint(0, 15), randint(0, 15))
			# return 1  # why while loop if ur gonna return instantly??? what was i thinking man

			Console.log(thread="SPAWNER",
						message=loc)
			while chunk.getBlock(int(loc.x), int(loc.y)).material.id not in [0, 1]:
				Console.log(thread="SPAWNER",
							message=f"There is already a block at {loc}.")
				loc = Vector2(randint(0, 15), randint(0, 15))
			# loc = Vector2(x * 16 + loc.x, y * 16 + loc.y)
			loc = Vector2(*(loc * 16))

			Console.event(thread="SPAWNER",
						  message=f"Spawning enemy at {loc}")
			en = Enemy(EntityTypes.ENEMYTEST.value, (x, y), loc, 300, self.game, 10, 2)
			ents.append(en)
			self.game.world.entities.append(en)
