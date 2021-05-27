from events.cancelableevent import CancelableEvent
from events.event import Event
from core.utils.timer import Timer


class EventManager:
	listeners: list = []

	@staticmethod
	def call_event(event: Event):
		Timer.start(f"Event call: {event.__class__.__name__}")
		for handler in EventManager.listeners:
			for var in handler.__annotations__:
				if isinstance(event.__class__, handler.__annotations__[var].__class__):
					if not handler.ignore_canceled or (
							isinstance(event.__class__, CancelableEvent.__class__) and not event.is_canceled()):
						handler(event)
					break
		dura = Timer.stop(f"Event call: {event.__class__.__name__}")
		print(f"Event call: {event.__class__.__name__} took {dura} seconds")
		return event

	@staticmethod
	def register_listener(handler):
		print("Registering handler: " + str(handler.__annotations__))
		EventManager.listeners.append(handler)
		EventManager.listeners.sort(reverse=True, key=lambda a: a.priority)
