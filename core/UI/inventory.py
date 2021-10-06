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

        for i in range(24):
            # Row 1
            if i <= 7:
                pygame.draw.rect(self.game.screen, (50, 50, 50),
                                 pygame.Rect(Settings.Game.WIDTH / 2 - 310 + 80 * i,
                                             Settings.Game.HEIGHT - 490, 60, 60))
            # Row 2
            if 8 <= i <= 15:
                pygame.draw.rect(self.game.screen, (50, 50, 50),
                                 pygame.Rect(Settings.Game.WIDTH / 2 - 310 + 80 * (i - 8),
                                             Settings.Game.HEIGHT - 410, 60, 60))
            # Row 3
            if 16 <= i <= 23:
                pygame.draw.rect(self.game.screen, (50, 50, 50),
                                 pygame.Rect(Settings.Game.WIDTH / 2 - 310 + 80 * (i - 16),
                                             Settings.Game.HEIGHT - 330, 60, 60))

        for i, item in enumerate(self.game.player.inventory.get()):
            amount = pygame.font.SysFont('Corbel', 25).render(str(item.quantity), True, Colors.WHITE)

            # Row 1
            if i <= 7:
                self.game.screen.blit(pygame.transform.scale(item.item.image, (60, 60)), pygame.Rect(
                                    Settings.Game.WIDTH / 2 - 310 + 80 * i, Settings.Game.HEIGHT - 490, 60, 60))
                if item.item.max_stack > 1:
                    if 1 <= item.quantity <= 9:
                        self.game.screen.blit(amount,
                                              (Settings.Game.WIDTH / 2 - 265 + 80 * i, Settings.Game.HEIGHT - 460))
                    if 10 <= item.quantity <= 99:
                        self.game.screen.blit(amount,
                                              (Settings.Game.WIDTH / 2 - 279 + 80 * i, Settings.Game.HEIGHT - 460))
                    if 100 <= item.quantity <= 999:
                        self.game.screen.blit(amount,
                                              (Settings.Game.WIDTH / 2 - 289 + 80 * i, Settings.Game.HEIGHT - 460))
            # Row 2
            if 8 <= i <= 15:
                self.game.screen.blit(pygame.transform.scale(item.item.image, (60, 60)), pygame.Rect(
                                    Settings.Game.WIDTH / 2 - 310 + 80 * (i - 8), Settings.Game.HEIGHT - 410, 60, 60))
                if item.item.max_stack > 1:
                    if 1 <= item.quantity <= 9:
                        self.game.screen.blit(amount,
                                              (Settings.Game.WIDTH / 2 - 265 + 80 * (i - 8), Settings.Game.HEIGHT - 380))
                    if 10 <= item.quantity <= 99:
                        self.game.screen.blit(amount,
                                              (Settings.Game.WIDTH / 2 - 279 + 80 * (i - 8), Settings.Game.HEIGHT - 380))
                    if 100 <= item.quantity <= 999:
                        self.game.screen.blit(amount,
                                              (Settings.Game.WIDTH / 2 - 289 + 80 * (i - 8), Settings.Game.HEIGHT - 380))
            # Row 3
            if 16 <= i <= 23:
                self.game.screen.blit(pygame.transform.scale(item.item.image, (60, 60)), pygame.Rect(
                                    Settings.Game.WIDTH / 2 - 310 + 80 * (i - 16), Settings.Game.HEIGHT - 330, 60, 60))
                if item.item.max_stack > 1:
                    if 1 <= item.quantity <= 9:
                        self.game.screen.blit(amount,
                                              (Settings.Game.WIDTH / 2 - 265 + 80 * (i - 16), Settings.Game.HEIGHT - 300))
                    if 10 <= item.quantity <= 99:
                        self.game.screen.blit(amount,
                                              (Settings.Game.WIDTH / 2 - 279 + 80 * (i - 16), Settings.Game.HEIGHT - 300))
                    if 100 <= item.quantity <= 999:
                        self.game.screen.blit(amount,
                                              (Settings.Game.WIDTH / 2 - 289 + 80 * (i - 16), Settings.Game.HEIGHT - 300))
