import math
from core.prefabs.sprites import EnemyStandard
from random import randint
from settings import TILESIZE
from pygame.math import Vector2
from world.entitytypes import EntityTypes
from world.enemy import Enemy


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
		loc = Vector2(math.floor(self.game.player.pos.x + randint(-self.radius + self.min_r, self.radius + self.min_r) - self.min_r),
					  math.floor(self.game.player.pos.y + randint(-self.radius + self.min_r, self.radius + self.min_r) - self.min_r))

		chunk: tuple[int, int] = loc / TILESIZE // 16

		for ent in self.game.world.entities:
			while ent.entitytype.rect.collidepoint(loc):
				print(f"There is already a sprite at {loc}.")
				loc = Vector2(math.floor(self.game.player.pos.x + randint(-self.radius + self.min_r, self.radius + self.min_r) - self.min_r),
							  math.floor(self.game.player.pos.y + randint(-self.radius + self.min_r, self.radius + self.min_r) - self.min_r)) / TILESIZE

		while self.game.world.getChunkAt(chunk[0], chunk[0]).getBlock(int(loc.x % 16), int(loc.y % 16)).material.id not in [0, 1]:
			print(f"There is already a sprite at {loc}.")
			loc = Vector2(math.floor(self.game.player.pos.x + randint(-self.radius + self.min_r, self.radius + self.min_r) - self.min_r),
						  math.floor(self.game.player.pos.y + randint(-self.radius + self.min_r, self.radius + self.min_r) - self.min_r)) / TILESIZE

		self.game.world.entities.append(
			Enemy(EntityTypes.ENEMYTEST.value, EnemyStandard(self.game, 10, 10, 2, 300, loc.x, loc.y), (chunk[0], chunk[1]), loc))
		print(f"Enemy spawned at {loc} in chunk {chunk}")

	def spawnEventLoc(self, x, y):
		"""
		:param Any x: X coordinate for the spawn location of the enemy
		:param Any y: Y coordinate for the spawn location of the enemy
		:return: Returns 1 on failure and 0 on success
		:rtype: int
		"""
		# TODO: Check for possible bugs and improve code
		loc = Vector2(x, y)

		chunk: tuple[int, int] = loc / TILESIZE // 16

		for ent in self.game.world.entities:
			while ent.entitytype.rect.collidepoint(loc):
				print(f"There is already a sprite at {loc}.")
				return 1

		while self.game.world.getChunkAt(chunk[0], chunk[0]).getBlock(int(loc.x % 16), int(loc.y % 16)).material.id not in [0, 1]:
			print(f"There is already a sprite at {loc}.")
			return 1

		self.game.world.entities.append(
			Enemy(EntityTypes.ENEMYTEST.value, EnemyStandard(self.game, 10, 10, 2, 300, loc.x, loc.y), (chunk[0], chunk[1]), loc))
		print(f"Enemy spawned at {loc} in chunk {chunk}")
		return 0
