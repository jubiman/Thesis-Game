import inspect
from functools import partial


class Levelbase:
	def __init__(self, level, xp, xpn, xpf="self.xp_needed+10", game=None):
		"""
		:param int level: The level value
		:param int xp: Current experience/skill points
		:param int xpn: XP/SP needed for levelup
		:param str xpf: The xp formula for level ups
		"""
		self.level = level
		self.xp = xp  # XP could be used for Skill Points!
		self.xp_needed = xpn
		self.xp_formula = xpf
		self.game = game

	def levelup(self, t=""):
		"""
		:param str t: Type of object levelup was called from (player/bs/ps)
		"""
		self.level += 1
		self.xp = 0
		self.xp_needed = eval(self.xp_formula)  # TODO: Make dynamic XP/SP system to have working lvlbase
		try:
			meth = getattr(self.game.player, inspect.getouterframes(inspect.currentframe(), 2)[1][3])
			if isinstance(self.game.player, get_class_that_defined_method(meth)):
				self.game.player.hp += 10  # TODO: Add more player levelup bonus
		except Exception as ex:
			print(ex)


def get_class_that_defined_method(meth):
	if isinstance(meth, partial):
		return get_class_that_defined_method(meth.func)
	if inspect.ismethod(meth) or (
			inspect.isbuiltin(meth) and getattr(meth, '__self__', None) is not None and getattr(meth.__self__,
																								'__class__', None)):
		for cls in inspect.getmro(meth.__self__.__class__):
			if meth.__name__ in cls.__dict__:
				return cls
		meth = getattr(meth, '__func__', meth)  # fallback to __qualname__ parsing
	if inspect.isfunction(meth):
		cls = getattr(inspect.getmodule(meth),
						meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
						None)
		if isinstance(cls, type):
			return cls
	return getattr(meth, '__objclass__', None)  # handle special descriptor objects
