import pygame


class Healthbar:
    def __init__(self):
        self.countdown = 0
        self.game = None

    def resethealth(self):
        self.game.player.hp = 100

    def setHealthbarRegen(self, newhealth):  # TODO: remove this from the UI and set it into the player
        # with health-regen reset
        self.game.player.hp = newhealth
        self.countdown = 5
        if self.game.player.hp <= 0:
            # TODO: DIE
            self.game.player.hp = 100

    def setHealthbar(self, newhealth):
        # without health-regen reset
        self.game.player.hp = newhealth
        if self.game.player.hp <= 0:
            # TODO: DIE
            self.game.player.hp = 100

    def update(self):
        pass

    def draw(self, screen):
        backgroundhealthbar = pygame.Rect(50, 50, 180, 50)
        pygame.draw.rect(screen, (0, 0, 0), backgroundhealthbar)
        currenthealthbar = pygame.Rect(50, 50, self.game.player.hp / 100 * 180, 50)
        pygame.draw.rect(screen, (0, 200, 0), currenthealthbar)
        currenthealthtext = pygame.font.SysFont('Corbel', 40).render(str(self.game.player.hp), True, (255, 255, 255))
        screen.blit(currenthealthtext, (currenthealthbar.x + 60, currenthealthbar.y))

    def regen(self):
        if self.countdown > 0:
            self.countdown = self.countdown - 1
        else:
            if self.game.player.hp >= 100:
                return
            elif self.game.player.hp <= 95:
                self.setHealthbarRegen(self.game.player.hp + 5)
            else:
                self.setHealthbarRegen(100)
