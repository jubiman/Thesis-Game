from pygame.math import Vector2

from world.entity.entitytype import EntityType
from world.entity.pathfinding.pathfinding import Pathfinding
from core.prefabs.livingcreature import LivingCreature
from core.console.console import Console


class Enemy:
	def __init__(self, ent: EntityType, chunk: tuple[int, int], pos: Vector2, speed, game, hp, armor):
		"""
		:param ent: The EntityType of the enemy
		:param chunk: The chunk the enemy is in
		:param int speed: Speed of the player
		"""
		# super().__init__(game, sprite.hp, sprite.max_hp, sprite.armor, speed)
		self.entitytype = ent
		self.chunk = chunk
		self.pos = Vector2(pos)
		self.vel = Vector2(0, 0)
		self.speed = speed
		self.game = game

		self.hp = hp
		self.max_hp = hp
		self.armor = armor

		self.cooldown = 0

	def update(self):
		# print(Pathfinding.find(self, world.game.player, world))
		# for loc in Pathfinding.find(self, world.game.player, world):
		# path = Pathfinding.find(self, world.game.player, world)
		if self.cooldown != 0:
			self.cooldown += self.game.clock.get_time()
		if self.cooldown > 200:
			self.cooldown = 0

		if self.cooldown == 0:
			# path = Pathfinding.findOneStatic(self, self.game.player, self.game.world)
			path = None
			if path is not None:
				self.move(*path[0])
			self.cooldown = 1

		self.entitytype.rect = self.entitytype.image.get_rect()
		self.entitytype.rect.centerx = self.pos.x
		self.entitytype.rect.centery = self.pos.y
		self.pos += self.vel * self.game.dt

	def move(self, dirx, diry):
		if dirx != 0 and diry != 0:
			self.vel = Vector2(dirx * self.speed * 0.7071, diry * self.speed * 0.7071)
			return
		self.vel = Vector2(dirx * self.speed, diry * self.speed)
