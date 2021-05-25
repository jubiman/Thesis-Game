import pygame


class Healthbar:
    def __init__(self, player):
        self.countdown = 0
        self.player = player

    def resethealth(self):
        self.player.hp = 100

    def setHealthbarRegen(self, newhealth):
        # with health-regen reset
        self.player.hp = newhealth
        self.countdown = 5
        if self.player.hp <= 0:
            # TODO: DIE
            self.player.hp = 100

    def setHealthbar(self, newhealth):
        # without health-regen reset
        self.player.hp = newhealth
        if self.player.hp <= 0:
            # TODO: DIE
            self.player.hp = 100

    def draw(self, screen):
        backgroundhealthbar = pygame.Rect(50, 50, 180, 50)
        pygame.draw.rect(screen, (0, 0, 0), backgroundhealthbar)
        currenthealthbar = pygame.Rect(50, 50, self.player.hp / 100 * 180, 50)
        pygame.draw.rect(screen, (0, 200, 0), currenthealthbar)
        currenthealthtext = pygame.font.SysFont('Corbel', 40).render(str(self.player.hp), True, (255, 255, 255))
        screen.blit(currenthealthtext, (currenthealthbar.x + 60, currenthealthbar.y))

    def regen(self):
        if self.countdown > 0:
            self.countdown = self.countdown - 1
        else:
            if self.player.hp >= 100:
                pass
            elif self.player.hp <= 95:
                self.setHealthbarRegen(self.player.hp + 5)
            else:
                self.setHealthbarRegen(100)
