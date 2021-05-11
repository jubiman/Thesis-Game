import pygame


class HealthBar:
    health = 100
    countdown = 0

    def __init__(self):
        pass

    def resethealth(self):
        HealthBar.health = 100

    def sethealthbar1(self, newhealth):
        # with health-regen reset
        HealthBar.health = newhealth
        HealthBar.countdown = 5
        if HealthBar.health <= 0:
            HealthBar.health = 100

    def sethealthbar2(self, newhealth):
        # without health-regen reset
        HealthBar.health = newhealth
        if HealthBar.health <= 0:
            HealthBar.health = 100

    def gethealthbar(self):
        return HealthBar.health

    def drawhealthbar(self):
        backgroundhealthbar = pygame.Rect(50, 50, 180, 50)
        pygame.draw.rect(self.screen, (0, 0, 0), backgroundhealthbar)
        currenthealthbar = pygame.Rect(50, 50, self.gethealthbar() / 100 * 180, 50)
        pygame.draw.rect(self.screen, (0, 200, 0), currenthealthbar)
        currenthealthtext = pygame.font.SysFont('Corbel', 40).render(self.gethealthbar(), True, (255, 255, 255))
        self.screen.blit(currenthealthtext, (currenthealthbar + 60, currenthealthbar.y))

    def regen(self):
        if HealthBar.countdown > 0:
            HealthBar.countdown = HealthBar.countdown - 1
        else:
            if HealthBar.health >= 100:
                pass
            elif HealthBar.health <= 95:
                HealthBar.sethealthbar2(self, HealthBar.health + 5)
            else:
                HealthBar.sethealthbar2(self, 100)
