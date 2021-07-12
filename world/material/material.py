class Material:
	def __init__(self, displayName, texturePath, iden, idstring, tools: list[str] = None, xptypes: list[str] = None):
		# TODO: Might change tools to seperate class (item/tool class)
		self.displayName = displayName
		self.texturePath = texturePath
		self.id = iden
		self.idstring = idstring
		self.xptypes = xptypes
		self.tools = tools
		self.image = None
		self.rect = None

	# TODO: Get correct items and use skill multipliers
	def calculateItemDrops(self):
		pass
