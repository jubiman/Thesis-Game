import pygame
from settings import *


class Map:
	def __init__(self, fn):
		self.data = []
		with open(fn, 'rt') as f:
			for l in f:
				self.data.append(l.strip())
		self.tWidth = len(self.data[0])
		self.tHeight = len(self.data)
		self.width = self.tWidth * TILESIZE
		self.height = self.tHeight * TILESIZE


class Camera:
	# TODO: Implement Camera
	def __init__(self, width, height):
		self.camera = pygame.Rect(0, 0, width, height)
		self.width = width
		self.height = height

	def apply(self, entity):
		return entity.rect.move(self.camera.topleft)

	def update(self, target):
		x = -target.rect.x + int(WIDTH/2)
		y = -target.rect.y + int(HEIGHT/2)
		self.camera = pygame.Rect(x, y, self.width, self.height)