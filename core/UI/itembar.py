import pygame

from settings import WIDTH, HEIGHT, WHITE


class Itembar:
    def __init__(self):
        self.game = None

    def draw(self):
        backgrounditembar = pygame.Rect(WIDTH / 2 - 320, HEIGHT - 150, 640, 80)
        pygame.draw.rect(self.game.screen, (75, 75, 75), backgrounditembar)

        if self.game.player.inventory.selectedslot == 1:
            slot1 = pygame.Rect(WIDTH / 2 - 320, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot1)
        elif self.game.player.inventory.selectedslot == 2:
            slot2 = pygame.Rect(WIDTH / 2 - 240, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot2)
        elif self.game.player.inventory.selectedslot == 3:
            slot3 = pygame.Rect(WIDTH / 2 - 160, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot3)
        elif self.game.player.inventory.selectedslot == 4:
            slot4 = pygame.Rect(WIDTH / 2 - 80, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot4)
        elif self.game.player.inventory.selectedslot == 5:
            slot5 = pygame.Rect(WIDTH / 2 - 0, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot5)
        elif self.game.player.inventory.selectedslot == 6:
            slot6 = pygame.Rect(WIDTH / 2 + 80, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot6)
        elif self.game.player.inventory.selectedslot == 7:
            slot7 = pygame.Rect(WIDTH / 2 + 160, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot7)

        itembar1 = pygame.Rect(WIDTH / 2 - 310, HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar1)
        itembar2 = pygame.Rect(WIDTH / 2 - 230, HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar2)
        itembar3 = pygame.Rect(WIDTH / 2 - 150, HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar3)
        itembar4 = pygame.Rect(WIDTH / 2 - 70, HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar4)
        itembar5 = pygame.Rect(WIDTH / 2 + 10, HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar5)
        itembar6 = pygame.Rect(WIDTH / 2 + 90, HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar6)
        itembar7 = pygame.Rect(WIDTH / 2 + 170, HEIGHT - 140, 60, 60)
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar7)

        if self.game.paused:
            self.drawInventory()

    def drawInventory(self):
        pass