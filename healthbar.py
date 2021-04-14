import pygame


class HealthBar:
    def __init__(self, health, countdown):
        self.health = health
        self.countdown = countdown

    def resethealth(self):
        HealthBar.health = 100

    def sethealthbar1(self, health):
        # with health-regen reset
        HealthBar.health = health
        HealthBar.countdown = 5
        if HealthBar.health <= 0:
            self.console.kill()
            HealthBar.health = 100

    def sethealthbar2(self, health):
        # without health-regen reset
        HealthBar.health = health
        if HealthBar.health <= 0:
            self.console.kill()
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
            HealthBar.health = HealthBar.health + 5
