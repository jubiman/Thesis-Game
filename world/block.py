from world.material.material import Material


class Block:
	def __init__(self, material: Material, data: object = None):
		if data is None:
			data = {}
		self.material: Material = material
		self.data: object = data
