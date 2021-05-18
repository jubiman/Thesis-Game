from events.event import Event


class CancelableEvent(Event):
	def __init__(self, canceled=False):
		super.__init__(self)
		self.canceled = canceled

	def is_canceled(self):
		return self.canceled

	def set_canceled(self, canceled: bool):
		self.canceled = canceled
