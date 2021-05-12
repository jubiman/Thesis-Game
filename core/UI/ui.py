from core.UI.healthbar import Healthbar


class UI:
	uiElements = []

	@staticmethod
	def load(game):
		UI.uiElements.append(Healthbar(game.player, game.screen))

	@staticmethod
	def draw():
		for obj in UI.uiElements:
			obj.draw()
