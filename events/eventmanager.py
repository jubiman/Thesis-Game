from events.cancelableevent import CancelableEvent
from events.event import Event
from events.eventhandler import EventHandler


class EventManager:
	listeners: list[EventHandler] = []

	@staticmethod
	def call_event(event: Event):
		for handler in EventManager.listeners:
			for var in handler.__annotations__:
				if isinstance(event.__class__, handler.__annotations__[var]):
					if not handler.ignore_canceled or (
							isinstance(event.__class__, CancelableEvent.__class__) and not event.is_canceled()):
						handler(event)
					break
		return event

	@staticmethod
	def register_listener(handler):
		EventManager.listeners.append(handler)
		EventManager.listeners.sort(reverse=True, key=lambda a: a.priority)
