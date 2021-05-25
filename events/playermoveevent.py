from events.cancelableevent import CancelableEvent
from events.playerevent import PlayerEvent
from world.location import Location


class PlayerMoveEvent(PlayerEvent, CancelableEvent):
	"""
	Example event
	"""

	def __init__(self, player, fromloc: Location, toloc: Location):
		super(PlayerEvent, self).__init__(player)
		super(CancelableEvent, self).__init__()
		self.fromloc = fromloc
		self.toloc = toloc
