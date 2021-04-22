class Item:
	# TODO: add plural name?
	def __init__(self, displayName, texturePath, iden, maxStack):
		"""
		:param str name: The name of the item
		:param int iden: The ID of the item
		:param int max_stack: The maximum amount the player can hold of the item in one slot
		"""
		self.displayName = displayName
		self.texturePath = texturePath
		self.image = None
		self.id = iden
		self.max_stack = maxStack
