import pygame


class LivingCreature(pygame.sprite.Sprite):
	def __init__(self, game, hp, max_hp, armor, speed):
		self.groups = game.sprites

		# Get the game's object so we can interact with the world
		self.game = game

		# LivingCreature Base
		self.hp = hp
		self.max_hp = max_hp
		self.armor = armor
		self.speed = speed

		# Initialize Sprite base
		pygame.sprite.Sprite.__init__(self, self.groups)
