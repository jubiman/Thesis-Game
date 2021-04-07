import pygame
from pygame.locals import *
from settings import *
import assets
import inventory
import baseskill
import playerskill
import math
import item
import levelbase
from random import randint
from livingcreature import LivingCreature


class Player(LivingCreature):
	def __init__(self, game, hp, max_hp, armor, x, y):

		# Getting specific information from LivingCreature class
		super().__init__(game, hp, max_hp, armor)

# Assets
		# Player image asset
		self.image = pygame.transform.scale(assets.get_asset_from_name(game.graphics, 'player1').image, (64, 64))
		self.rect = self.image.get_rect()

# World interaction
		# Create player position and velocity
		self.vel = pygame.math.Vector2(0, 0)
		self.pos = pygame.math.Vector2(x, y) * TILESIZE

# Inventory
		# Create an empty inventory
		self.inventory = inventory.Inventory()
		# Set equipped slot to the first slot
		self.equipped_slot = self.inventory.slots[0]

# Skills
		# Initialize all base skills at level 0
		self.baseskills = baseskill.init()
		# Initialize all upgradable skills for the player
		self.playerskills = playerskill.init()

# Player base
		# Set initial skill/level values
		self.skillpoints = 0
		self.level = levelbase.Levelbase(0, 0, 10)
		self.xp_formula = "x = x + 10"  # TODO: Change XP system

		# TODO: Set debug cooldown (might remove later)
		self.debug_print_cooldown = 0

