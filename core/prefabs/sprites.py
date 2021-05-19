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
from console import Console


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

	# Check player input (currently only movement keys)
	def get_keys(self):
		self.vel = pygame.math.Vector2(0, 0)
		keys = pygame.key.get_pressed()

		if keys[ord(self.game.cpc['BINDS']['MOVELEFT'])]:
			self.vel.x = -self.speed
		if keys[ord(self.game.cpc['BINDS']['MOVERIGHT'])]:
			self.vel.x = self.speed
		if keys[ord(self.game.cpc['BINDS']['MOVEUP'])]:
			self.vel.y = -self.speed
		if keys[ord(self.game.cpc['BINDS']['MOVEDOWN'])]:
			self.vel.y = self.speed
		if self.vel.x != 0 and self.vel.y != 0:
			self.vel *= 0.7071
		if keys[K_p] and self.debug_print_cooldown == 0:
			# TODO: Debug menu for skills
			Console.log(thread="Player",
						message="-------------------------------------------------")
			for bs in baseskills.Baseskills:
				Console.log(thread="Player",
							message=f"{bs.value.name} {bs.value.lvl.level} {bs.value.lvl.xp} {bs.value.lvl.xp_needed}")
			Console.log(thread="Player",
						message="-------------------------------------------------")
			for ps in playerskills.Playerskills:
				Console.log(thread="Player",
							message=f"{ps.value.name} {ps.value.lvl.level} {ps.value.lvl.xp_needed}")
			Console.log(thread="Player",
						message="-------------------------------------------------")
			Console.log(thread="Player",
						message="Format: level | xp | sp | hp | armor")
			Console.log(thread="Player",
						message=f"Player {self.lvl.level} {self.lvl.xp} {self.skillpoints} {self.hp} {self.armor}")
			self.debug_print_cooldown = 1
		if keys[K_i] and self.debug_print_cooldown == 0:
			Console.log(thread="Player",
						message="Inventory:")
			for it in self.inventory.inv.ls:
				Console.log(thread="Player",
							message=f"{it.item.displayName} {it.quantity} {it.item.max_stack}")
			self.debug_print_cooldown = 1
		if keys[K_o]:
			Console.log(thread="Player",
						message=f"world.entities: {self.game.world.entities}")

	# DEPRICATED
	def get_events(self):
		for ev in pygame.event.get():
			if ev.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
				for tree in self.game.trees:
					if tree.collidepoint(pygame.mouse.get_pos()):
						# Chop down the tree
						pass

	# Check mouse actions
	def get_mouse(self):
		mouse = pygame.mouse.get_pressed(5)
		if mouse[0]:
			for tree in self.game.trees:
				rel_mouse = (math.floor((pygame.mouse.get_pos()[0] + self.game.player.pos[0]) - WIDTH / 2),
								math.floor((pygame.mouse.get_pos()[1] + self.game.player.pos[1]) - HEIGHT / 2))

				# print(rel_mouse, pygame.mouse.get_pos())
				# Check if the mouse and tree image collide
				if tree.rect.collidepoint(rel_mouse):
					if self.inventory.hands[0].item.name.lower() == 'axe' or self.inventory.hands[
						1].item.name.lower() == 'axe':

						# Chop down the tree
						tree.kill()

						# Add wood to inventory
						# TODO: Add woodcutting skill multiplier
						amount = randint(1, 5)
						self.inventory.add_new_item(Items['WOOD'], amount)
						# Display message for amount of wood
						Console.log(thread="Player",
									message=f"You got {amount} wood!")

						# TODO: Add wood to inventory
						# Add exp to woodcutting
						# TODO: Add multiplier/check tree type?
						baseskill.get_from_name(self.baseskills, "Woodcutting").lvl.xp += 10
						# TODO: Pure debug text, remove later
						Console.log(thread="Player",
									message="You chopped down a tree and gained 10 Woodcutting xp!")
						Console.log(thread="Player",
									message="Your player gained 10 xp")
						self.lvl.xp += 10
						self.check_levels()
					else:
						Console.log(thread="Player",
									message="You need an axe to break a tree")

	# Gets called every frame to update the player's status
	def update(self):
		self.get_keys()
		# Move the player
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.collision_rect.centerx = self.pos.x
		# self.collide_with_walls('x')
		self.collision_rect.centery = self.pos.y
		# self.collide_with_walls('y')
		self.collide_with_walls()
		self.pos += self.vel * self.game.dt
		self.rect.center = self.collision_rect.center

		self.get_mouse()

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
							self.hp -= 5
						if self.vel.x < 0 and dx < 0:
							# print("a")
							self.vel.x = 0
							self.hp -= 5
						if self.vel.y > 0 and dy > 0:
							# print("s")
							self.vel.y = 0
							self.hp -= 5
						if self.vel.y < 0 and dy < 0:
							# print("w")
							self.vel.y = 0
							self.hp -= 5


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
		self.move()

	def move(self):
		pass
