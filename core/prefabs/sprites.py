import math
from random import randint

import pygame
from pygame.locals import *

import assets
from core.inventory import inventory
from core.items.items import Items
from core.prefabs.livingcreature import LivingCreature
from core.skills import baseskills, levelbase
from core.skills import playerskills
from settings import *
from world.block import Block
from world.material.materials import Materials
from core.console.consolefunctions import Console
from core.UI.ui import UI


class Player(LivingCreature):
	def __init__(self, game, hp, max_hp, armor, speed, x, y):

		# Getting specific information from LivingCreature class
		super().__init__(game, hp, max_hp, armor, speed)

		# Assets
		# Player image asset
		self.image = pygame.transform.scale(assets.get_asset_from_name(game.graphics, 'player1').image, (64, 64))
		self.rect = self.image.get_rect()

		# World interaction
		# Create player position and velocity
		self.vel = pygame.math.Vector2(0, 0)
		self.pos = pygame.math.Vector2(x, y) * TILESIZE
		# Collision properties
		self.collision_rect = pygame.Rect(0, 0, 35, 35)
		# self.collision_rect = pygame.Rect(0, 0, 64, 64)
		self.collision_rect.center = self.rect.center

		# Inventory
		# Create an empty inventory
		self.inventory = inventory.Inventory()
		# Set equipped slot to the first slot
		# self.equipped_slot = self.inventory.slots[0]
		# TODO: This is now done in the inventory itself

		# TODO: Add new way (Enum)
		# Skills (OLD WAY)
		# Initialize all base skills at level 0
		# self.baseskills = baseskill.init()
		# Initialize all upgradable skills for the player
		# self.playerskills = playerskill.init()

		# Player base
		# Set initial skill/level values
		self.skillpoints = 0
		self.lvl = levelbase.Levelbase(0, 0, 10, game=self.game)
		self.xp_formula = "x = x + 10"  # TODO: Change XP system

		# TODO: Set debug cooldown (might remove later)
		self.debug_print_cooldown = 0

	# Methods
	def check_levels(self):
		# Check base skills
		for bs in baseskills.Baseskills:
			if bs.value.lvl.xp >= bs.value.lvl.xp_needed:
				bs.value.lvl.levelup(t="player")
				# Display text to notify player of level up
				# TODO: Make notification on-screen, not in console
				Console.log(thread="Player",
					message=f"You leveled up {bs.value.name} to level {bs.value.lvl.level}! \
					You need {bs.value.lvl.xp_needed} xp for the next level")

		# Check player skills
		for ps in playerskills.Playerskills:
			if ps.value.lvl.xp >= ps.value.lvl.xp_needed:
				ps.value.lvl.levelup(t="player")
				# Display text to notify player of level up
				# TODO: Make notification on-screen, not in console
				Console.log(thread="Player",
							message=f"You leveled up {ps.value.name} to level {ps.value.lvl.level}! \
							You need {ps.value.lvl.xp_needed} xp for the next level")

		# Check player level
		while self.lvl.xp >= self.lvl.xp_needed:
			self.lvl.levelup()
			self.skillpoints += self.lvl.level * 333 % 4  # TODO: make dynamic
			# Display text to notify player of level up
			# TODO: Make notification on-screen, not in console
			Console.log(thread="Player",
						message=f"Your player leveled up to level {self.lvl.level}! You need {self.lvl.xp_needed} xp for the next level")

	# Gets called every frame to update the player's status
	def update(self):
		# self.get_keys()
		# Move the player
		self.rect = self.image.get_rect()
		self.collision_rect.centerx = self.pos.x
		self.collision_rect.centery = self.pos.y
		self.pos += self.vel * self.game.dt
		self.rect.center = self.collision_rect.center

		# self.get_mouse()

		# TODO: Debug cooldown, might remove later
		if self.debug_print_cooldown != 0:
			self.debug_print_cooldown += self.game.clock.get_time()
		if self.debug_print_cooldown > 400:
			self.debug_print_cooldown = 0

	# Called from move(), checks if the direction we're going is obstructed
	def collide_with_walls(self):
		# TODO: Make algorithm that checks only surrounding tiles + rewrite with world gen
		# if pos/TILESIZE+64 ==
		movedColRect = self.collision_rect.move(self.vel.x * self.game.dt, self.vel.y * self.game.dt)
		for dx in range(-3, 3):
			for dy in range(-3, 3):
				px = int(self.pos.x // TILESIZE)
				py = int(self.pos.y // TILESIZE)
				block: Block = self.game.world.getBlockAt(px + dx, py + dy)
				if block.material.id == Materials.WALL.value.id:
					rect: Rect = block.material.rect.move((px + dx) * TILESIZE, (py + dy) * TILESIZE)
					if rect.colliderect(movedColRect):
						# print(f"COLLIDE {self.vel} {dx},{dy}")
						if self.vel.x > 0 and dx > 0:
							# print("d")
							self.vel.x = 0
							UI.getElementByID(0).setHealthbar(self.hp - 5)
						if self.vel.x < 0 and dx < 0:
							# print("a")
							self.vel.x = 0
							UI.getElementByID(0).setHealthbar(self.hp - 5)
						if self.vel.y > 0 and dy > 0:
							# print("s")
							self.vel.y = 0
							UI.getElementByID(0).setHealthbar(self.hp - 5)
						if self.vel.y < 0 and dy < 0:
							# print("w")
							self.vel.y = 0
							UI.getElementByID(0).setHealthbar(self.hp - 5)


class EnemyStandard(LivingCreature):
	def __init__(self, game, hp, max_hp, armor, speed):
		# TODO: Remove pos and image from this class as it will be in enemy.py
		# TODO: Add movement (pathfinding
		# Getting specific information from LivingCreature class
		super().__init__(game, hp, max_hp, armor, speed)
		# Assets
		self.image = pygame.transform.scale(assets.get_asset_from_name(self.game.graphics, 'mage3').image, (64, 64))
		self.rect = self.image.get_rect()

	def update(self):
		# Move the player
		if self.image is not None:
			self.rect = self.image.get_rect()
