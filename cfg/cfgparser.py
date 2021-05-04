from os import path


class CfgParser:
	def __init__(self, game, fn):
		self.game = game
		if path.exists(fn):
			self.file = open(fn, 'r')

	def read(self):
		if self.file is None:
			return
		for line in self.file.readlines():
			s = line.split()
			try:
				if s[0] == "bind":
					try:
						self.game.cpc['BINDS'][s[1].strip('"')] = s[2].strip('"')
					except IndexError:
						print(f"Expected 2 arguments, got {len(s)-1} instead.")
					except KeyError:
						try:
							self.game.cpc.add_section('BINDS')
							self.game.cpc.set('BINDS', s[1].strip('"'), s[2].strip('"'))
						except KeyError:
							pass
						else:
							continue
						print(f"Couldn't find {s[1]} in ConfigParser, please check your spelling.")
			except Exception:
				print("Failed")

		with open(path.join(path.dirname(__file__), 'controls.ini'), 'w') as f:
			self.game.cpc.write(f)
			f.close()
		self.file.close()
