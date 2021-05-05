import time

from settings import CHUNK_UNLOAD_DELAY
from world.chunk import Chunk


class Cache:
	def __init__(self, world):
		self.world = world
		self.chunks: dict[tuple[int, int], Chunk] = {}
		self.lastUsedAt: dict[tuple[int, int], int] = {}

	def checkForLazyChunks(self):
		unloadThese = []
		unloadIfLessThan = int(time.time() * 1000) - CHUNK_UNLOAD_DELAY
		for xy in self.lastUsedAt:
			if self.lastUsedAt[xy] < unloadIfLessThan:
				unloadThese.append(xy)
		for xy in unloadThese:
			del self.lastUsedAt[xy]
			self.world.unload(xy[0], xy[1])

	def getChunk(self, x: int, y: int):
		# print(f"{x},{y} used.")
		self.lastUsedAt[x, y] = int(time.time() * 1000)
		if (x, y) in self.chunks:
			return self.chunks[x, y]
		self.chunks[x, y] = self.world.loadChunk(x, y)
		return self.chunks[x, y]

	# Deprecated
	def setChunk(self, x: int, y: int):
		x = int(x)
		y = int(y)
		self.chunks[x, y] = self.world.specialLoadChunk(x, y)
