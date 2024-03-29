"""
	Pathfinding using A* algorithm
"""
# TODO: Improve algorithm so entities don't go in eachother (and possibly do random movements when too close to player)
import pygame

from core.console.console import Console

# Diagonal movement is impossible (for now?)
adjacents = [
	(-1, 0),
	(0, 1),
	(1, 0),
	(0, -1),

	(1, 1),
	(-1, -1),
	(1, -1),
	(-1, 1)
]


class Pathfinding:
	@staticmethod
	def findFullStatic(ent, target, world):
		# Create start and end node
		startNode = Node(pos=ent.pos)
		endNode = Node(pos=target.pos)

		# If the distance to the player is bigger than 10 tiles, we don't move
		if ((startNode.pos.x - endNode.pos.x) ** 2) + ((startNode.pos.y - endNode.pos.y) ** 2) > 10:
			return None

		# Create lists
		openList = []
		closedList = []

		openList.append(startNode)

		while len(openList) > 0:
			current = openList[0]
			currIndex = 0

			for index, item in enumerate(openList):
				if item.f < current.f:
					current = item
					currIndex = index

			openList.pop(currIndex)
			closedList.append(current)

			# We have reached the target
			if current == endNode:
				path = []
				while current is not None:
					path.append(current.pos)
					current = current.parent
				return path[::-1]  # Return the path reversed

			# Generate children
			children = []
			for newpos in adjacents:
				# Get node pos
				nodepos = pygame.Vector2(current.pos.x + newpos[0], current.pos.y + newpos[1])

				# TODO: Add all collidable blocks
				if world.getBlockAt(*nodepos).material.id == 3:
					continue
				children.append(Node(current, nodepos))

			# Loop through children
			for child in children:
				for closedChild in closedList:
					if child == closedChild:
						continue

				child.g = current.g + 1
				child.h = ((child.pos.x - endNode.pos.x) ** 2) + ((child.pos.y - endNode.pos.y) ** 2)
				child.f = child.g + child.h

				for openNode in openList:
					if child == openNode and child.g > openNode.g:
						continue

				openList.append(child)

	@staticmethod
	def findOneStatic(ent, target, world):
		h = 0
		# Generate children
		children = []
		for newpos in adjacents:
			# Get node pos
			nodepos = pygame.Vector2(ent.pos.x + newpos[0], ent.pos.y + newpos[1])

			# TODO: Add all collidable blocks
			try:
				if world.getBlockAt(int(nodepos.x), int(nodepos.y)).material.id == 3:
					# Console.debug(message=f"Wall at {nodepos}")
					continue
			except IndexError:
				Console.error(f"IndexError: {nodepos}")

			if newpos[0] != 0 and newpos[1] != 0:
				nodepos1 = pygame.Vector2(ent.pos.x + newpos[0], ent.pos.y)
				nodepos2 = pygame.Vector2(ent.pos.x, ent.pos.y + newpos[1])
				if world.getBlockAt(nodepos1.x, nodepos1.y).material.id == 3:
					continue
				if world.getBlockAt(nodepos2.x, nodepos2.y).material.id == 3:
					continue

			children.append(Node(pos=nodepos))

		ind = 0
		for index, child in enumerate(children):
			newH = ((child.pos.x - target.pos.x) ** 2) + ((child.pos.y - target.pos.y) ** 2)
			if newH > h:
				h = newH
				ind = index
		return [ent.pos - children[ind].pos]


class Node:
	def __init__(self, parent=None, pos=None):
		self.parent = parent
		self.pos = pos
		self.g = 0
		self.h = 0
		self.f = 0

	def __eq__(self, other):
		return self.pos == other.pos
