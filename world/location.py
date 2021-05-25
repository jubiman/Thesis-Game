class Location:
	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

	def clone(self):
		return Location(self.x, self.y)
