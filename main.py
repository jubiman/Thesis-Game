# import modules
import pygame
import random
import sys
import getopt
# from os import system
# system('cls')
fps = 144

# TODO: make this better lol
# Check arguments
try:
	opts, args = getopt.getopt(sys.argv[1:], 'f', ["fps="])
except getopt.GetoptError as err:
	print(err)
for o, a in opts:
	if o == '--fps':
		fps = a

print('FPS is: ', fps)

# Define global window area
wWidth = 1600
wHeight = 900
clock = pygame.time.Clock()


class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.surf = pygame.Surface((20, 10))
		self.surf.fill((255, 255, 255))
		self.rect = self.surf.get_rect(center=(random.randint(wWidth+20, wWidth+100), random.randint(0, wHeight)))
		self.speed = random.randint(3, 5)

	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.surf = pygame.Surface((75, 25))
		self.surf.fill((255, 255, 255))
		self.rect = self.surf.get_rect()

	def update(self, presk):
		if presk[pygame.key.K_w]:
			self.rect.move_ip(0, -2)
		if presk[pygame.key.K_s]:
			self.rect.move_ip(0, 2)
		if presk[pygame.key.K_a]:
			self.rect.move_ip(-2, 0)
		if presk[pygame.key.K_d]:
			self.rect.move_ip(2, 0)

		# Keep player on the screen
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > wWidth:
			self.rect.right = wWidth
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= wHeight:
			self.rect.bottom = wHeight


# Initialize pygame
pygame.init()

# Create window object
window = pygame.display.set_mode((wWidth, wHeight))
window.fill((255, 255, 255))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Init player object
player = Player()

# Init enemies objects
enemies = pygame.sprite.Group()
sprites = pygame.sprite.Group()
sprites.add(player)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.key.KEYDOWN:
			if event.key == pygame.key.K_ESCAPE:
				running = False
		elif event.type == pygame.event.QUIT:
			running = False
		elif event.type == ADDENEMY:
			nEn = Enemy()
			enemies.add(nEn)
			sprites.add(nEn)

	# Fill the screen with black
	window.fill((0, 0, 0))

	# Draw sprites
	for ent in sprites:
		window.blit(ent.surf, ent.rect)

	# Check collision
	if pygame.sprite.spritecollideany(player, enemies):
		player.kill()
		running = False

	# Get all the keys currently pressed
	presK = pygame.key.get_pressed()
	# Update the player sprite based on user keypresses
	player.update(presK)
	enemies.update()
	# Update the display
	pygame.display.flip()

	# Run at framerate
	clock.tick(fps)
