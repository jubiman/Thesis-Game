import pygame
from core.assets.assets import Assets
from core.items.items import Items
import core.inventory.inventory
from settings import WIDTH, HEIGHT, WHITE


class Itembar:
    def __init__(self):
        self.game = None
        self.inventory = core.inventory.inventory

    def draw(self):
        backgrounditembar = pygame.Rect(WIDTH / 2 - 320, HEIGHT - 150, 640, 80)
        pygame.draw.rect(self.game.screen, (75, 75, 75), backgrounditembar)

        if self.game.player.inventory.selectedslot == 0:
            slot1 = pygame.Rect(WIDTH / 2 - 320, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot1)
        elif self.game.player.inventory.selectedslot == 1:
            slot2 = pygame.Rect(WIDTH / 2 - 240, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot2)
        elif self.game.player.inventory.selectedslot == 2:
            slot3 = pygame.Rect(WIDTH / 2 - 160, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot3)
        elif self.game.player.inventory.selectedslot == 3:
            slot4 = pygame.Rect(WIDTH / 2 - 80, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot4)
        elif self.game.player.inventory.selectedslot == 4:
            slot5 = pygame.Rect(WIDTH / 2 - 0, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot5)
        elif self.game.player.inventory.selectedslot == 5:
            slot6 = pygame.Rect(WIDTH / 2 + 80, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot6)
        elif self.game.player.inventory.selectedslot == 6:
            slot7 = pygame.Rect(WIDTH / 2 + 160, HEIGHT - 150, 80, 80)
            pygame.draw.rect(self.game.screen, WHITE, slot7)

        itembarrects = [pygame.Rect(WIDTH / 2 - 310, HEIGHT - 140, 60, 60),
                        pygame.Rect(WIDTH / 2 - 230, HEIGHT - 140, 60, 60),
                        pygame.Rect(WIDTH / 2 - 150, HEIGHT - 140, 60, 60),
                        pygame.Rect(WIDTH / 2 - 70, HEIGHT - 140, 60, 60),
                        pygame.Rect(WIDTH / 2 + 10, HEIGHT - 140, 60, 60),
                        pygame.Rect(WIDTH / 2 + 90, HEIGHT - 140, 60, 60),
                        pygame.Rect(WIDTH / 2 + 170, HEIGHT - 140, 60, 60)]

        itembar = [(WIDTH / 2 - 310, HEIGHT - 140),
                   (WIDTH / 2 - 230, HEIGHT - 140),
                   (WIDTH / 2 - 150, HEIGHT - 140),
                   (WIDTH / 2 - 70, HEIGHT - 140),
                   (WIDTH / 2 + 10, HEIGHT - 140),
                   (WIDTH / 2 + 90, HEIGHT - 140),
                   (WIDTH / 2 + 170, HEIGHT - 140),
                   (WIDTH / 2 + 250, HEIGHT - 140)]

        pygame.draw.rect(self.game.screen, (50, 50, 50), itembarrects[0])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembarrects[1])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembarrects[2])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembarrects[3])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembarrects[4])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembarrects[5])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembarrects[6])
        self.game.screen.blit(pygame.transform.scale(Assets.BACKPACK1.value.image, (60, 60)), itembar[7])

        for i, item in enumerate(self.game.player.inventory.getslots()):
            self.game.screen.blit(pygame.transform.scale(item.item.image, (60, 60)), itembar[i])
            if item.item != Items.EMPTY.value:
                if 1 <= item.quantity <= 9:
                    amount = pygame.font.SysFont('Corbel', 25).render(str(item.quantity), True, WHITE)
                    self.game.screen.blit(amount, (WIDTH / 2 - 265 + 80 * i, HEIGHT - 110))
                if 10 <= item.quantity <= 99:
                    amount = pygame.font.SysFont('Corbel', 25).render(str(item.quantity), True, WHITE)
                    self.game.screen.blit(amount, (WIDTH / 2 - 279 + 80 * i, HEIGHT - 110))
                if 100 <= item.quantity <= 999:
                    amount = pygame.font.SysFont('Corbel', 25).render(str(item.quantity), True, WHITE)
                    self.game.screen.blit(amount, (WIDTH / 2 - 289 + 80 * i, HEIGHT - 110))
            if i == self.game.player.inventory.selectedslot:
                self.game.screen.blit(pygame.transform.flip(pygame.transform.scale(item.item.image, (30, 30)), True, False), (WIDTH / 2 - 44, HEIGHT / 2 - 6))
