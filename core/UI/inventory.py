from core.assets.assets import Assets
from core.utils.colors import Colors
from core.utils.settings import Settings
import pygame


class Inventory:
    openinventory = False
    inventorytimer = 0

    def __init__(self):
        self.game = None

    def draw(self):
        if self.openinventory:
            self.drawInv()

    def drawInv(self):
        background = pygame.Rect(Settings.Game.WIDTH / 2 - 320, Settings.Game.HEIGHT - 500, 640, 240)
        pygame.draw.rect(self.game.screen, (75, 75, 75), background)
        title = pygame.font.SysFont('Corbel', 25, bold=pygame.font.Font.bold).render(
                                                                                str("Inventory"), True, Colors.WHITE)
        self.game.screen.blit(title, (Settings.Game.WIDTH / 2 - 310, Settings.Game.HEIGHT - 540))

        for i, item in enumerate(self.game.player.inventory.get()):
            # Row 1
            if i <= 7:
                pygame.draw.rect(self.game.screen, (50, 50, 50),
                                 pygame.Rect(Settings.Game.WIDTH / 2 - 310 + 80 * i,
                                             Settings.Game.HEIGHT - 490, 60, 60))
                self.game.screen.blit(pygame.transform.scale(item.item.image, (60, 60)), pygame.Rect(
                                    Settings.Game.WIDTH / 2 - 310 + 80 * i, Settings.Game.HEIGHT - 490, 60, 60))
            # Row 2
            if 8 <= i <= 15:
                pygame.draw.rect(self.game.screen, (50, 50, 50),
                                 pygame.Rect(Settings.Game.WIDTH / 2 - 310 + 80 * (i - 8),
                                             Settings.Game.HEIGHT - 410, 60, 60))
                self.game.screen.blit(pygame.transform.scale(item.item.image, (60, 60)), pygame.Rect(
                                    Settings.Game.WIDTH / 2 - 310 + 80 * (i - 8), Settings.Game.HEIGHT - 410, 60, 60))
            # Row 3
            if 16 <= i <= 23:
                pygame.draw.rect(self.game.screen, (50, 50, 50),
                                 pygame.Rect(Settings.Game.WIDTH / 2 - 310 + 80 * (i - 16),
                                             Settings.Game.HEIGHT - 330, 60, 60))
                self.game.screen.blit(pygame.transform.scale(item.item.image, (60, 60)), pygame.Rect(
                                    Settings.Game.WIDTH / 2 - 310 + 80 * (i - 16), Settings.Game.HEIGHT - 330, 60, 60))
