import time


class Timer:
	timers = {}

	@staticmethod
	def start(name):
		Timer.timers[name] = time.time()

	@staticmethod
	def stop(name):
		start = Timer.timers[name]
		dura = time.time() - start
		del Timer.timers[name]
		return dura
