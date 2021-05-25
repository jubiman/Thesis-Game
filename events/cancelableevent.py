from events.event import Event


class CancelableEvent(Event):
	"""
	These events can be canceled.
	"""

	def __init__(self, canceled=False):
		super().__init__()
		self.canceled = canceled
