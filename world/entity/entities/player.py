from pygame import Vector2, Rect, draw

from core.UI.ui import UI
from core.inventory.inventory import Inventory
from core.prefabs.livingcreature import LivingCreature
from core.skills.levelbase import Levelbase
from core.skills.baseskills import Baseskills
from core.skills.playerskills import Playerskills
from core.console.console import Console
from settings import TILESIZE
from world.block import Block
from world.material.materials import Materials


class Player(LivingCreature):
	def __init__(self, game, hp, max_hp, armor, speed, x, y, ent):

		# Getting specific information from LivingCreature class
		super().__init__(game, hp, max_hp, armor, speed)

		self.entitytype = ent

	# World interaction
		# Create player position and velocity
		self.vel = Vector2(0, 0)
		self.pos = Vector2(x, y)

		# Collision properties
		self.collision_rect = Rect(0, 0, 35, 35)
		self.collision_rect.centerx = self.pos.x
		self.collision_rect.centery = self.pos.y

	# Inventory
		# Create an empty inventory
		self.inventory = Inventory()
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
		self.lvl = Levelbase(0, 0, 10, game=self.game)
		self.xp_formula = "x = x + 10"  # TODO: Change XP system

		# TODO: Set debug cooldown (might remove later)
		self.debug_print_cooldown = 0

	# Methods
	def check_levels(self):
		# Check base skills
		for bs in Baseskills:
			if bs.value.lvl.xp >= bs.value.lvl.xp_needed:
				bs.value.lvl.levelup(t="player")
				# Display text to notify player of level up
				# TODO: Make notification on-screen, not in console
				Console.log(thread="Player",
					message=f"You leveled up {bs.value.name} to level {bs.value.lvl.level}! \
					You need {bs.value.lvl.xp_needed} xp for the next level")

		# Check player skills
		for ps in Playerskills:
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
		# Move the player
		self.pos += self.vel * self.game.dt / TILESIZE

		self.entitytype.rect = self.entitytype.image.get_rect()
		self.entitytype.rect.centerx = self.pos.x * TILESIZE
		self.entitytype.rect.centery = self.pos.y * TILESIZE
		self.collision_rect.center = self.entitytype.rect.center

		# TODO: Debug cooldown, might remove later
		if self.debug_print_cooldown != 0:
			self.debug_print_cooldown += self.game.clock.get_time()
		if self.debug_print_cooldown > 400:
			self.debug_print_cooldown = 0

	# Called from inputhandler, checks if the direction we're going is obstructed
	def collide_with_walls(self):
		# TODO: Make algorithm that checks only surrounding tiles + rewrite with world gen
		movedColRect = self.collision_rect.move(self.vel * self.game.dt / TILESIZE)
		draw.rect(self.game.screen, (125, 125, 125), self.game.camera.applyraw(movedColRect), 1)
		for dx in range(-3, 3):
			for dy in range(-3, 3):
				block: Block = self.game.world.getBlockAt(self.pos.x + dx, self.pos.y + dy)
				if block.material.id == Materials.WALL.value.id:
					rect: Rect = block.material.rect.move(self.pos.x + dx, self.pos.y + dy)
					if rect.colliderect(movedColRect):
						if self.vel.x > 0 and dx > 0:
							self.vel.x = 0
							UI.HEALTHBAR.value.setHealthbar(self.hp - 5)
						if self.vel.x < 0 and dx < 0:
							self.vel.x = 0
							UI.HEALTHBAR.value.setHealthbar(self.hp - 5)
						if self.vel.y > 0 and dy > 0:
							self.vel.y = 0
							UI.HEALTHBAR.value.setHealthbar(self.hp - 5)
						if self.vel.y < 0 and dy < 0:
							self.vel.y = 0
							UI.HEALTHBAR.value.setHealthbar(self.hp - 5)