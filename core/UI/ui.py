from core.UI.healthbar import Healthbar


class UI:
	uiElements = []

	@staticmethod
	def load(game):
		UI.uiElements.append(Healthbar(game.player))

	@staticmethod
	def draw(screen):
		for obj in UI.uiElements:
			obj.draw(screen)

	@staticmethod
	def getElementByID(iden):
		"""
		:param iden: The ID of the element (can also do UI.uiElements[id])
		:return: UI element
		:rtype: Any
		"""
		return UI.uiElements[iden]

	@staticmethod
	def getElementByStr(name):
		"""
		:param name: The name of the element
		:return: None or the UI element
		"""
		for el in UI.uiElements:
			if name.lower() == el.__class__.__name__.lower():
				return el
		return None
