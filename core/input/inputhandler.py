from core.console.console import Console
from core.skills.baseskills import Baseskills
from core.skills.playerskills import Playerskills
from core.items.items import Items
from world.block import Block
from world.material.materials import Materials
from settings import *

import pygame
from pygame.locals import *
import math
from random import randint


class InputHandler:
	def __init__(self, game):
		self.game = game

	def handleInput(self):
		self.__getKeys()
		self.__getMouse()

	def __getKeys(self):
		self.game.player.game.player.vel = pygame.math.Vector2(0, 0)
		keys = pygame.key.get_pressed()

		if keys[ord(self.game.cpc['BINDS']['MOVELEFT'])]:
			self.game.player.vel.x = -self.game.player.speed
			self.game.player.collide_with_walls()
		if keys[ord(self.game.cpc['BINDS']['MOVERIGHT'])]:
			self.game.player.vel.x = self.game.player.speed
			self.game.player.collide_with_walls()
		if keys[ord(self.game.cpc['BINDS']['MOVEUP'])]:
			self.game.player.vel.y = -self.game.player.speed
			self.game.player.collide_with_walls()
		if keys[ord(self.game.cpc['BINDS']['MOVEDOWN'])]:
			self.game.player.vel.y = self.game.player.speed
			self.game.player.collide_with_walls()
		if self.game.player.vel.x != 0 and self.game.player.vel.y != 0:
			self.game.player.vel *= 0.7071
			self.game.player.collide_with_walls()
		if keys[K_p] and self.game.player.debug_print_cooldown == 0:
			# TODO: Debug menu for skills
			Console.log(thread="PLAYER",
						message="-------------------------------------------------")
			for bs in Baseskills:
				Console.log(thread="PLAYER",
							message=f"{bs.value.name} {bs.value.game.player.lvl.legame.player.vel} {bs.value.game.player.lvl.xp} {bs.value.game.player.lvl.xp_needed}")
			Console.log(thread="PLAYER",
						message="-------------------------------------------------")
			for ps in Playerskills:
				Console.log(thread="Player",
							message=f"{ps.value.name} {ps.value.game.player.lvl.legame.player.vel} {ps.value.game.player.lvl.xp_needed}")
			Console.log(thread="PLAYER",
						message="-------------------------------------------------")
			Console.log(thread="PLAYER",
						message="Format: level | xp | sp | hp | armor")
			Console.log(thread="PLAYER",
						message=f"Player {self.game.player.lvl.legame.player.vel} {self.game.player.lvl.xp} {self.game.player.skillpoints} {self.game.player.hp} {self.game.player.armor}")
			self.game.player.debug_print_cooldown = 1
		if keys[K_i] and self.game.player.debug_print_cooldown == 0:
			Console.log(thread="PLAYER",
						message="Inventory:")
			for it in self.game.player.inventory.inv.ls:
				Console.log(thread="PLAYER",
							message=f"{it.item.displayName} {it.quantity} {it.item.max_stack}")
			self.game.player.debug_print_cooldown = 1
		if keys[K_o]:
			Console.log(thread="PLAYER",
						message=f"world.entities: {self.game.world.entities}")

	def __getMouse(self):
		mouse = pygame.mouse.get_pressed(5)
		mouse_pos = pygame.mouse.get_pos()
		rel_mouse = (int((mouse_pos[0] - self.game.player.pos.x - (WIDTH / 2)) / TILESIZE),
						int((mouse_pos[1] - self.game.player.pos.y - (HEIGHT / 2)) / TILESIZE))
		Console.debug(message=f"mouse: {mouse_pos}\tplayer: {self.game.player.pos}, W/H: {WIDTH}x{HEIGHT}")
		Console.debug(message=f"{(mouse_pos[0] // TILESIZE - self.game.player.pos.x - WIDTH / 2) // TILESIZE}")
		if mouse[0]:
			block = self.game.world.getBlockAt(*rel_mouse)

			if not block.material.displayName == "Tree":
				# Console.debug(message=(rel_mouse, block.material.displayName))
				pass

			# The block is unbreakable
			if not block.material.tools:
				return

			# Check if the player has a correct tool
			if self.game.player.inventory.hands[0].item.texturePath.lower() in block.material.tools or \
				self.game.player.inventory.hands[1].item.texturePath.lower() in block.material.tools:

				# Console.debug(message=f"{rel_mouse} {block.material.displayName}")

				# Chop down the tree
				self.game.world.setBlock(*rel_mouse, Block(Materials.GRASS.value))

				# Add items to inventory
				# TODO: Add woodcutting skill multiplier
				amount = randint(1, 5)
				self.game.player.inventory.add_new_item(Items.WOOD.value, amount)
				# Display message for amount of wood
				Console.log(thread="PLAYER", message=f"You got {amount} wood!")

				# TODO: Add wood to inventory
				# Add exp to woodcutting
				# TODO: Add multiplier/check tree type?
				if not block.material.xptypes:
					return
				for xptype in block.material.xptypes:
					Baseskills[xptype].lvl.xp += 10
					# TODO: Pure debug text, remove later, also always tree's display text
					Console.log(thread="PLAYER",
									message="You chopped down a tree and gained 10 Woodcutting xp!")
					Console.log(thread="PLAYER", message="Your player gained 10 xp")
					self.game.player.lvl.xp += 10
					self.game.player.check_levels()
			else:
				Console.log(thread="PLAYER", message="You need an axe to break a tree")
