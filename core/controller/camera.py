import pygame

from settings import *


class Camera(pygame.Rect):
	# TODO: Implement Camera
	def __init__(self, width, height):
		super().__init__(0, 0, width, height)
		self.camera = pygame.Rect(0, 0, width, height)
		self.width = width
		self.height = height

	def apply(self, entity):
		return entity.rect.move(self.camera.topleft)

	def applyraw(self, rect):
		return rect.move(self.camera.topleft)

	def update(self, target):
		self.camera = pygame.Rect(-target.rect.x + int(WIDTH / 2), -target.rect.y + int(HEIGHT / 2), self.width,
								  self.height)
