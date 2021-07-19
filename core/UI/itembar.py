import pygame

from settings import WIDTH, HEIGHT, WHITE


class Itembar:
    def __init__(self):
        self.game = None

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

        itembar = [pygame.Rect(WIDTH / 2 - 310, HEIGHT - 140, 60, 60),
                pygame.Rect(WIDTH / 2 - 230, HEIGHT - 140, 60, 60),
                pygame.Rect(WIDTH / 2 - 150, HEIGHT - 140, 60, 60),
                pygame.Rect(WIDTH / 2 - 70, HEIGHT - 140, 60, 60),
                pygame.Rect(WIDTH / 2 + 10, HEIGHT - 140, 60, 60),
                pygame.Rect(WIDTH / 2 + 90, HEIGHT - 140, 60, 60),
                pygame.Rect(WIDTH / 2 + 170, HEIGHT - 140, 60, 60)]

        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar[0])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar[1])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar[2])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar[3])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar[4])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar[5])
        pygame.draw.rect(self.game.screen, (50, 50, 50), itembar[6])

        for i, item in enumerate(self.game.player.inventory.slots.get()):
            self.game.screen.blit(pygame.transform.scale(item.image, (60, 60)), itembar[i])
