from enum import Enum

from core.UI.healthbar import Healthbar
from core.UI.itembar import Itembar


class UI(Enum):
	HEALTHBAR = Healthbar()
	ITEMBAR = Itembar()

	@staticmethod
	def load(game):
		for obj in UI:
			obj.value.game = game

	@staticmethod
	def draw(screen):
		for obj in UI:
			obj.value.draw(screen)

	@staticmethod
	def getElementByID(iden):
		"""
		:param iden: The ID of the element (you can also use list(UI)[id])
		:return: UI element
		:rtype: Any
		"""
		return list(UI)[iden]
