class ArgumentException(Exception):
	def __init__(self, argc=0, message=None):
		if not message:
			self.message = f"Expected 2 arguments, got {argc} instead."
		else:
			self.message = message
		super().__init__(self.message)

	def __str__(self):
		return self.message
