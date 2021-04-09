from world.chunk import Chunk


class Cache:
	def __init__(self, world):
		self.world = world
		self.chunks: dict[str, Chunk] = {}

	def getChunk(self, x: int, y: int):
		if f"{x},{y}" in self.chunks:
			return self.chunks[f"{x},{y}"]
		self.chunks[f"{x},{y}"] = self.world.loadChunk(x, y)
		return self.chunks[f"{x},{y}"]
