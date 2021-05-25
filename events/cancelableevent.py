from events.event import Event


class CancelableEvent(Event):
	"""
	These events can be canceled.
	"""

	def __init__(self, canceled=False):
		super().__init__()
		self.canceled = canceled

	def is_canceled(self):
		return self.canceled

	def set_canceled(self, canceled: bool):
		self.canceled = canceled
