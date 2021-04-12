import pygame.math

import item
import sys

import sprites


class Console:
	def __init__(self, game):
		self.game = game
		self.running = True

	def run(self):
		while self.running:
			inp = sys.stdin.readline()
			s = inp.split()
			if s[0] == "give":
				try:
					self.game.player.inventory.add_new_item(item.get_item_from_name(self.game.items, s[1]), int(s[2]))
				except ValueError:
					print("Could not convert int to string")
				except Exception:
					pass
				continue
			elif s[0] == "debug":
				try:
					if s[1] == "pos" or s[1] == "position":
						print(self.game.player.pos)
					elif s[1] == "bases":
						print(sprites.Player.__bases__)
				except IndexError:
					print("Please add an argument to this comment")
				finally:
					continue
			elif s[0] == "setpos":
				try:
					self.game.player.pos = pygame.math.Vector2(float(s[1]), float(s[2]))
				except Exception as ex:
					print(ex)
				finally:
					continue
			elif s[0] == "xp":
				try:
					if s[1] == "give" or s[1] == "add":
						if len(s) == 3:
							self.game.player.lvl.xp += int(s[2])
				except ValueError:
					print(f"Could not convert {s[2]} to an integer, please check your values and try again")
				else:
					self.game.player.check_levels()
				finally:
					continue

			print(f"Could not find command {s[0]}. Please check for correct spelling")

	def kill(self):
		self.running = False
