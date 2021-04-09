class Material:
	def __init__(self, displayName, texturePath, id):
		self.displayName = displayName
		self.texturePath = texturePath
		self.id = id
		self.image = None
		self.rect = None
