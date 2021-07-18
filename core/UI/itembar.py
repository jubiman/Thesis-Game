import pygame
import settings
from core.inventory.inventory import SelectedSlot

class Itembar:
    def __init__(self):
        self.game = None
        self.inventory = SelectedSlot()

    def setItemSlot(self, newitemslot):
        self.inventory.itemslot = newitemslot

    def draw(self):
        backgrounditembar = pygame.Rect(settings.WIDTH / 2 - 320, settings.HEIGHT - 150, 640, 80)
        pygame.draw.rect(self.game.screen, (75, 75, 75), backgrounditembar)

        if self.inventory.itemslot == 1:
            slot1 = pygame.Rect(settings.WIDTH / 2 - 320, settings.HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, settings.WHITE, slot1)
        elif self.inventory.itemslot == 2:
            slot2 = pygame.Rect(settings.WIDTH / 2 - 240, settings.HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, settings.WHITE, slot2)
        elif self.inventory.itemslot == 3:
            slot3 = pygame.Rect(settings.WIDTH / 2 - 160, settings.HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, settings.WHITE, slot3)
        elif self.inventory.itemslot == 4:
            slot4 = pygame.Rect(settings.WIDTH / 2 - 80, settings.HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, settings.WHITE, slot4)
        elif self.inventory.itemslot == 5:
            slot5 = pygame.Rect(settings.WIDTH / 2 - 0, settings.HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, settings.WHITE, slot5)
        elif self.inventory.itemslot == 6:
            slot6 = pygame.Rect(settings.WIDTH / 2 + 80, settings.HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, settings.WHITE, slot6)
        elif self.inventory.itemslot == 7:
            slot7 = pygame.Rect(settings.WIDTH / 2 + 160, settings.HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, settings.WHITE, slot7)

        itembar1 = pygame.Rect(settings.WIDTH / 2 - 310, settings.HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar1)
        itembar2 = pygame.Rect(settings.WIDTH / 2 - 230, settings.HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar2)
        itembar3 = pygame.Rect(settings.WIDTH / 2 - 150, settings.HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar3)
        itembar4 = pygame.Rect(settings.WIDTH / 2 - 70, settings.HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar4)
        itembar5 = pygame.Rect(settings.WIDTH / 2 + 10, settings.HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar5)
        itembar6 = pygame.Rect(settings.WIDTH / 2 + 90, settings.HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar6)
        itembar7 = pygame.Rect(settings.WIDTH / 2 + 170, settings.HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar7)
