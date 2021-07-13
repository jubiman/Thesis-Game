from core.utils.errors.exceptions import InfinityException


# If x > 0, y must be > 0 as well
def mod(x, y):
	if y == 0 and x != 0:
		raise InfinityException
	if x < y:
		return x
	return mod(x - y, y)


# If x < 0, y must be < 0 as well
def negativeMod(x, y):
	if y == 0 and x != 0:
		raise InfinityException
	if x > y:
		return x
	return negativeMod(x - y, y)


# Check if x > 0 or x < 0, returns corresponding mod function
def specialMod(x, y):
	if x > 0:
		return mod(x, y)
	return negativeMod(x, -y)
