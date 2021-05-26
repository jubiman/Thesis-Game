from events.event import Event


class PlayerEvent(Event):
	def __init__(self, player):
		self.player = player
