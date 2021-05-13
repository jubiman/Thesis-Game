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