# Methods
	def check_levels(self):
		# Check base skills
		for bs in self.baseskills:
			if bs.level.xp >= bs.level.xp_needed:
				bs.level.levelup()
				"""bs.xp = 0
				bs.level += 1
				# TODO: just a placeholder, check basekill.py
				bs.xp_needed += 10"""

				# Display text to notify player of level up
				# TODO: Make notification on-screen, not in console
				print(f"You leveled up {bs.name} to level {bs.level.level}!")
		# Check player skills
		for ps in self.playerskills:
			if ps.level.xp >= ps.level.xp_needed:
				ps.level.levelup()
				"""ps.xp = 0
				ps.level += 1
				# TODO: just a placeholder, check playerskill.py
				ps.xp_needed += 10"""
				print(f"You leveled up {ps.name} to level {ps.level.level}!")
		# Check player level
		if self.level.xp >= self.level.xp_needed:
			self.level.levelup()
			self.skillpoints += 1 * self.level.level * 333 % 4  # TODO: make dynamic
			print(f"Your player leveled up to level {self.level.level}!")

	# Check player input (currently only movement keys)
	def get_keys(self):
		self.vel = pygame.math.Vector2(0, 0)
		keys = pygame.key.get_pressed()
		if keys[K_a]:
			self.vel.x = -PLAYERSPEED
		if keys[K_d]:
			self.vel.x = PLAYERSPEED
		if keys[K_w]:
			self.vel.y = -PLAYERSPEED
		if keys[K_s]:
			self.vel.y = PLAYERSPEED
		if self.vel.x != 0 and self.vel.y != 0:
			self.vel *= 0.7071
		if keys[K_i]:
			self.pos = (256, 192)
		if keys[K_p] and self.debug_print_cooldown == 0:
			# TODO: Debug menu for skills
			print("-------------------------------------------------")
			for bs in self.baseskills:
				print(bs.name, bs.level.level, bs.level.xp, bs.level.xp_needed)
			print("-------------------------------------------------")
			for ps in self.playerskills:
				print(ps.name, ps.level.level, ps.level.xp_needed)
			print("-------------------------------------------------")
			print("Format: level | xp | sp | hp | armor")
			print("Player", self.level.level, self.level.xp, self.skillpoints, self.hp, self.armor)
			self.debug_print_cooldown = 1
		if keys[K_l] and self.debug_print_cooldown == 0:
			print("Inventory:")
			for it in self.inventory.inv:
				print(it.item.name, it.quantity)
			self.debug_print_cooldown = 1

	def get_events(self):
		for ev in pygame.event.get():
			print("1")
			if ev.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
				print("2")
				for tree in self.game.trees:
					if tree.collidepoint(pygame.mouse.get_pos()):
						# Chop down the tree
						print(tree)

	# Check mouse actions
	def get_mouse(self):
		mouse = pygame.mouse.get_pressed()
		if mouse[0]:
			for tree in self.game.trees:
				rel_mouse = (math.floor((pygame.mouse.get_pos()[0] + self.game.player.pos[0]) - 8 * 64),
								math.floor((pygame.mouse.get_pos()[1] + self.game.player.pos[1]) - 6 * 64))

				# Check if the mouse and tree image collide
				if tree.rect.collidepoint(rel_mouse):
					if self.equipped_slot.get_item().name.lower() == 'axe':

						# Chop down the tree
						tree.kill()

						# Add wood to inventory
						# TODO: Add woodcutting skill multiplier
						amount = randint(1, 5)
						self.inventory.add_new_item(item.get_item_from_name(self.game.items, 'Wood'), amount)
						# Display message for amount of wood
						print(f"You got {amount} wood!")

						# TODO: Add wood to inventory
						# Add exp to woodcutting
						# TODO: Add multiplier/check tree type?
						baseskill.get_from_name(self.baseskills, "Woodcutting").level.xp += 10
						# TODO: Pure debug text, remove later
						print("You chopped down a tree and gained 10 Woodcutting xp!")
						print("Your player gained 10 xp")
						self.level.xp += 10
						self.check_levels()
					else:
						print("You need an axe to break a tree")

	# Gets called every frame to update the player's status
	def update(self):
		self.get_keys()
		# Move the player
		self.pos += self.vel * self.game.dt
		self.rect.x = self.pos.x
		self.collide_with_walls('x')
		self.rect.y = self.pos.y
		self.collide_with_walls('y')
		self.get_mouse()

		# TODO: Debug cooldown, might remove later
		if self.debug_print_cooldown != 0:
			self.debug_print_cooldown += self.game.clock.get_time()
		if self.debug_print_cooldown > 400:
			self.debug_print_cooldown = 0

	# Called from move(), checks if the direction we're going is obstructed
	def collide_with_walls(self, d):
		if d == 'x':
			hits = pygame.sprite.spritecollide(self, self.game.walls, False)
			if hits:
				if self.vel.x > 0:
					self.pos.x = hits[0].rect.left - self.rect.width
				if self.vel.x < 0:
					self.pos.x = hits[0].rect.right
				self.vel.x = 0
				self.rect.x = self.pos.x
		if d == 'y':
			hits = pygame.sprite.spritecollide(self, self.game.walls, False)
			if hits:
				if self.vel.y > 0:
					self.pos.y = hits[0].rect.top - self.rect.height
				if self.vel.y < 0:
					self.pos.y = hits[0].rect.bottom
				self.vel.y = 0
				self.rect.y = self.pos.y


class Wall(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.walls
		pygame.sprite.Sprite.__init__(self, self.groups)

		# Game object so we can interact with the world
		self.game = game

		# Wall image asset
		self.image = pygame.transform.scale(assets.get_asset_from_name(game.graphics, "wall1").image, (64, 64))
		self.rect = self.image.get_rect()

		# Set positions
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE


class Tree(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.trees
		pygame.sprite.Sprite.__init__(self, self.groups)

		# Game object so we can interact with the world
		self.game = game
		self.image = pygame.transform.scale(assets.get_asset_from_name(game.graphics, "tree1").image, (64, 64))
		self.rect = self.image.get_rect()

		# Set positions
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE


# class Enemy_standard(LivingCreature):
	# def __init__(self, game, hp, max_hp, armor, x, y):

		# Getting specific information from LivingCreature class
		# super().__init__(game, hp, max_hp, armor)
		# im soo angry right now

