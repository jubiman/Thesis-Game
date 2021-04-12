import item
import sys


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
						continue
				except IndexError:
					print("Please add an argument to this comment")
					continue
			print(f"Could not find command {s[0]}. Please check for correct spelling")

	def kill(self):
		self.running = False
