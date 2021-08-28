import pygame
from core.assets.images import Images


class Healthbar:
	def __init__(self):
		self.game = None
		self.countdown = 0

	def resethealth(self):
		self.game.player.hp = 100

	def setHealthbarRegen(self, newhealth):  # TODO: remove this from the UI and set it into the player
		# with health-regen reset
		self.game.player.hp = newhealth
		self.countdown = 5
		if self.game.player.hp <= 0:
			# TODO: DIE
			self.game.player.hp = 100

	def setHealthbar(self, newhealth):
		# without health-regen reset
		self.game.player.hp = newhealth
		if self.game.player.hp <= 0:
			# TODO: DIE
			self.game.player.hp = 100

	def update(self):
		pass

	def draw(self):
		# Health
		backgroundhealthbar = pygame.Rect(80, 40, 300, 40)
		pygame.draw.rect(self.game.screen, (0, 0, 0), backgroundhealthbar)
		currenthealthbar = pygame.Rect(80, 40, self.game.player.hp / 100 * 300, 40)
		pygame.draw.rect(self.game.screen, (0, 200, 0), currenthealthbar)
		currenthealthtext = pygame.font.SysFont('Corbel', 50).render(str(self.game.player.hp), True, (255, 255, 255))
		self.game.screen.blit(currenthealthtext, (400, 25))
		self.game.screen.blit(Images.HEALTH.value.image, (30, 30))

		# Mana (only temporary, before added its own class)
		backgroundmanabar = pygame.Rect(80, 110, 300, 40)
		pygame.draw.rect(self.game.screen, (0, 0, 0), backgroundmanabar)
		currentmanabar = pygame.Rect(80, 110, 300, 40)
		pygame.draw.rect(self.game.screen, (0, 0, 200), currentmanabar)
		currentmanatext = pygame.font.SysFont('Corbel', 50).render(str('100'), True, (255, 255, 255))
		self.game.screen.blit(currentmanatext, (400, 95))
		self.game.screen.blit(Images.MANA.value.image, (30, 100))

		# Level (only temporary, before added its own class)
		backgroundlevelbar = pygame.Rect(80, 180, 300, 40)
		pygame.draw.rect(self.game.screen, (0, 0, 0), backgroundlevelbar)
		currentlevelbar = pygame.Rect(80, 180, 300, 40)
		pygame.draw.rect(self.game.screen, (255, 165, 0), currentlevelbar)
		currentleveltext = pygame.font.SysFont('Corbel', 50).render(str(100), True, (255, 255, 255))
		self.game.screen.blit(currentleveltext, (400, 165))
		self.game.screen.blit(Images.LEVEL.value.image, (30, 170))

	def regen(self):
		if self.countdown > 0:
			self.countdown = self.countdown - 1
		else:
			if self.game.player.hp >= 100:
				return
			if self.game.player.hp <= 95:
				self.setHealthbarRegen(self.game.player.hp + 5)
			else:
				self.setHealthbarRegen(100)
