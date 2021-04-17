import pygame.math

from sprites import EnemyStandard
from random import randint, random
from settings import TILESIZE
from pygame.math import Vector2
from world.entity import Entity
from world.entities import Entities

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
		# TODO: Check if location is in a wall
		loc = Vector2(self.game.player.pos.x + randint(-self.radius + self.min_r, self.radius + self.min_r) - self.min_r,
						self.game.player.pos.y + randint(-self.radius + self.min_r, self.radius + self.min_r) - self.min_r) / TILESIZE
		self.game.world.entities.append(EnemyStandard(self.game, 10, 10, 2, 300, *loc))
