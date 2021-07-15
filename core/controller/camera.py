import pygame

from settings import HEIGHT, WIDTH


class Camera(pygame.Rect):
	# TODO: Implement Camera
	def __init__(self):
		super().__init__(0, 0, 0, 0)
		self.camera = pygame.Rect(0, 0, 0, 0)

	def apply(self, entity):
		return entity.rect.move(self.camera.topleft)

	def applyraw(self, rect):
		return rect.move(self.camera.topleft)

	def update(self, target):
		self.camera = pygame.Rect(-target.rect.centerx + WIDTH / 2, -target.rect.centery + HEIGHT / 2, 0, 0)
