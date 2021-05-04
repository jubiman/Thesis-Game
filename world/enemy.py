from pygame.math import Vector2

from world.entitytype import EntityType


class Enemy:
	def __init__(self, ent: EntityType, sprite, chunk: tuple[int, int], pos: Vector2):
		"""
		:param ent: The EntityType of the enemy
		:param Any sprite: The sprite object of the enemy
		:param chunk: The chunk the enemy is in
		"""
		self.entitytype = ent
		self.sprite = sprite
		self.chunk = chunk
		self.pos = pos
