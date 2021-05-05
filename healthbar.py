import pygame


class HealthBar:
    def __init__(self, health, countdown):
        self.health = health
        self.countdown = countdown

    def resethealth(self):
        HealthBar.__init__(self).health = 100

    def sethealthbar1(self, health):
        # with health-regen reset
        HealthBar.__init__(self).health = health
        HealthBar.__init__(self).countdown = 5
        if HealthBar.__init__(self).health <= 0:
            self.console.kill()
            HealthBar.__init__(self).health = 100

    def sethealthbar2(self, health):
        # without health-regen reset
        HealthBar.__init__(self).health = health
        if HealthBar.__init__(self).health <= 0:
            self.console.kill()
            HealthBar.__init__(self).health = 100

    def gethealthbar(self):
        return HealthBar.__init__(self).health

    def drawhealthbar(self):
        backgroundhealthbar = pygame.Rect(50, 50, 180, 50)
        pygame.draw.rect(self.screen, (0, 0, 0), backgroundhealthbar)
        currenthealthbar = pygame.Rect(50, 50, self.gethealthbar() / 100 * 180, 50)
        pygame.draw.rect(self.screen, (0, 200, 0), currenthealthbar)
        currenthealthtext = pygame.font.SysFont('Corbel', 40).render(self.gethealthbar(), True, (255, 255, 255))
        self.screen.blit(currenthealthtext, (currenthealthbar + 60, currenthealthbar.y))

    def regen(self):
        if HealthBar.__init__(self).countdown > 0:
            HealthBar.__init__(self).countdown = HealthBar.__init__(self).countdown - 1
        else:
            HealthBar.__init__(self).health = HealthBar.__init__(self).health + 5
