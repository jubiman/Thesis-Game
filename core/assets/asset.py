class Asset:
	# TODO: add plural name?
	def __init__(self, displayName, texturePath, iden):
		"""
		:param str displayName: The name of the item
		:param str texturePath: The assetname of the skill
		:param int iden: The ID of the item
		:param int mx_sk: The maximum amount the player can hold of the item in one slot (max_stack)
		"""
		self.displayName = displayName
		self.texturePath = texturePath
		self.image = None
		self.rect = None
		self.id = iden
