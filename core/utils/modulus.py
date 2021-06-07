from core.utils.errors.exceptions import InfinityException


def mod(x, y):
	if y == 0 and x != 0:
		raise InfinityException
	if x < y:
		return x
	return mod(x - y, y)
