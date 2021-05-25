from pygame.math import Vector2

from world.entity.entitytype import EntityType
from world.entity.pathfinding.pathfinding import Pathfinding


class Enemy:
	def __init__(self, ent: EntityType, sprite, chunk: tuple[int, int], pos: Vector2, speed, game):
		"""
		:param ent: The EntityType of the enemy
		:param Any sprite: The sprite object of the enemy
		:param chunk: The chunk the enemy is in
		"""
		self.entitytype = ent
		self.sprite = sprite
		self.chunk = chunk
		self.pos = pos
		self.vel = Vector2(0, 0)
		self.speed = speed
		self.game = game

	def update(self):
		# print(Pathfinding.find(self, world.game.player, world))
		# for loc in Pathfinding.find(self, world.game.player, world):
		# path = Pathfinding.find(self, world.game.player, world)
		path = Pathfinding.findOneStatic(self, self.game.player, self.game.world)
		if path is not None:
			if len(path) > 1:
				self.move(*(path[1] - path[0]))
			else:
				self.move(*path[0])
		self.pos += self.vel * self.game.dt
		self.sprite.update()

	def move(self, dirx, diry):
		self.vel = Vector2(dirx * self.speed, diry * self.speed)
