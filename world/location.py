class Location:
	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def set_x(self, x: float):
		self.x = x

	def set_y(self, y: float):
		self.y = y

	def clone(self):
		return Location(self.x, self.y)
