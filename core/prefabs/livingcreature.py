class LivingCreature:
	def __init__(self, game, hp, max_hp, armor, speed, hp_regen):
		# Get the game's object so we can interact with the world
		self.game = game

		# LivingCreature Base
		self.hp = hp
		self.max_hp = max_hp
		self.hp_regen = hp_regen
		self.armor = armor
		self.speed = speed
