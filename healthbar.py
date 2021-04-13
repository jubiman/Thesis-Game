import pygame

class HealthBar:
    def drawHealthBar(self):
        currenthealthbar = pygame.Rect(50, 50, 180, 50)
        pygame.draw.rect(self.screen, (0, 200, 0), currenthealthbar)
        currenthealthtext = pygame.font.SysFont('Corbel', 40).render('100', True, (255, 255, 255))
        self.screen.blit(currenthealthtext, (currenthealthbar + 60, currenthealthbar.y))