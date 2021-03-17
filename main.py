# import pygame
import pygame
from pygame.locals import *

# Define window area
wWidth = 1600
wHeight = 900


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.surf = pygame.Surface((75, 25))
		self.surf.fill((255, 255, 255))
		self.rect = self.surf.get_rect()

	def update(self, presk):
		if presk[K_w]:
			self.rect.move_ip(0, -5)
		if presk[K_s]:
			self.rect.move_ip(0, 5)
		if presk[K_a]:
			self.rect.move_ip(-5, 0)
		if presk[K_d]:
			self.rect.move_ip(5, 0)


# Initialize pygame
pygame.init()

# Create window object
window = pygame.display.set_mode((wWidth, wHeight))

window.fill((255, 255, 255))

player = Player()


running = True
while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
		elif event.type == QUIT:
			running = False

	# Get all the keys currently pressed
	presK = pygame.key.get_pressed()

	# Fill the screen with black
	window.fill((0, 0, 0))

	# Draw the player on the screen
	window.blit(player.surf, player.rect)

	# Update the player sprite based on user keypresses
	player.update(presK)

	# Update the display
	pygame.display.flip()
