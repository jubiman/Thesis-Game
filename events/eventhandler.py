from events.eventmanager import EventManager


class EventHandler:

	def __init__(self):
		self.ignore_canceled = False
		self.priority = 0

	@staticmethod
	def register(priority=0, ignore_canceled=False):
		"""
		**Usage**::

			@EventHandler.register()
			def on_damage(event: DamageEvent):
				# Do funny stuff

		:param priority: Higher priority means the event will be called earlier.
		:param ignore_canceled: Ignore canceled events.
		:return:
		"""

		def decorator(handler):
			handler.priority = priority
			handler.ignore_canceled = ignore_canceled
			EventManager.register_listener(handler)
			return handler

		return decorator
