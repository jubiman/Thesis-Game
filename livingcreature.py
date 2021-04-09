import pygame


class LivingCreature(pygame.sprite.Sprite):
	def __init__(self, game, hp, max_hp, armor, speed):
		self.groups = game.sprites

		# Get the game's object so we can interact with the world
		self.game = game

# LivingCreature Base
		self.hp = hp  # TODO: Ability to change the HP of player
		self.max_hp = max_hp
		self.armor = armor
		self.speed = speed
		# TODO: max_hp

		# Initialize Sprite base
		pygame.sprite.Sprite.__init__(self, self.groups)
